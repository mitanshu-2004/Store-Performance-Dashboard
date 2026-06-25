"""Tests for the workbook loader. Run with: pytest"""
import os
import sys

import pandas as pd
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.load_data import load_and_preprocess_data


def _write_workbook(tmp_path, columns, rows):
    df = pd.DataFrame(rows, columns=columns)
    path = tmp_path / "wb.xlsx"
    df.to_excel(path, index=False)
    return path


def test_months_ordered_chronologically_regardless_of_column_order(tmp_path):
    # Columns deliberately out of order (and descending, like the real file).
    path = _write_workbook(
        tmp_path,
        ["Branch", "Store_Name", "Dec", "Nov", "Oct", "Sep", "Aug"],
        [["B", "S1", 0.5, 0.4, 0.3, 0.2, 0.1]],
    )
    _, perf = load_and_preprocess_data(path)
    order = (
        perf.drop_duplicates("Month")
        .sort_values("Month_Num")["Month"].astype(str).tolist()
    )
    assert order == ["Aug", "Sep", "Oct", "Nov", "Dec"]
    # Month_Num increases with calendar time, not column position.
    aug = perf[perf["Month"] == "Aug"]["Month_Num"].iloc[0]
    dec = perf[perf["Month"] == "Dec"]["Month_Num"].iloc[0]
    assert aug == 0 and dec == 4


def test_works_with_a_different_month_subset(tmp_path):
    path = _write_workbook(
        tmp_path,
        ["Branch", "Store_Name", "Mar", "Jan", "Feb"],
        [["B", "S1", 0.3, 0.1, 0.2]],
    )
    _, perf = load_and_preprocess_data(path)
    order = (
        perf.drop_duplicates("Month")
        .sort_values("Month_Num")["Month"].astype(str).tolist()
    )
    assert order == ["Jan", "Feb", "Mar"]


def test_missing_identifier_column_raises(tmp_path):
    path = _write_workbook(tmp_path, ["Store_Name", "Aug"], [["S1", 0.1]])
    with pytest.raises(ValueError, match="identifier"):
        load_and_preprocess_data(path)


def test_unrecognised_month_column_raises(tmp_path):
    path = _write_workbook(
        tmp_path, ["Branch", "Store_Name", "Augustus"], [["B", "S1", 0.1]]
    )
    with pytest.raises(ValueError, match="Unrecognised"):
        load_and_preprocess_data(path)
