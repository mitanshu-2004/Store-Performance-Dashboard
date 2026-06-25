import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from modules.config import ensure_output_dir, get_charts_dir

def branch_month_heatmap(performance_data, output_dir=None):
    if output_dir is None:
        output_dir = ensure_output_dir()
    charts_dir = get_charts_dir()
    branch_monthly_matrix = performance_data.pivot_table(
        index="Branch",
        columns="Month",
        values="Attach_Percentage",
        aggfunc="mean",
        observed=False
    )
    plt.figure(figsize=(10, 6))
    sns.heatmap(branch_monthly_matrix, annot=True, cmap="YlGnBu")
    plt.title("Branch × Month Attach % Heatmap")
    plt.tight_layout()
    plt.savefig(charts_dir / "branch_month_heatmap.png")
    plt.close()
