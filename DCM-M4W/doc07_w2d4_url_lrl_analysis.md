## PSP Reservoir Level Monitoring

**Date:** 2025-10-30  
**Category:** Data Processing & Validation

### Task Definition
To process and analyze one month of PSP Parquet data to monitor upper and lower reservoir head levels, detect data quality issues (nulls, outliers, sensor drift), and determine the most reliable sensors through statistical visualization and comparison of raw vs cleaned distributions.

### Insights
- Multi-sensor monitoring requires data harmonization and statistical filtering to ensure accurate reservoir head tracking.
- Outlier and null analysis play a critical role in identifying faulty or drifting sensors before modeling water-level behavior.
- Kernel density and frequency comparisons provide a quantitative measure of sensor reliability and post-cleaning data integrity.

### Code Results
- Code1: [d08'06_url_12_null_outlr_opr.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/c3584fdda705217ec21f4aa218caa877de8af211/W02-SF650/d08'06_url_12_null_outlr_opr.py)

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img144.png?raw=true)

~~~python
Monitor1: 33 (3σ), 0 (5σ) outliers
Monitor2: 0 (3σ), 0 (5σ) outliers
~~~

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img145.png?raw=true)

~~~python
Null % — M1: 0.00% | M2: 42.11%
~~~

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img146.png?raw=true)

~~~python
Average Sampling Interval: 88.54 seconds
~~~

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img147.png?raw=true)

~~~python
M1 Violations: 295 | M2 Violations: 330
~~~

- Code2: [d08'07_url_12_distr_lvl.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/cc2d9f8e512d416679a7ef1e01f845450175e184/W02-SF650/d08'07_url_12_distr_lvl.py)


![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img148.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img149.png?raw=true)

- Code3: [d08'08_url_02_freq_plot.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/cc2d9f8e512d416679a7ef1e01f845450175e184/W02-SF650/d08'08_url_02_freq_plot.py)

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img150.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img151.png?raw=true)

~~~python
Total samples: 11759 | Out-of-range: 119 samples
~~~

- Code4: [d08'09_url_02_cln_plot.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/cc2d9f8e512d416679a7ef1e01f845450175e184/W02-SF650/d08'09_url_02_cln_plot.py)

~~~python
count    12214.000000
mean       453.823260
std          3.813411
min        445.325623
25%        450.474808
50%        453.664307
75%        457.191871
max        461.147675
~~~

- Code5: [d08'10_url_02_freq_plot_cln.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/cc2d9f8e512d416679a7ef1e01f845450175e184/W02-SF650/d08'10_url_02_freq_plot_cln.py)

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img152.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img153.png?raw=true)

~~~python
Total samples: 12214
Out-of-range samples: 119 (Below: 111, Above: 8)
~~~

- Code6: [d08'12_url_kde_combined.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/cc2d9f8e512d416679a7ef1e01f845450175e184/W02-SF650/d08'12_url_kde_combined.py)

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img154.png?raw=true)

- Code7: [d08'13_lrl_12_null_outlr_opr.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/cc2d9f8e512d416679a7ef1e01f845450175e184/W02-SF650/d08'13_lrl_12_null_outlr_opr.py)

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img155.png?raw=true)

~~~python
Monitor1: 0 (3σ), 0 (5σ) outliers
Monitor2: 0 (3σ), 0 (5σ) outliers
~~~

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img156.png?raw=true)

~~~python
Null % — M1: 0.00% | M2: 24.76%
~~~

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img157.png?raw=true)

~~~python
Average Sampling Interval: 129.79 seconds
~~~

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img158.png?raw=true)

~~~python
M1 Violations: 89 | M2 Violations: 49
~~~

- Code8: [d08'14_lrl_12_distr_lvl.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/cc2d9f8e512d416679a7ef1e01f845450175e184/W02-SF650/d08'14_lrl_12_distr_lvl.py)


![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img159.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img160.png?raw=true)

- Code9: [d08'15_lrl_12_freq_plot.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/cc2d9f8e512d416679a7ef1e01f845450175e184/W02-SF650/d08'15_lrl_12_freq_plot.py)

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img161.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img162.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img163.png?raw=true)

~~~python
Monitor1 — Total samples: 19970 | Out-of-range: 89 samples
Monitor2 — Total samples: 20730 | Out-of-range: 278 samples
~~~

- Code10: [d08'16_lrl_01_freq_plot.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/cc2d9f8e512d416679a7ef1e01f845450175e184/W02-SF650/d08'16_lrl_01_freq_plot.py)

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img164.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img165.png?raw=true)

~~~python
Total samples: 19970 | Out-of-range: 89 samples
~~~

- Code11: [d08'17_lrl_01_freq_plot_cln.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/cc2d9f8e512d416679a7ef1e01f845450175e184/W02-SF650/d08'17_lrl_01_freq_plot_cln.py)

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img166.png?raw=true)

~~~python
Total samples: 19975 | Out-of-range: 87 samples
~~~

- Code12: [d08'19_lrl_kde_combined.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/cc2d9f8e512d416679a7ef1e01f845450175e184/W02-SF650/d08'19_lrl_kde_combined.py)

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img167.png?raw=true)
### Issues Faced
- Sensor overlap produced partial null segments in both head level series.
- 3σ outliers caused false spikes in trend visualization.
- Frequency inconsistencies between monitors introduced alignment errors during comparison.

### Fixes Applied
- Used combined sensor averaging to stabilize noisy data.
- Removed high-deviation samples beyond statistical thresholds.
- Applied consistent time alignment across all monitors before merging.

### Updated Observations
- Post-cleaning frequency plots exhibit stable and continuous data flow.
- KDE curves confirm balanced data distribution and improved operational range uniformity.
- Selected monitors reflect consistent head-level response matching expected PSP operations.

### Conclusion
- The analysis efficiently converted, cleaned, and validated one month of PSP Parquet data — identifying reliable sensors (Upper: Monitor 2, Lower: Monitor 1), removing anomalies, and confirming data stability through statistical and frequency-based evaluation.


