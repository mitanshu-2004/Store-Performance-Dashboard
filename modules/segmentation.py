import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from pathlib import Path
from modules.config import ensure_output_dir, get_charts_dir, get_csv_dir

def store_segmentation(performance_data, num_clusters=4, output_dir=None):
    if output_dir is None:
        output_dir = ensure_output_dir()
    charts_dir = get_charts_dir()
    csv_dir = get_csv_dir()
    store_metrics = performance_data.pivot_table(
        index="Store_Name",
        columns="Month",
        values="Attach_Percentage",
        observed=False
    ).fillna(0)
    store_metrics["Average_Attach"] = store_metrics.mean(axis=1)
    store_metrics["Volatility"] = store_metrics.std(axis=1)
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    store_metrics["Cluster"] = kmeans.fit_predict(store_metrics[["Average_Attach", "Volatility"]])
    store_metrics.to_csv(csv_dir / "store_segmentation_results.csv")
    plt.figure(figsize=(12, 8))
    sns.scatterplot(
        data=store_metrics,
        x="Average_Attach",
        y="Volatility",
        hue="Cluster",
        s=120,
        palette="Set2"
    )
    plt.title("Store Segmentation (Performance vs Volatility)")
    plt.tight_layout()
    plt.savefig(charts_dir / "segmentation_scatter.png")
    plt.close()
    return store_metrics
