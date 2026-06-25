# Store-Performance-Dashboard

Sales-performance pipeline for 163 retail stores using attach rate as the KPI. It
forecasts the next month's attach rate with XGBoost (two months of lag plus one-hot
store and branch), segments stores by performance and stability with K-Means, and
renders branch- and month-level charts.

## What's in here

| File | What it does |
|---|---|
| `run_dashboard.py` | Runs everything below in order and prints the holdout metrics. |
| `modules/load_data.py` | Reads the Excel sheet and reshapes it to long format. |
| `modules/train_model.py` | Sorts chronologically, builds two lag features, fits XGBoost, and evaluates a one-step-ahead forecast on a temporal holdout against a persistence baseline. |
| `modules/segmentation.py` | K-Means (`k=4`) on standardised `(mean_attach, volatility)`. |
| `modules/rankings.py` | Sorts stores by mean attach. |
| `modules/{boxplot,distribution,monthly_trend,branch_trend,heatmap,segmentation}.py` | Six charts. |

## Method notes

- The workbook lists months in descending order (Dec..Aug). Rows are sorted by month
  before lagging, so the lags are genuinely past values rather than future ones.
- Evaluation is a temporal holdout (predict the latest observed month), not a random
  split. A random split would put the same store's adjacent months in both train and
  validation and leak its level through the one-hot store columns.
- The model is benchmarked against a persistence baseline (next month = last month).
  On this data XGBoost only marginally beats persistence (RMSE 0.158 vs 0.160). The
  held-out December attach rate averages 0.217, so an error of 0.158 is most of the
  signal: with five months of history and two of them spent on lags, that is the
  honest ceiling, and the small margin over the naive baseline is the real result.
- Predictions are clamped to be non-negative and kept on the same 0-1 fraction scale
  as the ranking and segmentation outputs, so the CSVs can be joined directly.

## Run

```bash
pip install -r requirements.txt
python run_dashboard.py
```

`Jumbo & Company_ Attach % .xls` is committed in the repo root. Outputs land in
`output/charts/` and `output/csv/`.
