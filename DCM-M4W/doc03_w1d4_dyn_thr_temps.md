## Dynamic Thresholds for Bearing Temperature Anomaly Detection

**Date:** 2025-10-24  
**Category:** Task

### Task Definition
To analyze the "Bearing D.E. Temperature" for device "G97-N24" during April 2024 and to implement and compare different statistical methods to set three distinct operating thresholds.

### Insights
- Percentiles: Using percentile cutoffs (e.g., 75th, 90th, 98th) on the dataset.
- Standard Deviation: Using the "Empirical Rule" (Mean $\pm$ k·Std Dev), such as $\mu+\sigma$, $\mu+2\sigma$, and $\mu+3\sigma$, to define the zones.
- By analyzing historical sensor data, we can statistically define what constitutes normal behavior. This allows the system to automatically flag early-stage anomalies ("Warnings") before they escalate into critical failures ("Alarms"), enabling proactive maintenance.

### Code Results
- Code1: [d04'01_temp_thrsd_pct0.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/00ccacd9122be502dd9590fe5d06da3b3c519c51/W01-SF417/d04'01_temp_thrsd_pct0.py)

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W01-SF417/img002.png?raw=true)

~~~python
=== Data-Driven Thresholds (Apr 2024) ===
Normal Operating Range:  48.00 - 57.80 °C
Warning Threshold:     57.80 °C
Alarm Threshold:       60.00 °C
~~~

- Code2: [d04'02_temp_thrsd_pct1.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/00ccacd9122be502dd9590fe5d06da3b3c519c51/W01-SF417/d04'02_temp_thrsd_pct1.py)

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W01-SF417/img003.png?raw=true)

~~~python
=== Thresholds Using Full AWS.csv (Apr 2024) ===
Normal Operating Min:  48.00 °C
Normal Operating Max:  68.80 °C
Warning Threshold:     >68.80 °C and ≤60.60 °C
Alarm Threshold:       >60.60 °C and ≤58.30 °C
~~~

- Code3: [d04'03_temp_thrsd_sdm0.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/00ccacd9122be502dd9590fe5d06da3b3c519c51/W01-SF417/d04'03_temp_thrsd_sdm0.py)

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W01-SF417/img004.png?raw=true)

~~~python
=== Thresholds Using Mean ± k·Std Dev (Apr 2024) ===
Normal Operating Range: 52.36 °C → 58.83 °C
Warning Threshold:      > 58.83 °C → 62.06 °C
Alarm Threshold:        > 62.06 °C → 65.29 °C
~~~

- Code4: [d04'04_temp_thrsd_sdm1.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/00ccacd9122be502dd9590fe5d06da3b3c519c51/W01-SF417/d04'04_temp_thrsd_sdm1.py)

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W01-SF417/img005.png?raw=true)

~~~python
=== Thresholds Using Mean ± k·Std Dev with AWS Logs (Apr 2024) ===
Normal Operating Range: 50.49 °C → 57.22 °C
Warning Threshold:      > 60.33 °C → 62.74 °C
Alarm Threshold:        > 59.02 °C → 59.82 °C
~~~

- Code5: [d04'05_temp_thrsd_sdm2.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/00ccacd9122be502dd9590fe5d06da3b3c519c51/W01-SF417/d04'05_temp_thrsd_sdm2.py)

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W01-SF417/img006.png?raw=true)

~~~python
=== Mean ± k·Std Dev Thresholds ===
Normal Operating Range: 47.13 °C → 57.22 °C
Warning Threshold:      55.53 °C
Alarm Threshold:        59.82 °C
~~~

### Issues Faced
- The first scripts calculated statistics (like average and standard deviation) using the entire dataset all at once. This approach was flawed because it mixed normal, warning, and alarm temperatures together, which skewed the results and made the "Normal" range inaccurate.

### Fixes Applied
- The code was modified to load the AWS alarm/warning logs.
- It then segmented the temperature data, identifying which readings occurred during a known warning, during a known alarm, or outside any event (true normal).
- Statistics were then calculated independently for each of these clean, separated data populations.

### Updated Observations
- The "Normal" range was calculated only from "true normal" data, resulting in a tighter, more representative baseline.
- The "Warning" and "Alarm" thresholds were calculated from the statistics of historical warning and alarm events, respectively. This means the thresholds are based on the actual behavior of the machine during those states, not just an arbitrary statistical cutoff.

### Conclusion
- Relying on simple, all-encompassing statistics for anomaly detection is unreliable. The key takeaway is that contextual data is crucial. By correlating the raw sensor time series (X-Minutal.csv) with the event logs (Full AWS.csv), we can build a significantly more robust, accurate, and reliable model for predictive maintenance.


