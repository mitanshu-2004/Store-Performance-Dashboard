import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from modules.config import ensure_output_dir, get_charts_dir

def store_distribution(performance_data, january_predictions, output_dir=None):
    if output_dir is None:
        output_dir = ensure_output_dir()
    charts_dir = get_charts_dir()
    january_values = january_predictions["Jan_Prediction_XGBoost"]/100
    months = performance_data["Month"].cat.categories
    month_labels = list(months) + ["Jan (Predicted)"]
    monthly_distributions = [
        performance_data[performance_data["Month"] == month]["Attach_Percentage"]
        for month in months
    ] + [january_values]
    rows, cols = 3, 2
    fig, axes = plt.subplots(rows, cols, figsize=(16, 12), sharex=True, sharey=True)
    axes = axes.flatten()
    x_min, x_max = 0, 1.0
    max_count = 0
    for distribution in monthly_distributions:
        counts, _ = np.histogram(distribution, bins=30, range=(x_min, x_max))
        max_count = max(max_count, counts.max())
    for idx, (label, distribution) in enumerate(zip(month_labels, monthly_distributions)):
        ax = axes[idx]
        sns.histplot(distribution, kde=True, bins=30, ax=ax)
        ax.set_title(label)
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(0, max_count + 5)
        ax.set_xlabel("Attach Percentage")
        ax.set_ylabel("Count")
        ax.tick_params(labelleft=True)
        ax.tick_params(labelbottom=True)
    plt.tight_layout()
    plt.savefig(charts_dir / "attach_distribution_all_months.png")
    plt.close()
