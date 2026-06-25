import pandas as pd
from pathlib import Path
from modules.config import ensure_output_dir, get_csv_dir

def generate_rankings(performance_data, output_dir=None):
    if output_dir is None:
        output_dir = ensure_output_dir()
    csv_dir = get_csv_dir()
    store_rankings = (
        performance_data.groupby("Store_Name")["Attach_Percentage"]
        .mean()
        .sort_values(ascending=False)
    )
    store_rankings.to_csv(csv_dir / "store_rankings.csv")
    return store_rankings
