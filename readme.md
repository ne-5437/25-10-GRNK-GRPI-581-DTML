#### D3 Concurrency Comparison for Image I/O: Multithreading vs Multiprocessing
- `d003'1_multithreading_img.ipynb` - multithreading an image with 15 workers => 0.157s
- `d003'2_multiprocessing_img.ipynb` - synthetic multiprocessing an image with 15 workers => 0.170s

#### D3 Temperature Threshold Analysis for Device G97-N24
- `d003_3_temp_thrsd_mintl.py`(`img001`) - warning range (53.9-62.4), alarm range (56.4-58.3) => temp(warning>alarm) -> !

#### D4 Dynamic Thresholds for Bearing Temperature Anomaly Detection
- `d004'1_temp_thrsd_pct0.py`(`img002`) - percentile -> opr range(48-57.8), warning thr(57.8), alarm thr(60)
- `d004'2_temp_thrsd_pct1.py`(`img003`) - percentile v2 -> opr range(48-68.8), warning thr(68.8), alarm thr(60.6) -> !
- `d004'3_temp_thrsd_sdm0.py`(`img004`) - standard deviation -> opr range(52.36-58.83), warning thr(58.83), alarm thr(62.06)
- `d004'4_temp_thrsd_sdm1.py`(`img005`) - standard deviation v2 -> opr range(50.49-57.22), warning thr(60.33), alarm thr(59.02) -> !
- `d004'5_temp_thrsd_sdm2.py`(`img006`) - standard deviation v3 -> opr range(47.13-57.22), warning thr(55.53), alarm thr(59.82)

#### D4 Reporting and Visualizing Actual Temperature Ranges During Categorized Events
- `d004'6_temp_report.py` - A tabular report of every unit parameter's opr ranges(min/max), warning & alarm thresholds
- `d004'7_temp_report_plot.py`(`img007`) - A split bar plot to capture normal, warning & alarm states
- `d004'8_temp_report_stkplot_max.py`(`img008`) - A stacked plot to capture normal, warning & alarm states
- `d004'9_temp_report_spltplot_minmax.py`(`img009`) - A split bar plot to capture min/max normal, warning & alarm states
- `d004_10_temp_report_stkplot_minmax.py`(`img010`) - A stacked plot to capture min/max normal, warning & alarm states
- `d004_11_temp_plot_517_error.py`(`img011`) - A floating bar plot to capture min/max warning states for 517 Generator D.E. bearing temps
