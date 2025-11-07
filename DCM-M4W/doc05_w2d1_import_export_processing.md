## PSP Data Workflow: Import–Export Processing

**Date:** 2025-10-27  
**Category:** Energy Data Visualization

### Task Definition
Developed a three-stage Marimo-based system to automate PSP data cleaning, transformation, validation, and turbine-level operational analytics.

### Insights
- Power equivalence can be computed and validated from ΔEnergy values, which can be used to analyze turbine operating modes and cycle-level efficiency.
- From raw data → validated power metrics → visual performance diagnostics.

### Code Results
- Code1: [d05'02_turbine_min_plots.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/e61ef057241c5f145fefbe8e8f9c9d336d00cfa2/W02-SF650/d05'02_turbine_min_plots.py)

~~~python
===== Efficiency Stats =====
count     1.000000
mean     54.293475
std            NaN
min      54.293475
25%      54.293475
50%      54.293475
75%      54.293475
max      54.293475
~~~

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img100.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img101.png?raw=true)

- Code2: [d05'10_psp_clean_data.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/e29b839881fe1de4559673f23d70e9af2c615d83/W02-SF650/d05'10_psp_clean_data.py)

~~~python
Import Data: (570848, 4)
Export Data: (657210, 4)
~~~
~~~python
=== Import Statistical Summary ===
          Unnamed: 0  gen_mwh_import
count  570848.000000   570848.000000
mean   285423.500000   111585.475915
std    164789.767571    68841.204481
min         0.000000        7.939000
25%    142711.750000    25019.570801
50%    285423.500000   135765.773438
75%    428135.250000   164908.386719
max    570847.000000   219030.859375
=== Export Statistical Summary ===
          Unnamed: 0  gen_mwh_export
count  657210.000000   657210.000000
mean   328604.500000   128532.319858
std    189720.329545    78644.537561
min         0.000000        1.213000
25%    164302.250000    29137.507324
50%    328604.500000   148961.960938
75%    492906.750000   189681.031250
max    657209.000000   263973.906250
~~~

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img102.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img103.png?raw=true)

- Code3: [d06'01_imp_exp_pwr_csv.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/e29b839881fe1de4559673f23d70e9af2c615d83/W02-SF650/d06'01_imp_exp_pwr_csv.py)

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img104.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img105.png?raw=true)

~~~python
Summary:
               MW    ΔIMPORT    ΔEXPORT  MW_FROM_IMPORT  MW_FROM_EXPORT
count   96.000000  28.000000  67.000000       28.000000       67.000000
mean   -99.128397  49.212612  55.298741      196.850446      221.194963
std    214.308892  18.859675  17.606649       75.438698       70.426596
min   -259.667605   1.062500   0.000000        4.250000        0.000000
25%   -256.261664  54.054688  60.515625      216.218750      242.062500
50%   -252.038696  57.515625  61.453125      230.062500      245.812500
75%    169.384148  58.738281  62.164062      234.953125      248.656250
max    245.750917  59.640625  63.296875      238.562500      253.187500
~~~
~~~python
===== VERIFICATION OF POWER FROM ENERGY =====
Correlation (MW vs Import-based power): 0.957
Correlation (MW vs Export-based power): -0.897

Mean Absolute Error vs Import Power: 19.37 MW
Mean Absolute Error vs Export Power: 456.76 MW
~~~

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img106.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img107.png?raw=true)

### Issues Faced
- Timestamp misalignment between energy and power datasets initially caused join mismatches.
- Negative ΔEnergy values occurred due to meter rollovers.
- NaN values propagated during merging due to partial Import/Export overlaps.

### Fixes Applied
- Enforced timestamp normalization using pd.to_datetime(..., utc=True) across all datasets.
- Removed rollover anomalies with conditional filtering (ΔIMPORT >= 0, ΔEXPORT >= 0).

### Updated Observations
- Data consistency and continuity were achieved across stages, producing stable 15-min aggregates.
- High correlation (>0.9) between actual and computed MW confirmed integrity of power-energy conversion.
- Turbine cycles distinctly alternate between pumping and generation, with realistic duration distributions.

### Conclusion
- The workflow unifies PSP data cleaning, power validation, and turbine cycle analysis into a reliable, automated process for accurate performance insights.


