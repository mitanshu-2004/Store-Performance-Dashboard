# Store Performance Report

## What it is

This project looks at how well stores are doing. It uses a number called "Attach Percentage" to measure this. The project uses data from an Excel file to see patterns, guess future performance, and make charts and reports. The main idea is to use data to understand and help improve how stores are doing.

The report does these things:

*   **Gets Data Ready:** Reads the store data from the Excel file and prepares it for review.
*   **Guesses Future Performance:** Uses a tool called XGBoost to guess the "Attach Percentage" for each store in the future.
*   **Makes Charts:** Creates charts to show how stores are doing. This includes:
    *   A boxplot to compare different branches.
    *   A histogram to show how the "Attach Percentage" is spread out each month.
    *   Line charts to show how performance has changed over time.
    *   A heatmap to show performance by branch and month.
*   **Groups Stores:** Puts stores into groups based on how well they are doing using K-Means.
*   **Ranks Stores:** Makes a list of stores from best to worst based on their average "Attach Percentage."

## Tools Used

*   **Python:** The main programming language used.
*   **Pandas:** To work with the data.
*   **Scikit-learn:** To help get the data ready for the model.
*   **XGBoost:** To make the model that guesses future performance.
*   **Matplotlib & Seaborn:** To make the charts.

## Project Files

```
Store-Performance-Dashboard/
├── Jumbo & Company_ Attach % .xls      # The data file
├── README.md                           # This file
├── run_dashboard.py                    # The main script to run everything
├── modules/
│   ├── boxplot.py                      # Makes the branch boxplots
│   ├── branch_trend.py                 # Makes the monthly trend by branch chart
│   ├── config.py                       # Handles file paths
│   ├── distribution.py                 # Makes the distribution plots
│   ├── heatmap.py                      # Makes the branch-month heatmap
│   ├── load_data.py                    # Loads and prepares data
│   ├── monthly_trend.py                # Makes the overall monthly trend chart
│   ├── rankings.py                     # Makes the store rankings
│   ├── segmentation.py                 # Groups the stores
│   └── train_model.py                  # Trains the model and makes guesses
└── output/
    ├── charts/                         # Where the charts are saved
    │   ├── attach_distribution_all_months.png
    │   ├── branch_boxplot.png
    │   ├── branch_month_heatmap.png
    │   ├── monthly_trend_by_branch.png
    │   ├── monthly_trend_overall.png
    │   └── segmentation_scatter.png
    └── csv/                            # Where the reports are saved
        ├── january_predictions_xgboost.csv
        ├── store_rankings.csv
        └── store_segmentation_results.csv
```

## How to Get Started

1.  **Copy the project:**
    ```bash
    git clone https://github.com/your-username/Store-Performance-Dashboard.git
    cd Store-Performance-Dashboard
    ```

2.  **Set up a work area (a good idea):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Add the needed tools:**
    ```bash
    pip install pandas scikit-learn xgboost matplotlib seaborn
    ```

## How to Run It

To run the report and make all the charts and reports, run this command in the main project folder:

```bash
python run_dashboard.py
```

This will read the data, train the model, and save all the charts and reports in the `output` folder.

## The Modules

### `run_dashboard.py`

This is the main script. It runs all the other parts of the project in the right order.

### `modules/`

*   **`config.py`**: Keeps track of where files are and makes the output folders.
*   **`load_data.py`**: Reads the data from the Excel file and gets it ready.
*   **`train_model.py`**:
    *   Prepares the data for the XGBoost model.
    *   Splits the data for training and testing.
    *   Trains the model.
    *   Guesses the "Attach Percentage" for the next month.
    *   Saves the guesses to a CSV file.
*   **`boxplot.py`**: Makes a boxplot chart to show how "Attach Percentage" is spread out for each branch.
*   **`distribution.py`**: Makes charts to show the spread of "Attach Percentage" for each month.
*   **`monthly_trend.py`**: Makes a chart to show the average "Attach Percentage" for all stores over time.
*   **`branch_trend.py`**: Makes a chart to show the "Attach Percentage" for each branch over time.
*   **`heatmap.py`**: Makes a heatmap to show the average "Attach Percentage" for each branch and month.
*   **`rankings.py`**: Ranks the stores from best to worst and saves the list.
*   **`segmentation.py`**: Groups the stores using K-Means.

## Store Grouping with K-Means

The K-Means tool is used to put stores into groups based on how well they do and how steady their performance is. Here is how it works:

1.  **Two Numbers are Made:** For each store, two numbers are figured out:
    *   **Average Attach %:** The average "Attach Percentage" for a store over all months. This shows how well the store is doing overall.
    *   **Volatility:** This shows if a store's "Attach Percentage" changes a lot or stays about the same.

2.  **Grouping:** The K-Means tool uses these two numbers to make 4 groups of stores. Each group has stores that are like each other in performance and steadiness.

3.  **Output:** The group for each store is saved in a CSV file. A chart is also made to show the groups.

## The Output Files

The project makes these files in the `output` folder:

### Charts (`output/charts/`)

*   **`attach_distribution_all_months.png`**: Shows how the "Attach Percentage" is spread out each month.
*   **`branch_boxplot.png`**: A chart to compare the "Attach Percentage" for each branch.
*   **`branch_month_heatmap.png`**: A heatmap to show how each branch did each month.
*   **`monthly_trend_by_branch.png`**: A line chart to show how each branch's performance has changed.
*   **`monthly_trend_overall.png`**: A line chart to show the overall performance of all stores.
*   **`segmentation_scatter.png`**: A chart to show the groups of stores.

### Reports (`output/csv/`)

*   **`january_predictions_xgboost.csv`**: Has the guessed "Attach Percentage" for the next month.
*   **`store_rankings.csv`**: A list of stores from best to worst.
*   **`store_segmentation_results.csv`**: Has the results of the store grouping.
