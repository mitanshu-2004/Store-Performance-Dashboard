import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from modules.config import ensure_output_dir, get_charts_dir

def branch_monthly_trend(performance_data, output_dir=None):
    if output_dir is None:
        output_dir = ensure_output_dir()
    charts_dir = get_charts_dir()
    plt.figure(figsize=(12, 7))
    sns.lineplot(
        data=performance_data,
        x="Month",
        y="Attach_Percentage",
        hue="Branch",
        marker="o"
    )
    plt.title("Month-wise Attach % Trend by Branch")
    plt.legend(bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.savefig(charts_dir / "monthly_trend_by_branch.png")
    plt.close()
