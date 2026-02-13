import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from modules.config import ensure_output_dir, get_charts_dir

def branch_boxplot(performance_data, output_dir=None):
    if output_dir is None:
        output_dir = ensure_output_dir()
    charts_dir = get_charts_dir()
    plt.figure(figsize=(14, 7))
    sns.boxplot(
        data=performance_data,
        x="Branch",
        y="Attach_Percentage",
        hue="Branch",
        palette="viridis",
        legend=False
    )
    plt.title("Attach % Distribution by Branch")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(charts_dir / "branch_boxplot.png")
    plt.close()
