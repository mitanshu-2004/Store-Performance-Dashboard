import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from modules.config import ensure_output_dir, get_charts_dir

def overall_monthly_trend(performance_data, output_dir=None):
    if output_dir is None:
        output_dir = ensure_output_dir()
    charts_dir = get_charts_dir()
    average_by_month = performance_data.groupby("Month", observed=False)["Attach_Percentage"].mean()
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=average_by_month, marker="o")
    plt.title("Average Attach % Across Months")
    plt.savefig(charts_dir / "monthly_trend_overall.png")
    plt.close()
