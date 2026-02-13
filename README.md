# Retail Performance Analysis

This project looks at the sales performance of different store branches. It uses data from an Excel file to find patterns, make predictions, and create charts. The main metric is "Attach Percentage," which is the rate at which a secondary product is sold along with a primary product.

## What I Used

*   **Python:** The main language for the project.
*   **Pandas:** To read and work with the data.
*   **Scikit-learn:** To get the data ready for the model.
*   **XGBoost:** To create a model that predicts future performance.
*   **Matplotlib & Seaborn:** To make the charts.

## The Input

The project uses an Excel file named `Jumbo & Company_ Attach % .xls`. This file has information about different stores, their branches, and their "Attach Percentage" over several months. This percentage shows how often a related item is sold with a main product.

## What the Project Does

The main script, `run_dashboard.py`, does the following:

1.  **Loads Data:** It reads the Excel file and gets it ready for analysis.
2.  **Predicts Performance:** It uses a machine learning model (XGBoost) to guess how well stores will do in the future.
3.  **Makes Charts:** It creates different charts to show the data in a visual way. These charts include:
    *   A boxplot to compare branches.
    *   A distribution plot to see how performance is spread out.
    *   Trend lines to see how performance changes over time.
    *   A heatmap to show performance by branch and month.
    *   A scatter plot to group stores into different segments.
4.  **Ranks Stores:** It creates a list of stores from best to worst.
5.  **Groups Stores:** It groups stores together based on their performance.

## The Output

The project creates two types of output files in the `output` directory:

*   **Charts:** PNG images of the different plots.
*   **CSVs:**
    *   `january_predictions_xgboost.csv`: The predictions from the model.
    *   `store_rankings.csv`: The ranked list of stores.
    *   `store_segmentation_results.csv`: The store groupings.

This project shows how to use data to understand and predict business performance.
