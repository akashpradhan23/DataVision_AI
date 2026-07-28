import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

from sklearn.base import clone


def train_model(df, target_column):
    """
    Automatically trains multiple ML models and
    selects the best performing model.
    """

    # ----------------------------------
    # Copy Dataset
    # ----------------------------------
    data = df.copy()

    # ----------------------------------
    # Remove rows having missing target
    # ----------------------------------
    data = data.dropna(subset=[target_column]).reset_index(drop=True)

    if len(data) < 20:
        raise ValueError(
            "Not enough rows available after removing missing target values."
        )

    X = data.drop(columns=[target_column])
    y = data[target_column]

    # ----------------------------------
    # Check target
    # ----------------------------------
    if y.nunique() <= 1:
        raise ValueError(
            "Target column must contain at least two unique values."
        )

    # ----------------------------------
    # Detect Problem Type
    # ----------------------------------
    if pd.api.types.is_numeric_dtype(y):

        unique_ratio = y.nunique() / len(y)

        if y.nunique() <= 15 and unique_ratio < 0.05:
            problem_type = "classification"
        else:
            problem_type = "regression"

    else:
        problem_type = "classification"

    # ----------------------------------
    # Feature Types
    # ----------------------------------
    numeric_features = X.select_dtypes(include=np.number).columns.tolist()

    categorical_features = X.select_dtypes(exclude=np.number).columns.tolist()

    # ----------------------------------
    # Preprocessing
    # ----------------------------------
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median"))
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore"))
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features)
        ]
    )

    # ----------------------------------
    # Train Test Split
    # ----------------------------------
    if problem_type == "classification":

        # Check if every class has at least 2 samples
        class_counts = y.value_counts()

        if class_counts.min() < 2:
            stratify = None
        else:
            stratify = y

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42,
            stratify=stratify
        )

    else:

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42
        )

    # ----------------------------------
    # Models
    # ----------------------------------
    if problem_type == "regression":

        models = {
            "Linear Regression": LinearRegression(),
            "Decision Tree": DecisionTreeRegressor(random_state=42),
            "Random Forest": RandomForestRegressor(random_state=42),
        }

    else:

        models = {
            "Logistic Regression": LogisticRegression(max_iter=1000),
            "Decision Tree": DecisionTreeClassifier(random_state=42),
            "Random Forest": RandomForestClassifier(random_state=42),
        }

    best_model = None
    best_model_name = None
    best_score = float("-inf")

    evaluation = {}
    best_predictions = None

    # ----------------------------------
    # Train Every Model
    # ----------------------------------
    for name, model in models.items():

        pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", clone(model))
            ]
        )

        pipeline.fit(X_train, y_train)

        predictions = pipeline.predict(X_test)

        if problem_type == "regression":

            r2 = r2_score(y_test, predictions)
            mae = mean_absolute_error(y_test, predictions)
            rmse = np.sqrt(mean_squared_error(y_test, predictions))

            evaluation[name] = {
                "R2": round(r2, 4),
                "MAE": round(mae, 4),
                "RMSE": round(rmse, 4),
            }

            score = r2

        else:

            accuracy = accuracy_score(y_test, predictions)

            precision = precision_score(
                y_test,
                predictions,
                average="weighted",
                zero_division=0
            )

            recall = recall_score(
                y_test,
                predictions,
                average="weighted",
                zero_division=0
            )

            f1 = f1_score(
                y_test,
                predictions,
                average="weighted",
                zero_division=0
            )

            evaluation[name] = {
                "Accuracy": round(accuracy, 4),
                "Precision": round(precision, 4),
                "Recall": round(recall, 4),
                "F1": round(f1, 4),
            }

            score = accuracy

        if score > best_score:
            best_score = score
            best_model = pipeline
            best_model_name = name

            best_predictions = predictions
        # ----------------------------------
    # Feature Importance
    # ----------------------------------
    feature_importance = None

    try:
        model = best_model.named_steps["model"]
        preprocessor = best_model.named_steps["preprocessor"]

        feature_names = preprocessor.get_feature_names_out()

        if hasattr(model, "feature_importances_"):

            feature_importance = (
                pd.DataFrame({
                    "Feature": feature_names,
                    "Importance": model.feature_importances_
                })
                .sort_values(by="Importance", ascending=False)
                .reset_index(drop=True)
            )

        elif hasattr(model, "coef_"):

            coef = np.abs(model.coef_)

            if coef.ndim > 1:
                coef = coef.mean(axis=0)

            feature_importance = (
                pd.DataFrame({
                    "Feature": feature_names,
                    "Importance": coef
                })
                .sort_values(by="Importance", ascending=False)
                .reset_index(drop=True)
            )

    except Exception:
        feature_importance = None

    # ----------------------------------
    # Confusion Matrix
    # ----------------------------------
    cm = None

    if problem_type == "classification":
        cm = confusion_matrix(y_test, best_predictions)

    # ----------------------------------
    # Actual vs Predicted
    # ----------------------------------
    actual_vs_predicted = pd.DataFrame({
        "Actual": y_test.values,
        "Predicted": best_predictions
    })

    return {
        "problem_type": problem_type,
        "best_model_name": best_model_name,
        "best_model": best_model,
        "evaluation": evaluation,
        "feature_columns": X.columns.tolist(),
        "feature_importance": feature_importance,
        "X_test": X_test,
        "y_test": y_test,
        "predictions": best_predictions,
        "actual_vs_predicted": actual_vs_predicted,
        "confusion_matrix": cm
    }