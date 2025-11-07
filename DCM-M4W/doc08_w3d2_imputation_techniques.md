## Imputation & Smoothing Comparison for Missing Data

**Date:** 2025-11-05  
**Category:** Data Preprocessing

### 🔍 Insights
- **Mean/Median Imputation**: Replace missing values with a central statistic. Best for stable distributions.
- **Forward/Backward Fill**: Use adjacent known values. Ideal for time-series continuity.
- **Linear Interpolation**: Estimate missing values using straight-line trends between known points.
- **Exponential Smoothing**: Apply weighted averages with decay. Useful for forecasting and trend-aware filling.

### 🧪 Task Definition
Developed an interactive Marimo-based tool to visualize and compare six imputation and smoothing techniques on uploaded CSV data. The dashboard lets users select a column and apply any method to observe how each approach affects data continuity and trend behavior.

### 📎 Code Results
- Code1: [d11'01_imputation_techq.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/bbe046a1a01a082354848c917e5f4022691566b2/W03-SF408/d11'01_imputation_techq.py)

- The Dropdown Widget:

| Index | Input   | Mean Imputation | Median Imputation | Forward Fill | Backward Fill | Linear Interpolation | Exponential Smoothing |
|-------|---------|------------------|--------------------|--------------|----------------|------------------------|------------------------|
| 0     | 10      | 10               | 10                 | 10           | 10             | 10                     | 10                     |
| 1     |         | 14.5             | 14.5               | 10           | 12             | 11                     |                        |
| 2     | 12      | 12               | 12                 | 12           | 12             | 12                     | 10                     |
| 3     |         | 14.5             | 14.5               | 12           | 14             | 13                     |                        |
| 4     | 14      | 14               | 14                 | 14           | 14             | 14                     | 10.4                   |
| 5     | 15      | 15               | 15                 | 15           | 15             | 15                     | 11.12                  |
| 6     |         | 14.5             | 14.5               | 15           | 17             | 16                     |                        |
| 7     | 17      | 17               | 17                 | 17           | 17             | 17                     | 11.896                 |
| 8     |         | 14.5             | 14.5               | 17           | 19             | 18                     |                        |
| 9     | 19      | 19               | 19                 | 19           | 19             | 19                     | 12.9168                |


- Code2: [d12'01_imputation_techq_csv_up.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/bbe046a1a01a082354848c917e5f4022691566b2/W03-SF408/d12'01_imputation_techq_csv_up.py)

- Uploaded Xminutal6.csv
- ![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W03-SF408/img200.png?raw=true)
- Automatically takes the drop-down inout of selected technique
- ![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W03-SF408/img201.png?raw=true)
- Then the column selection is done based on provided csv file columns
- ![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W03-SF408/img202.png?raw=true)
- Finally the output is displayed comparing the data before & after the technique being applied
- ![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W03-SF408/img203.png?raw=true)

### 🐞 Issues Faced
- Initially, Marimo raised multiple RuntimeError and AttributeError exceptions due to UI .value access restrictions and version differences.
- Older Marimo builds lacked @mo.reactive, mo.display, and minimum/maximum arguments, requiring us to refactor logic into multiple reactive-safe cells.

### ✅ Fixes Applied
- Used pandas `.fillna()`, `.interpolate()`, and `SimpleExpSmoothing()` from `statsmodels` to apply each method.
- Uploader + dropdowns in early cells, column selector in a later cell, and method application in the final one.
- We replaced deprecated calls (fillna(method=...)) with ffill()/bfill(), removed unsafe .value access, and used safe return-based rendering instead of reactive decorators.

### 🔁 Updated Observations
- **Mean/Median**: Fast, but statistically rigid.
- **Forward/Backward Fill**: Good for continuity, poor for trend.
- **Linear Interpolation**: Balanced and intuitive for gradual changes.
- **Exponential Smoothing**: Best for forecasting, but needs warm-up history.

### 🏷️ Conclusion
Each technique serves a distinct purpose. For time-series analytics, interpolation and smoothing offer better trend fidelity. For static datasets, mean/median imputation is efficient. The choice depends on data type, missingness pattern, and downstream task sensitivity.
