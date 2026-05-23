# Store-Performance-Dashboard

Sales-performance pipeline for 163 retail stores using Attach % as the KPI. Forecasts next month's attach with XGBoost (two months of lag plus one-hot store and branch), tags stores by performance × stability via K-Means, and produces a handful of branch- and month-level charts.

The source workbook is proprietary client data and isn't in the repo, so the script won't run end-to-end on a clean checkout. If you have a similar wide-format Excel sheet (`Store | Branch | YYYY_MM | YYYY_MM | …`), drop it in and adjust `modules/load_data.py` to match the column layout.

## What's in here

| File | What it does |
|---|---|
| `run_dashboard.py` | Runs everything below in order. |
| `modules/load_data.py` | Reads the Excel sheet, reshapes to long format. |
| `modules/train_model.py` | XGBoost regressor with 20% holdout. Prints RMSE — not hard-coded as a claim in this README, so the number you see is the number the run produced. |
| `modules/segmentation.py` | K-Means with `k=4` on `(mean_attach_pct, std_attach_pct)`. Labels are descriptive (performance × stability), not causal. |
| `modules/rankings.py` | Sorts stores by mean attach (163 rows). |
| `modules/boxplot.py · distribution.py · monthly_trend.py · branch_trend.py · heatmap.py` | The five charts. |

Five months of data per store is thin — two lag features keep XGBoost from over-fitting, but anything fancier (LSTM, Prophet) would be silly at this length. If the data grows, the obvious next steps are price/promotion/headcount covariates and reporting MAPE alongside RMSE so the error scales with each store's baseline volume.

## Run

```bash
pip install pandas scikit-learn xgboost matplotlib seaborn openpyxl
python run_dashboard.py
```

Outputs land in `output/charts/` and `output/csv/`. RMSE goes to stdout.
