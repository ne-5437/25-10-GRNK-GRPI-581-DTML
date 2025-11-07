## PSP Discharge & Power Data Structuring & Analysis

**Date:** 2025-10-29  
**Category:** Data Processing & Validation

### Task Definition
To develop a unified preprocessing pipeline for PSP telemetry that converts raw sensor data into synchronized, structured, and validated datasets — enabling accurate detection of missing values, sampling irregularities, and performance trends across multiple generating units.

### Insights
- Reliable data modeling begins with a standardized temporal structure, ensuring that all physical measurements align in frequency and timestamp precision.
- Null and frequency analyses reveal system reliability — identifying downtime, transmission gaps, or irregular sampling behavior.

### Code Results
- Code1: [d07'06_units_null_cnt.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/b3139f3b758ec429dc8a7ef030590cb8df0bb721/W02-SF650/d07'06_units_null_cnt.py)

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img108.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img109.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img110.png?raw=true)

- Code2: [d07'07_units_null_cnt_sprt.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/b3139f3b758ec429dc8a7ef030590cb8df0bb721/W02-SF650/d07'07_units_null_cnt_sprt.py)

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img111.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img112.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img113.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img114.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img115.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img116.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img117.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img118.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img119.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img120.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img121.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img122.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img123.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img124.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img125.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img126.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img127.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img128.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img129.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img130.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img131.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img132.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img133.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img134.png?raw=true)

- Code3: [d07'08_units_freq_rate.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/b3139f3b758ec429dc8a7ef030590cb8df0bb721/W02-SF650/d07'08_units_freq_rate.py)

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img135.png?raw=true)

- Code4: [d07'09_units_freq_rate_sprt.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/b3139f3b758ec429dc8a7ef030590cb8df0bb721/W02-SF650/d07'09_units_freq_rate_sprt.py)

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img136.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img137.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img138.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img139.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img140.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img141.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img142.png?raw=true)
![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W02-SF650/img143.png?raw=true)

### Issues Faced
- Multiple timestamp formats (pt, dt) caused misalignment during merging.
- Some Parquet files had unreadable schema differences.
- Missing samples created false spikes during resampling.
- Large CSV merges occasionally produced duplicate timestamps.

### Fixes Applied
- Normalized timestamps using fillna() logic between pt and dt.
- Used safe regex-based ID extraction to isolate unit-level data.
- Implemented conditional forward-fill with a time-gap threshold (5 min).
- Removed duplicate index entries after resampling.

### Updated Observations
- Clean data now ensures synchronized timestamps and consistent unit tagging.
- Nulls are concentrated in short bursts, indicating brief sensor interruptions.
- Frequency plots confirm most units operate near 60 samples/min, consistent with expected telemetry rates.

### Conclusion
- The pipeline streamlines PSP data conversion, cleaning, and validation producing synchronized, gap-aware, and reliable datasets that enable deeper time-series and operational performance analysis.


