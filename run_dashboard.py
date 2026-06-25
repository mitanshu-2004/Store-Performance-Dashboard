from modules.config import ensure_output_dir
from modules.load_data import load_and_preprocess_data
from modules.train_model import train_and_predict_xgboost
from modules.boxplot import branch_boxplot
from modules.distribution import store_distribution
from modules.monthly_trend import overall_monthly_trend
from modules.branch_trend import branch_monthly_trend
from modules.heatmap import branch_month_heatmap
from modules.rankings import generate_rankings
from modules.segmentation import store_segmentation

def main():
    output_dir = ensure_output_dir()
    _, performance_data = load_and_preprocess_data()
    metrics, predictions = train_and_predict_xgboost(performance_data, output_dir)
    print(f"January forecast (temporal holdout on the latest month):")
    print(f"  XGBoost RMSE     = {metrics['rmse']:.4f}")
    print(f"  Persistence RMSE = {metrics['persistence_rmse']:.4f} "
          f"(predict next month = last month)")
    print(f"  target mean      = {performance_data['Attach_Percentage'].mean():.4f}")
    branch_boxplot(performance_data, output_dir)
    store_distribution(performance_data, predictions, output_dir)
    overall_monthly_trend(performance_data, output_dir)
    branch_monthly_trend(performance_data, output_dir)
    branch_month_heatmap(performance_data, output_dir)
    generate_rankings(performance_data, output_dir)
    store_segmentation(performance_data, output_dir=output_dir)

if __name__ == "__main__":
    main()
