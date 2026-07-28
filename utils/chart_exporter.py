import os

def save_chart(fig, filename):

    os.makedirs("reports/charts", exist_ok=True)

    path = os.path.join("reports", "charts", filename)

    fig.write_image(path)

    return path