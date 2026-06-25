import pandas as pd
from modules.config import DATA_FILE

ID_COLUMNS = ["Branch", "Store_Name"]
MONTH_ORDER = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def load_and_preprocess_data(file_path=None):
    """Read the wide attach-rate workbook and reshape it to long format.

    The month columns are detected from the sheet and ordered chronologically
    rather than assuming a fixed Aug..Dec layout, so any subset or ordering of
    months works. Month_Num is the chronological position among the months that
    are actually present (0-based).
    """
    if file_path is None:
        file_path = DATA_FILE
    raw_data = pd.read_excel(file_path)

    missing_ids = [c for c in ID_COLUMNS if c not in raw_data.columns]
    if missing_ids:
        raise ValueError(
            f"Workbook is missing required identifier column(s): {missing_ids}. "
            f"Found columns: {list(raw_data.columns)}"
        )

    month_columns = [c for c in raw_data.columns if c not in ID_COLUMNS]
    unknown = [c for c in month_columns if str(c) not in MONTH_ORDER]
    if unknown:
        raise ValueError(
            f"Unrecognised month column(s): {unknown}. Expected three-letter month "
            f"names from {MONTH_ORDER}."
        )
    if not month_columns:
        raise ValueError("No month columns found in the workbook.")

    present_order = [m for m in MONTH_ORDER if m in month_columns]

    performance_data = raw_data.melt(
        id_vars=ID_COLUMNS,
        value_vars=month_columns,
        var_name="Month",
        value_name="Attach_Percentage",
    )
    performance_data["Month"] = pd.Categorical(
        performance_data["Month"], categories=present_order, ordered=True
    )
    performance_data["Month_Num"] = performance_data["Month"].cat.codes
    return raw_data, performance_data
