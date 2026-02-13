import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from pathlib import Path
from modules.config import ensure_output_dir, get_csv_dir

def train_and_predict_xgboost(performance_data, output_dir=None):
    if output_dir is None:
        output_dir = ensure_output_dir()
    csv_dir = get_csv_dir()
    model_data = performance_data.copy()
    for lag in range(1, 3):
        model_data[f'lag_{lag}'] = model_data.groupby('Store_Name')['Attach_Percentage'].shift(lag)
    model_data = model_data.dropna().reset_index(drop=True)
    features = model_data.drop(['Attach_Percentage', 'Month'], axis=1)
    target = model_data['Attach_Percentage']
    encoded_features = pd.get_dummies(features, columns=['Branch', 'Store_Name'], drop_first=True)
    december_data = performance_data[performance_data['Month'] == 'Dec'].set_index('Store_Name')
    november_data = performance_data[performance_data['Month'] == 'Nov'].set_index('Store_Name')
    january_input = performance_data[['Store_Name', 'Branch']].drop_duplicates().reset_index(drop=True)
    january_input['Month_Num'] = 5
    january_input['lag_1'] = january_input['Store_Name'].map(december_data['Attach_Percentage'])
    january_input['lag_2'] = january_input['Store_Name'].map(november_data['Attach_Percentage'])
    january_input = january_input.fillna(0)
    encoded_january = pd.get_dummies(january_input, columns=['Branch', 'Store_Name'], drop_first=True)
    training_columns = encoded_features.columns
    missing_columns = set(training_columns) - set(encoded_january.columns)
    for col in missing_columns:
        encoded_january[col] = 0
    encoded_january = encoded_january[training_columns]
    X_train, X_val, y_train, y_val = train_test_split(
        encoded_features,
        target,
        test_size=0.2,
        random_state=42
    )
    model = xgb.XGBRegressor(
        objective='reg:squarederror',
        n_estimators=100,
        learning_rate=0.1,
        random_state=42
    )
    model.fit(X_train, y_train)
    rmse = np.sqrt(mean_squared_error(y_val, model.predict(X_val)))
    final_model = xgb.XGBRegressor(
        objective='reg:squarederror',
        n_estimators=100,
        learning_rate=0.1,
        random_state=42
    )
    final_model.fit(encoded_features, target)
    january_predictions = final_model.predict(encoded_january)
    results = january_input[['Store_Name', 'Branch']].copy()
    results['Jan_Prediction_XGBoost'] = january_predictions*100
    output_path = csv_dir / 'january_predictions_xgboost.csv'
    results.to_csv(output_path, index=False)
    return rmse, results
