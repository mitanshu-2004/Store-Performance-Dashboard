import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from modules.config import ensure_output_dir, get_csv_dir


def train_and_predict_xgboost(performance_data, output_dir=None):
    """Predict each store's January attach rate from its two most recent months.

    The source workbook lists months in descending order (Dec..Aug), so the rows
    must be sorted chronologically before lagging; otherwise `shift` builds lags
    from future months and the model learns the wrong direction of time. Evaluation
    uses a temporal holdout (predict the latest observed month) rather than a random
    split, which would leak store identity between train and validation through the
    one-hot store columns.
    """
    if output_dir is None:
        output_dir = ensure_output_dir()
    csv_dir = get_csv_dir()

    model_data = performance_data.copy()
    model_data = model_data.sort_values(['Store_Name', 'Month_Num']).reset_index(drop=True)

    for lag in range(1, 3):
        model_data[f'lag_{lag}'] = (
            model_data.groupby('Store_Name')['Attach_Percentage'].shift(lag)
        )
    model_data = model_data.dropna().reset_index(drop=True)

    features = model_data.drop(['Attach_Percentage', 'Month'], axis=1)
    target = model_data['Attach_Percentage']
    encoded_features = pd.get_dummies(features, columns=['Branch', 'Store_Name'], drop_first=True)

    # Temporal holdout: validate on the latest observed month (a one-step-ahead
    # forecast), train on everything earlier. Every store appears in both, but the
    # validation month is never in the training set, so there is no same-month leak.
    latest_month = model_data['Month_Num'].max()
    val_mask = (model_data['Month_Num'] == latest_month).to_numpy()
    train_mask = ~val_mask

    model = _make_model()
    model.fit(encoded_features[train_mask], target[train_mask])
    val_pred = np.clip(model.predict(encoded_features[val_mask]), 0, None)
    rmse = float(np.sqrt(mean_squared_error(target[val_mask], val_pred)))

    # Persistence baseline: predict the validation month as the previous month
    # (lag_1). A forecasting model is only worth keeping if it beats this.
    persistence_pred = model_data.loc[val_mask, 'lag_1'].to_numpy()
    baseline_rmse = float(np.sqrt(mean_squared_error(target[val_mask], persistence_pred)))
    metrics = {'rmse': rmse, 'persistence_rmse': baseline_rmse}

    # Retrain on all observed rows for the actual January forecast.
    final_model = _make_model()
    final_model.fit(encoded_features, target)

    keys, encoded_january = _build_january_input(performance_data, encoded_features.columns)
    january_predictions = np.clip(final_model.predict(encoded_january), 0, None)

    results = keys.copy()
    # Kept on the same 0-1 fraction scale as the rankings and segmentation outputs,
    # so the prediction CSV can be joined to them directly.
    results['Jan_Prediction_XGBoost'] = january_predictions
    results.to_csv(csv_dir / 'january_predictions_xgboost.csv', index=False)

    return metrics, results


def _make_model():
    return xgb.XGBRegressor(
        objective='reg:squarederror',
        n_estimators=100,
        learning_rate=0.1,
        random_state=42,
    )


def _build_january_input(performance_data, training_columns):
    """Assemble the January feature row for every store.

    lag_1 is December, lag_2 is November, the same chronological convention the
    model is trained on. Missing months fall back to the store's own average rather
    than zero, which would otherwise push that store to a floor prediction.
    """
    december = performance_data[performance_data['Month'] == 'Dec'].set_index('Store_Name')
    november = performance_data[performance_data['Month'] == 'Nov'].set_index('Store_Name')
    store_means = performance_data.groupby('Store_Name')['Attach_Percentage'].mean()

    january = performance_data[['Store_Name', 'Branch']].drop_duplicates().reset_index(drop=True)
    # One month past the last observed month, derived from the data rather than
    # hard-coded, so the forecast horizon tracks whatever months are present.
    january['Month_Num'] = int(performance_data['Month_Num'].max()) + 1
    january['lag_1'] = january['Store_Name'].map(december['Attach_Percentage'])
    january['lag_2'] = january['Store_Name'].map(november['Attach_Percentage'])
    for col in ['lag_1', 'lag_2']:
        january[col] = january[col].fillna(january['Store_Name'].map(store_means))
    january = january.fillna(0)  # only reached if a store has no data in any month

    encoded = pd.get_dummies(january, columns=['Branch', 'Store_Name'], drop_first=True)
    for col in set(training_columns) - set(encoded.columns):
        encoded[col] = 0
    encoded = encoded[training_columns]

    return january[['Store_Name', 'Branch']], encoded
