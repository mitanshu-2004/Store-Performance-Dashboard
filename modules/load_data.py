import pandas as pd
from modules.config import DATA_FILE

def load_and_preprocess_data(file_path=None):
    if file_path is None:
        file_path = DATA_FILE
    raw_data = pd.read_excel(file_path)
    performance_data = raw_data.melt(
        id_vars=['Branch', 'Store_Name'],
        var_name='Month',
        value_name='Attach_Percentage'
    )
    month_order = ['Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    performance_data['Month'] = pd.Categorical(
        performance_data['Month'],
        categories=month_order,
        ordered=True
    )
    performance_data['Month_Num'] = performance_data['Month'].cat.codes
    return raw_data, performance_data
