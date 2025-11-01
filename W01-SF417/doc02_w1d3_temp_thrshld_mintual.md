## Temperature Threshold Analysis for Device G97-N24 — April 2024

**Date:** 2025-10-23  
**Category:** Task

### Task Definition
To analyze and visualize the temperature behavior of the Bearing Drive End (D.E.) for device G97-N24 during April 2024, and correlate it with alarm and warning events recorded in the AWS logs.

### Insights
- The code uses Pandas, TensorFlow, and Matplotlib to filter, transform, and visualize device temperature data alongside alarm/warning events.
- It builds a time-series pipeline that extracts thresholds, converts data to tensors, and overlays critical ranges for anomaly detection and diagnostics.

### Code Results
- GitHub Link: [d03'06_temp_thrsd_mintl.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/00ccacd9122be502dd9590fe5d06da3b3c519c51/W01-SF417/d03'06_temp_thrsd_mintl.py)

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W01-SF417/img001.png?raw=true)

~~~python
Device: G97-N24
Parameter: Bearing D.E. Temperature max 10M (ºC)
Warning Range : 53.90 °C – 62.40 °C
Alarm Range   : 56.40 °C – 58.30 °C
~~~

### Issues Faced
- Column names had inconsistent formatting or hidden characters, which caused issues during filtering.
- Some date entries were malformed or missing, leading to NaN values and affecting the accuracy of time-based filtering.

### Fixes Applied
- Column names were cleaned using .str.strip() to remove hidden characters and trailing spaces, ensuring reliable filtering and access.
- Dates were parsed with pd.to_datetime(..., errors="coerce") to handle malformed entries gracefully and avoid runtime errors during time filtering.

### Updated Observations
- Alarm temperatures were consistently higher than warning temperatures, indicating distinct operational thresholds.
- Temperature spikes aligned with alarm and warning periods, revealing strong temporal correlation.

### Conclusion
- The analysis isolated temperature behavior during alarm and warning periods for a specific device in April 2024. It extracted threshold ranges and visualized critical excursions, enabling clear interpretation of operational risks and potential failure patterns.


