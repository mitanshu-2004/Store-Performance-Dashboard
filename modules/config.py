import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR
OUTPUT_DIR = BASE_DIR / "output"
CHARTS_DIR = OUTPUT_DIR / "charts"
CSV_DIR = OUTPUT_DIR / "csv"
DATA_FILE = DATA_DIR / "Jumbo & Company_ Attach % .xls"

def ensure_output_dir():
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR

def get_charts_dir():
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    return CHARTS_DIR

def get_csv_dir():
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    return CSV_DIR
