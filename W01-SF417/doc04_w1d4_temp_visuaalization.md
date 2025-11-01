## Reporting and Visualizing Actual Temperature Ranges During Categorized Events

**Date:** 2025-10-24  
**Category:** Task

### Task Definition
The main task was to merge the 10-minute sensor data (X-Minutal.csv) with the event logs (Full AWS.csv) using pd.merge_asof. The goal was to generate both a statistical report and a series of visualizations to see the actual min/max temperature ranges for each device during known 'State', 'Warning', and 'Alarm' periods.

### Insights
- The conceptual basis of this task is descriptive analytics used for model validation. Instead of prescribing what a 'Warning' or 'Alarm' should be, this approach describes what is actually happening.
- By isolating sensor data using event logs as a ground truth, we can build a statistical profile of each machine's real-world behavior in different states, which is critical for validating any defined thresholds.

### Code Results
- Code1: [d04'06_temp_report.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/00ccacd9122be502dd9590fe5d06da3b3c519c51/W01-SF417/d04'06_temp_report.py)

~~~python
--- Detailed Temperature Operation Ranges (Min/Max) by Device and Category ---

--- Device: G97-N24 ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  53.50    80.00  70.80
                                               max  88.40    80.00  79.40
Trafo 3 winding temperature max 10M (ºC)       min  56.80    88.00  67.60
                                               max  95.90    88.00  75.90
Bearing D.E. Temperature max 10M (ºC)          min  46.20    70.10  49.70
                                               max  92.20    70.10  58.10
Bearing N.D.E. Temperature max 10M (ºC)        min  45.20    80.10  50.50
                                               max  93.70    80.10  62.70
Gearbox bearing temperature max 10M (ºC)       min  48.90    75.90  51.30
                                               max  78.40    75.90  67.40
Gearbox oil temperature max 10M (ºC)           min  52.30    68.80  55.00
                                               max  71.80    68.80  62.50
Generator windings temperature 1 max 10M (ºC)  min  54.50   129.30  63.80
                                               max 139.60   129.30  84.70
Generator windings temperature 2 max 10M (ºC)  min  54.30   128.60  63.40
                                               max 138.90   128.60  84.50
Generator windings temperature 3 max 10M (ºC)  min  54.00   131.10  63.00
                                               max 141.70   131.10  85.40
Generator’s sliprings temperature max 10M (ºC) min  38.50    61.30  45.90
                                               max  67.70    61.30  52.10
Nacelle temperature average 10M (ºC)           min  24.26    35.27  37.43
                                               max  43.95    35.27  40.42
Trafo 1 winding temperature max 10M (ºC)       min  48.10    72.10  67.00
                                               max  78.50    72.10  74.90

--- Device: G97-N25 ---
Category                                            State  Warning
Trafo 2 winding temperature max 10M (ºC)       min  42.40    52.30
                                               max  80.50    77.10
Trafo 3 winding temperature max 10M (ºC)       min  43.00    52.10
                                               max  78.90    71.60
Bearing D.E. Temperature max 10M (ºC)          min  43.20    48.00
                                               max  97.90    74.70
Bearing N.D.E. Temperature max 10M (ºC)        min  42.00    47.00
                                               max  96.60    74.10
Gearbox bearing temperature max 10M (ºC)       min  49.40    54.80
                                               max  77.60    77.60
Gearbox oil temperature max 10M (ºC)           min  52.50    55.90
                                               max  71.70    71.90
Generator windings temperature 1 max 10M (ºC)  min  47.00    56.40
                                               max 132.50   131.00
Generator windings temperature 2 max 10M (ºC)  min  46.70    56.10
                                               max 132.30   130.80
Generator windings temperature 3 max 10M (ºC)  min  47.20    56.70
                                               max 134.30   130.90
Generator’s sliprings temperature max 10M (ºC) min  34.50    40.30
                                               max  70.10    69.40
Nacelle temperature average 10M (ºC)           min  25.89    32.61
                                               max  44.86    45.27
Trafo 1 winding temperature max 10M (ºC)       min  55.60    65.40
                                               max 108.70    95.20

--- Device: G97-N26 ---
Category                                            State  Warning
Trafo 2 winding temperature max 10M (ºC)       min  60.00    60.80
                                               max  86.70    78.20
Trafo 3 winding temperature max 10M (ºC)       min  49.70    55.00
                                               max  81.40    69.60
Bearing D.E. Temperature max 10M (ºC)          min  46.00    47.10
                                               max  99.40    80.40
Bearing N.D.E. Temperature max 10M (ºC)        min  45.70    47.40
                                               max  95.70    66.10
Gearbox bearing temperature max 10M (ºC)       min  47.30    49.50
                                               max  78.30    72.20
Gearbox oil temperature max 10M (ºC)           min  41.40    53.90
                                               max  72.40    66.80
Generator windings temperature 1 max 10M (ºC)  min  50.30    56.50
                                               max 135.10    99.20
Generator windings temperature 2 max 10M (ºC)  min  52.70    54.90
                                               max 155.30   102.90
Generator windings temperature 3 max 10M (ºC)  min  52.20    55.00
                                               max 139.00   104.50
Generator’s sliprings temperature max 10M (ºC) min  38.70    43.90
                                               max  66.00    53.40
Nacelle temperature average 10M (ºC)           min  25.94    32.35
                                               max  44.83    45.29
Trafo 1 winding temperature max 10M (ºC)       min  45.90    53.20
                                               max  76.60    68.00

--- Device: G97-N26A ---
Category                                            State  Warning
Trafo 2 winding temperature max 10M (ºC)       min  53.50    58.10
                                               max  80.40    78.40
Trafo 3 winding temperature max 10M (ºC)       min  47.60    53.60
                                               max  77.30    73.80
Bearing D.E. Temperature max 10M (ºC)          min  45.50    49.90
                                               max  75.50    63.50
Bearing N.D.E. Temperature max 10M (ºC)        min  45.40    49.80
                                               max  95.40    68.50
Gearbox bearing temperature max 10M (ºC)       min  51.90    52.80
                                               max  84.50    78.80
Gearbox oil temperature max 10M (ºC)           min  55.30    55.30
                                               max  75.40    70.10
Generator windings temperature 1 max 10M (ºC)  min  52.30    65.00
                                               max 141.20   103.00
Generator windings temperature 2 max 10M (ºC)  min  51.40    65.40
                                               max 140.70   102.30
Generator windings temperature 3 max 10M (ºC)  min  51.90    62.20
                                               max 143.10   103.20
Generator’s sliprings temperature max 10M (ºC) min  38.90    43.60
                                               max  66.10    57.90
Nacelle temperature average 10M (ºC)           min  24.48    28.89
                                               max  44.47    45.65
Trafo 1 winding temperature max 10M (ºC)       min  56.90    57.10
                                               max  85.10    80.20

--- Device: G97-N27 ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  60.10    61.20  74.80
                                               max  94.70    95.30  76.00
Trafo 3 winding temperature max 10M (ºC)       min  45.60    52.60  60.20
                                               max  79.10    78.00  64.00
Bearing D.E. Temperature max 10M (ºC)          min  43.50    53.80  48.60
                                               max  97.20   100.10  59.80
Bearing N.D.E. Temperature max 10M (ºC)        min  41.60    49.30  48.40
                                               max  91.80    99.80  53.90
Gearbox bearing temperature max 10M (ºC)       min  48.20    61.10  62.70
                                               max  76.40    76.30  63.50
Gearbox oil temperature max 10M (ºC)           min  51.80    58.50  59.30
                                               max  70.60    70.10  60.20
Generator windings temperature 1 max 10M (ºC)  min  44.00    66.50  58.90
                                               max 128.60   133.10  70.90
Generator windings temperature 2 max 10M (ºC)  min  45.70    68.20  60.50
                                               max 130.20   134.80  72.50
Generator windings temperature 3 max 10M (ºC)  min  46.10    68.70  61.20
                                               max 130.20   134.60  73.00
Generator’s sliprings temperature max 10M (ºC) min  32.70    41.80  43.60
                                               max  61.90    56.60  48.20
Nacelle temperature average 10M (ºC)           min  24.55    28.19  35.29
                                               max  44.84    44.38  37.27
Trafo 1 winding temperature max 10M (ºC)       min  41.80    48.00  59.00
                                               max  73.60    69.60  59.90

--- Device: G97-N28 ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  59.50    61.10  70.70
                                               max  82.30    81.70  77.80
Trafo 3 winding temperature max 10M (ºC)       min  53.90    57.90  67.30
                                               max  81.40    77.00  74.20
Bearing D.E. Temperature max 10M (ºC)          min  43.70    47.10  55.30
                                               max  92.40    66.70  60.60
Bearing N.D.E. Temperature max 10M (ºC)        min  42.50    46.40  55.80
                                               max  96.40    76.90  64.90
Gearbox bearing temperature max 10M (ºC)       min  51.40    50.90  57.50
                                               max  82.40    81.30  66.60
Gearbox oil temperature max 10M (ºC)           min  48.10    52.00  57.40
                                               max  75.70    70.20  61.60
Generator windings temperature 1 max 10M (ºC)  min  55.20    56.70  65.20
                                               max 135.70   125.50  83.70
Generator windings temperature 2 max 10M (ºC)  min  54.20    57.20  64.30
                                               max 136.30   125.80  83.20
Generator windings temperature 3 max 10M (ºC)  min  54.50    57.60  64.60
                                               max 150.40   138.30  87.10
Generator’s sliprings temperature max 10M (ºC) min  41.00    45.00  52.50
                                               max  68.20    66.10  59.10
Nacelle temperature average 10M (ºC)           min  26.62    28.65  35.96
                                               max  46.60    47.91  44.82
Trafo 1 winding temperature max 10M (ºC)       min  50.30    51.40  67.20
                                               max  76.70    76.80  74.40

--- Device: G97-N29 ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  44.40    48.00  76.30
                                               max  90.60    81.00  82.30
Trafo 3 winding temperature max 10M (ºC)       min  56.20    61.00  73.40
                                               max 109.10    99.70  79.70
Bearing D.E. Temperature max 10M (ºC)          min  46.90    49.70  54.70
                                               max  93.30    89.90  56.60
Bearing N.D.E. Temperature max 10M (ºC)        min  46.30    49.50  57.80
                                               max  95.20    92.70  60.50
Gearbox bearing temperature max 10M (ºC)       min  46.50    51.30  61.80
                                               max  75.70    75.30  63.30
Gearbox oil temperature max 10M (ºC)           min  50.00    53.90  60.00
                                               max  70.50    70.10  60.30
Generator windings temperature 1 max 10M (ºC)  min  53.70    56.80  72.50
                                               max 133.30   114.70  84.00
Generator windings temperature 2 max 10M (ºC)  min  52.80    55.70  72.00
                                               max 139.70   120.30  83.20
Generator windings temperature 3 max 10M (ºC)  min  53.10    56.10  72.40
                                               max 132.20   116.40  83.70
Generator’s sliprings temperature max 10M (ºC) min  38.90    43.70  48.00
                                               max  61.80    61.40  50.20
Nacelle temperature average 10M (ºC)           min  24.52    33.55  35.83
                                               max  46.11    46.39  39.59
Trafo 1 winding temperature max 10M (ºC)       min  46.10    46.50  68.60
                                               max  88.90    80.70  74.90

--- Device: G97-N30 ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  56.50    58.30  60.50
                                               max  80.30    80.10  76.80
Trafo 3 winding temperature max 10M (ºC)       min  57.40    60.90  63.40
                                               max  79.30    78.20  75.10
Bearing D.E. Temperature max 10M (ºC)          min  42.60    42.40  57.20
                                               max 105.20   104.80 105.10
Bearing N.D.E. Temperature max 10M (ºC)        min  40.50    42.30  48.20
                                               max  99.40    93.80  95.90
Gearbox bearing temperature max 10M (ºC)       min  48.00    48.90  61.10
                                               max  80.00    79.90  79.10
Gearbox oil temperature max 10M (ºC)           min  52.00    52.00  60.60
                                               max  71.20    70.90  69.90
Generator windings temperature 1 max 10M (ºC)  min  47.00    46.60  55.80
                                               max 125.70   123.60 103.70
Generator windings temperature 2 max 10M (ºC)  min  45.00    44.60  53.70
                                               max 123.40   121.30 101.30
Generator windings temperature 3 max 10M (ºC)  min  46.20    45.90  55.10
                                               max 125.30   123.30 103.10
Generator’s sliprings temperature max 10M (ºC) min  32.70    37.60  47.40
                                               max  59.00    54.10  53.40
Nacelle temperature average 10M (ºC)           min  28.20    32.12  41.48
                                               max  44.92    45.36  43.74
Trafo 1 winding temperature max 10M (ºC)       min  54.40    58.90  62.80
                                               max  79.10    74.20  71.20

--- Device: G97-N30A ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  58.70    63.70  60.00
                                               max  88.90    80.40  76.80
Trafo 3 winding temperature max 10M (ºC)       min  51.80    57.50  58.40
                                               max  83.10    75.20  72.10
Bearing D.E. Temperature max 10M (ºC)          min  45.70    46.50  49.40
                                               max  71.40    56.90  58.90
Bearing N.D.E. Temperature max 10M (ºC)        min  45.10    48.50  53.40
                                               max  92.00    62.10  65.30
Gearbox bearing temperature max 10M (ºC)       min  47.30    51.80  55.60
                                               max  78.10    72.30  72.60
Gearbox oil temperature max 10M (ºC)           min  51.00    55.80  58.10
                                               max  71.90    66.30  66.40
Generator windings temperature 1 max 10M (ºC)  min  51.70    66.00  63.90
                                               max 139.30   100.30 100.20
Generator windings temperature 2 max 10M (ºC)  min  51.20    65.50  63.40
                                               max 136.10    96.90  99.10
Generator windings temperature 3 max 10M (ºC)  min  51.00    65.50  63.20
                                               max 138.30    96.40  99.10
Generator’s sliprings temperature max 10M (ºC) min  36.50    40.20  42.50
                                               max  63.00    53.90  51.00
Nacelle temperature average 10M (ºC)           min  23.62    26.85  32.43
                                               max  43.67    42.93  38.57
Trafo 1 winding temperature max 10M (ºC)       min  47.20    51.90  59.00
                                               max  80.40    75.60  72.90

--- Device: G97-N31 ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  41.20    60.60  61.60
                                               max  86.60    87.90  83.30
Trafo 3 winding temperature max 10M (ºC)       min  40.60    44.90  47.90
                                               max  79.30    77.00  72.70
Bearing D.E. Temperature max 10M (ºC)          min  38.90    46.30  53.30
                                               max 100.10    97.30  82.50
Bearing N.D.E. Temperature max 10M (ºC)        min  45.10    48.70  53.30
                                               max 100.10    99.00  88.70
Gearbox bearing temperature max 10M (ºC)       min  48.60    50.60  58.50
                                               max  78.00    77.40  73.00
Gearbox oil temperature max 10M (ºC)           min  44.30    52.40  58.70
                                               max  71.00    70.50  67.30
Generator windings temperature 1 max 10M (ºC)  min  53.60    55.30  61.50
                                               max 130.60   139.80  98.80
Generator windings temperature 2 max 10M (ºC)  min  53.60    55.70  61.80
                                               max 133.00   143.60 100.80
Generator windings temperature 3 max 10M (ºC)  min  52.90    55.40  61.60
                                               max 130.20   134.80  95.50
Generator’s sliprings temperature max 10M (ºC) min  38.50    42.80  40.90
                                               max  65.40    63.80  52.30
Nacelle temperature average 10M (ºC)           min  24.43    28.87  27.52
                                               max  44.45    44.16  42.87
Trafo 1 winding temperature max 10M (ºC)       min  39.50    47.70  51.20
                                               max  80.10    82.40  71.20

--- Device: G97-N32 ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  59.40    68.60  73.90
                                               max 119.40    92.10  73.90
Trafo 3 winding temperature max 10M (ºC)       min  58.60    67.70  73.30
                                               max 118.60    89.70  73.30
Bearing D.E. Temperature max 10M (ºC)          min  44.00    49.10  58.30
                                               max 105.00    76.60  59.20
Bearing N.D.E. Temperature max 10M (ºC)        min  41.90    50.30  53.30
                                               max 102.60    66.70  53.80
Gearbox bearing temperature max 10M (ºC)       min  49.50    61.60  57.70
                                               max  79.20    75.30  58.20
Gearbox oil temperature max 10M (ºC)           min  50.70    58.80  57.90
                                               max  72.60    69.60  58.20
Generator windings temperature 1 max 10M (ºC)  min  47.20    69.20  69.70
                                               max 138.80   100.40  70.10
Generator windings temperature 2 max 10M (ºC)  min  46.90    68.70  69.20
                                               max 138.90   100.30  69.70
Generator windings temperature 3 max 10M (ºC)  min  46.30    67.40  68.70
                                               max 138.20   100.00  69.10
Generator’s sliprings temperature max 10M (ºC) min  36.40    40.70  44.20
                                               max  66.70    51.20  44.30
Nacelle temperature average 10M (ºC)           min  29.84    33.89  40.70
                                               max  44.73    42.67  40.77
Trafo 1 winding temperature max 10M (ºC)       min  57.00    64.30  69.20
                                               max 114.20    87.60  69.30

--- Device: G97-N33 ---
Category                                            State  Warning
Trafo 2 winding temperature max 10M (ºC)       min  57.30    67.20
                                               max  94.20    67.30
Trafo 3 winding temperature max 10M (ºC)       min  55.70    66.20
                                               max  93.60    67.50
Bearing D.E. Temperature max 10M (ºC)          min  41.10    59.10
                                               max  96.40    61.30
Bearing N.D.E. Temperature max 10M (ºC)        min  41.80    63.90
                                               max  97.40    67.40
Gearbox bearing temperature max 10M (ºC)       min  48.70    65.40
                                               max  79.30    71.30
Gearbox oil temperature max 10M (ºC)           min  47.80    60.10
                                               max  71.40    64.00
Generator windings temperature 1 max 10M (ºC)  min  51.20    87.60
                                               max 139.90    93.70
Generator windings temperature 2 max 10M (ºC)  min  50.50    87.10
                                               max 139.00    93.00
Generator windings temperature 3 max 10M (ºC)  min  51.10    87.30
                                               max 139.70    93.70
Generator’s sliprings temperature max 10M (ºC) min  39.30    52.50
                                               max  64.90    56.60
Nacelle temperature average 10M (ºC)           min  24.15    36.12
                                               max  44.36    37.99
Trafo 1 winding temperature max 10M (ºC)       min  46.40    54.20
                                               max  77.30    65.20

--- Device: G97-N33A ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  57.00    59.20  71.70
                                               max  80.40    78.80  77.00
Trafo 3 winding temperature max 10M (ºC)       min  57.40    56.50  66.30
                                               max  77.10    74.40  71.80
Bearing D.E. Temperature max 10M (ºC)          min  45.90    48.40  51.50
                                               max  90.10    58.90  76.90
Bearing N.D.E. Temperature max 10M (ºC)        min  44.80    47.60  51.70
                                               max  93.00    63.00  57.40
Gearbox bearing temperature max 10M (ºC)       min  52.10    50.20  65.40
                                               max  80.30    68.60  70.00
Gearbox oil temperature max 10M (ºC)           min  51.80    51.20  59.90
                                               max  71.00    61.40  63.90
Generator windings temperature 1 max 10M (ºC)  min  53.10    58.20  66.30
                                               max 134.00    93.00  78.30
Generator windings temperature 2 max 10M (ºC)  min  52.50    57.20  71.30
                                               max 140.80    99.90  81.40
Generator windings temperature 3 max 10M (ºC)  min  52.80    57.00  68.60
                                               max 135.90    95.30  80.30
Generator’s sliprings temperature max 10M (ºC) min  37.60    44.50  45.80
                                               max  64.70    55.70  52.00
Nacelle temperature average 10M (ºC)           min  24.71    30.68  31.38
                                               max  43.52    41.73  32.34
Trafo 1 winding temperature max 10M (ºC)       min  55.80    56.60  67.10
                                               max  76.80    74.20  72.50

--- Device: G97-N34 ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  47.70    51.60  62.50
                                               max  80.40    80.20  79.30
Trafo 3 winding temperature max 10M (ºC)       min  44.10    45.40  56.00
                                               max  75.70    75.30  73.20
Bearing D.E. Temperature max 10M (ºC)          min  45.30    48.60  54.80
                                               max 100.10    99.80  90.20
Bearing N.D.E. Temperature max 10M (ºC)        min  44.10    48.60  51.30
                                               max 100.10    96.30  91.60
Gearbox bearing temperature max 10M (ºC)       min  48.30    54.90  58.20
                                               max  81.40    80.40  76.50
Gearbox oil temperature max 10M (ºC)           min  52.70    55.00  60.10
                                               max  71.30    70.20  67.50
Generator windings temperature 1 max 10M (ºC)  min  50.70    54.10  65.90
                                               max 134.40   121.40  91.00
Generator windings temperature 2 max 10M (ºC)  min  49.90    53.40  65.60
                                               max 135.50   123.80  91.60
Generator windings temperature 3 max 10M (ºC)  min  50.10    53.60  65.40
                                               max 137.60   127.30  92.20
Generator’s sliprings temperature max 10M (ºC) min  38.00    44.40  43.40
                                               max  79.70    67.50  58.90
Nacelle temperature average 10M (ºC)           min  27.65    29.52  28.93
                                               max  47.18    46.49  42.50
Trafo 1 winding temperature max 10M (ºC)       min  55.90    57.80  57.00
                                               max  89.20    82.10  74.30

--- Device: G97-N35 ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  57.10    78.30  72.30
                                               max  86.20    78.80  72.40
Trafo 3 winding temperature max 10M (ºC)       min  55.50    77.50  70.30
                                               max  84.00    78.20  70.50
Bearing D.E. Temperature max 10M (ºC)          min  44.90    68.40  61.10
                                               max  90.10    72.60  61.20
Bearing N.D.E. Temperature max 10M (ºC)        min  45.60    74.00  65.90
                                               max  97.80    77.70  65.90
Gearbox bearing temperature max 10M (ºC)       min  48.60    77.20  68.10
                                               max  78.00    77.30  69.90
Gearbox oil temperature max 10M (ºC)           min  52.40    69.20  63.30
                                               max  71.00    69.50  63.40
Generator windings temperature 1 max 10M (ºC)  min  55.00   111.40  89.10
                                               max 137.40   117.90  90.40
Generator windings temperature 2 max 10M (ºC)  min  54.50   110.50  89.00
                                               max 136.40   117.10  90.00
Generator windings temperature 3 max 10M (ºC)  min  54.40   111.70  89.40
                                               max 141.90   118.40  92.90
Generator’s sliprings temperature max 10M (ºC) min  39.60    62.40  53.50
                                               max  64.60    63.20  53.60
Nacelle temperature average 10M (ºC)           min  25.50    45.34  40.62
                                               max  44.28    45.54  40.80
Trafo 1 winding temperature max 10M (ºC)       min  55.10    77.40  70.50
                                               max  83.60    77.80  70.80

--- Device: G97-N36 ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  54.10    71.60  56.60
                                               max  80.90    78.30  73.30
Trafo 3 winding temperature max 10M (ºC)       min  57.30    69.00  60.30
                                               max  85.70    75.50  70.90
Bearing D.E. Temperature max 10M (ºC)          min  45.20    52.30  48.50
                                               max  85.80    60.60  60.80
Bearing N.D.E. Temperature max 10M (ºC)        min  45.00    53.70  48.70
                                               max  94.60    70.70  68.60
Gearbox bearing temperature max 10M (ºC)       min  50.50    63.40  54.80
                                               max  86.40    76.00  69.40
Gearbox oil temperature max 10M (ºC)           min  52.40    60.30  58.20
                                               max  75.00    67.70  64.00
Generator windings temperature 1 max 10M (ºC)  min  53.00    64.50  59.30
                                               max 144.10   100.10  79.30
Generator windings temperature 2 max 10M (ºC)  min  52.10    63.70  58.00
                                               max 144.30    99.10  78.50
Generator windings temperature 3 max 10M (ºC)  min  52.40    64.20  58.50
                                               max 138.70    98.50  79.00
Generator’s sliprings temperature max 10M (ºC) min  38.20    48.80  44.20
                                               max  70.60    54.10  54.10
Nacelle temperature average 10M (ºC)           min  25.69    33.48  39.35
                                               max  44.51    44.70  42.37
Trafo 1 winding temperature max 10M (ºC)       min  50.40    66.10  52.50
                                               max  80.40    73.90  68.50

--- Device: G97-N36A ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  60.10    70.60  71.60
                                               max  85.60    82.80  75.30
Trafo 3 winding temperature max 10M (ºC)       min  51.70    67.60  68.80
                                               max  79.40    78.50  73.20
Bearing D.E. Temperature max 10M (ºC)          min  46.80    57.50  61.50
                                               max 100.10    99.00  67.30
Bearing N.D.E. Temperature max 10M (ºC)        min  45.40    54.20  54.20
                                               max 100.00    97.60  65.30
Gearbox bearing temperature max 10M (ºC)       min  51.10    57.70  61.90
                                               max  79.60    77.30  62.40
Gearbox oil temperature max 10M (ºC)           min  53.40    57.70  58.50
                                               max  71.70    69.90  59.20
Generator windings temperature 1 max 10M (ºC)  min  52.80    62.80  64.30
                                               max 137.20   121.40  77.20
Generator windings temperature 2 max 10M (ºC)  min  52.00    62.30  63.80
                                               max 135.10   119.20  76.70
Generator windings temperature 3 max 10M (ºC)  min  51.90    62.70  64.30
                                               max 138.20   121.80  77.30
Generator’s sliprings temperature max 10M (ºC) min  39.40    52.00  51.30
                                               max  68.90    60.80  54.20
Nacelle temperature average 10M (ºC)           min  25.07    31.78  41.98
                                               max  45.61    46.04  43.41
Trafo 1 winding temperature max 10M (ºC)       min  46.70    62.80  65.80
                                               max  77.50    72.70  71.10

--- Device: G97-N36B ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  58.00    58.70  71.00
                                               max  86.90    83.70  83.90
Trafo 3 winding temperature max 10M (ºC)       min  48.50    49.70  69.10
                                               max  79.30    78.30  70.90
Bearing D.E. Temperature max 10M (ºC)          min  43.00    46.80  59.20
                                               max  92.50    67.90  80.40
Bearing N.D.E. Temperature max 10M (ºC)        min  42.40    46.20  62.30
                                               max  91.80    88.80  64.30
Gearbox bearing temperature max 10M (ºC)       min  47.50    53.80  64.90
                                               max  81.90    80.40  78.00
Gearbox oil temperature max 10M (ºC)           min  49.80    55.50  63.40
                                               max  74.10    72.60  69.90
Generator windings temperature 1 max 10M (ºC)  min  51.30    51.20  94.30
                                               max 134.40   126.00 108.50
Generator windings temperature 2 max 10M (ºC)  min  50.90    51.10  94.10
                                               max 133.70   125.30 110.60
Generator windings temperature 3 max 10M (ºC)  min  51.30    51.60  94.80
                                               max 140.10   131.30 113.80
Generator’s sliprings temperature max 10M (ºC) min  37.20    43.50  51.50
                                               max  70.40    69.60  56.30
Nacelle temperature average 10M (ºC)           min  27.34    28.50  36.80
                                               max  48.05    48.41  39.85
Trafo 1 winding temperature max 10M (ºC)       min  54.00    57.20  67.90
                                               max  80.30    76.30  76.90

--- Device: G97-N37 ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  55.10    57.00  62.40
                                               max  87.50    89.60  79.70
Trafo 3 winding temperature max 10M (ºC)       min  58.70    60.40  62.90
                                               max  90.00    92.60  81.70
Bearing D.E. Temperature max 10M (ºC)          min  44.10    44.40  50.80
                                               max  90.70    81.20  69.70
Bearing N.D.E. Temperature max 10M (ºC)        min  42.60    42.60  49.30
                                               max  92.10    82.40  76.80
Gearbox bearing temperature max 10M (ºC)       min  48.10    48.00  55.30
                                               max  81.90    84.40  80.50
Gearbox oil temperature max 10M (ºC)           min  49.70    53.20  58.40
                                               max  71.40    74.20  69.70
Generator windings temperature 1 max 10M (ºC)  min  51.40    56.20  61.20
                                               max 132.30   136.10 125.10
Generator windings temperature 2 max 10M (ºC)  min  49.50    54.20  59.10
                                               max 148.20   138.00 135.30
Generator windings temperature 3 max 10M (ºC)  min  50.80    54.60  60.20
                                               max 142.80   147.80 135.80
Generator’s sliprings temperature max 10M (ºC) min  37.70    39.10  43.70
                                               max  64.80    65.40  63.70
Nacelle temperature average 10M (ºC)           min  25.00    29.67  31.04
                                               max  46.33    46.97  41.81
Trafo 1 winding temperature max 10M (ºC)       min  48.50    49.70  57.00
                                               max  79.70    80.40  74.00

--- Device: G97-N37A ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  42.10    68.30  63.10
                                               max  80.50    80.10  77.70
Trafo 3 winding temperature max 10M (ºC)       min  41.10    65.10  59.70
                                               max  85.20    82.90  81.20
Bearing D.E. Temperature max 10M (ºC)          min  47.00    57.50  58.00
                                               max 100.10   100.10 100.10
Bearing N.D.E. Temperature max 10M (ºC)        min  42.20    50.90  49.50
                                               max  94.10    92.60  79.70
Gearbox bearing temperature max 10M (ºC)       min  46.50    59.60  58.00
                                               max  81.50    80.90  79.50
Gearbox oil temperature max 10M (ºC)           min  46.90    59.10  59.90
                                               max  72.50    71.90  70.70
Generator windings temperature 1 max 10M (ºC)  min  52.30    58.70  60.70
                                               max 132.90   122.30 114.60
Generator windings temperature 2 max 10M (ºC)  min  51.80    58.40  60.30
                                               max 137.20   126.90 118.10
Generator windings temperature 3 max 10M (ºC)  min  52.00    58.90  60.80
                                               max 144.30   134.30 125.40
Generator’s sliprings temperature max 10M (ºC) min  37.60    44.90  44.80
                                               max  66.70    62.70  59.30
Nacelle temperature average 10M (ºC)           min  24.87    33.97  28.85
                                               max  45.00    45.54  39.94
Trafo 1 winding temperature max 10M (ºC)       min  41.50    61.80  59.90
                                               max  76.70    76.20  74.50

--- Device: G97-N39 ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  56.90    61.60  68.30
                                               max  80.50    80.40  73.00
Trafo 3 winding temperature max 10M (ºC)       min  59.70    62.50  71.10
                                               max  80.30    80.10  75.50
Bearing D.E. Temperature max 10M (ºC)          min  44.20    51.40  46.90
                                               max  72.00    71.60  58.40
Bearing N.D.E. Temperature max 10M (ºC)        min  44.50    52.40  47.50
                                               max  79.30    95.20  62.20
Gearbox bearing temperature max 10M (ºC)       min  50.00    55.00  60.50
                                               max  78.10    80.50  65.60
Gearbox oil temperature max 10M (ºC)           min  51.50    54.40  55.20
                                               max  70.20    72.50  60.60
Generator windings temperature 1 max 10M (ºC)  min  53.30    60.40  60.80
                                               max 129.10   131.80  90.60
Generator windings temperature 2 max 10M (ºC)  min  52.80    60.00  60.80
                                               max 129.10   131.80  90.90
Generator windings temperature 3 max 10M (ºC)  min  52.80    60.00  61.90
                                               max 131.60   133.60  91.50
Generator’s sliprings temperature max 10M (ºC) min  39.00    48.00  47.60
                                               max  60.70    63.20  52.10
Nacelle temperature average 10M (ºC)           min  26.89    37.23  37.65
                                               max  47.53    47.92  39.40
Trafo 1 winding temperature max 10M (ºC)       min  56.40    59.10  65.50
                                               max  78.70    78.00  70.80

--- Device: G97-N39A ---
Category                                            State  Warning
Trafo 2 winding temperature max 10M (ºC)       min  55.20    62.00
                                               max  80.40    80.30
Trafo 3 winding temperature max 10M (ºC)       min  54.00    64.60
                                               max  82.30    80.40
Bearing D.E. Temperature max 10M (ºC)          min  44.50    61.10
                                               max 100.20   100.00
Bearing N.D.E. Temperature max 10M (ºC)        min  44.30    63.10
                                               max  86.50    80.50
Gearbox bearing temperature max 10M (ºC)       min  49.40    70.50
                                               max  82.20    81.90
Gearbox oil temperature max 10M (ºC)           min  52.40    63.60
                                               max  75.30    74.90
Generator windings temperature 1 max 10M (ºC)  min  51.50    87.10
                                               max 137.60   136.60
Generator windings temperature 2 max 10M (ºC)  min  51.30    88.30
                                               max 140.70   138.40
Generator windings temperature 3 max 10M (ºC)  min  51.50    93.30
                                               max 146.80   141.70
Generator’s sliprings temperature max 10M (ºC) min  39.20    55.10
                                               max  69.20    70.70
Nacelle temperature average 10M (ºC)           min  25.25    39.12
                                               max  45.11    46.21
Trafo 1 winding temperature max 10M (ºC)       min  53.50    66.10
                                               max  76.90    73.70

--- Device: G97-N40 ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  53.80    54.50  65.40
                                               max  91.40    82.00  72.70
Trafo 3 winding temperature max 10M (ºC)       min  59.70    59.10  67.50
                                               max  91.60    83.10  74.10
Bearing D.E. Temperature max 10M (ºC)          min  37.10    49.30  53.20
                                               max  74.40    72.50  60.40
Bearing N.D.E. Temperature max 10M (ºC)        min  37.10    51.20  55.50
                                               max  83.80    81.70  65.40
Gearbox bearing temperature max 10M (ºC)       min  43.90    55.50  62.90
                                               max  78.80    77.30  64.10
Gearbox oil temperature max 10M (ºC)           min  39.50    54.90  59.50
                                               max  72.70    70.20  60.00
Generator windings temperature 1 max 10M (ºC)  min  42.30    66.10  75.60
                                               max 140.70   131.40  90.50
Generator windings temperature 2 max 10M (ºC)  min  42.30    66.10  75.40
                                               max 139.90   130.40  90.20
Generator windings temperature 3 max 10M (ºC)  min  42.40    65.40  75.80
                                               max 142.40   132.50  91.30
Generator’s sliprings temperature max 10M (ºC) min  39.60    41.30  50.00
                                               max  64.90    65.10  54.10
Nacelle temperature average 10M (ºC)           min  25.47    27.50  36.77
                                               max  44.13    45.73  40.40
Trafo 1 winding temperature max 10M (ºC)       min  52.60    52.10  63.50
                                               max  88.30    79.50  70.70

--- Device: G97-N40A ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  51.50    50.80  67.50
                                               max 106.30    83.00  73.60
Trafo 3 winding temperature max 10M (ºC)       min  39.10    43.60  46.70
                                               max  87.50    79.60  68.50
Bearing D.E. Temperature max 10M (ºC)          min  45.20    48.10  51.30
                                               max  89.80    90.70  55.00
Bearing N.D.E. Temperature max 10M (ºC)        min  45.40    47.50  53.20
                                               max  85.40    81.20  58.70
Gearbox bearing temperature max 10M (ºC)       min  51.00    51.90  65.20
                                               max  84.10    79.70  68.10
Gearbox oil temperature max 10M (ºC)           min  55.80    56.00  61.50
                                               max  75.00    70.10  63.20
Generator windings temperature 1 max 10M (ºC)  min  54.40    58.70  63.50
                                               max 135.30   121.80  77.80
Generator windings temperature 2 max 10M (ºC)  min  54.20    59.30  63.50
                                               max 135.00   121.90  77.60
Generator windings temperature 3 max 10M (ºC)  min  54.60    60.80  67.90
                                               max 147.40   132.90  84.70
Generator’s sliprings temperature max 10M (ºC) min  39.40    42.60  45.40
                                               max  67.20    59.80  49.80
Nacelle temperature average 10M (ºC)           min  25.19    26.45  35.13
                                               max  43.49    39.32  38.13
Trafo 1 winding temperature max 10M (ºC)       min  54.70    51.20  57.90
                                               max  99.60    88.20  65.80

--- Device: G97-N41 ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  60.20    63.70  70.00
                                               max  81.90    83.50  70.00
Trafo 3 winding temperature max 10M (ºC)       min  47.70    55.20  65.40
                                               max  79.40    78.80  65.40
Bearing D.E. Temperature max 10M (ºC)          min  46.30    52.30  51.90
                                               max  86.20    84.10  51.90
Bearing N.D.E. Temperature max 10M (ºC)        min  45.30    52.90  52.90
                                               max  92.60    92.20  52.90
Gearbox bearing temperature max 10M (ºC)       min  51.50    58.90  62.30
                                               max  78.90    80.90  62.30
Gearbox oil temperature max 10M (ºC)           min  55.60    57.40  59.20
                                               max  72.40    74.90  59.20
Generator windings temperature 1 max 10M (ºC)  min  57.10    66.90  71.20
                                               max 132.20   136.10  71.20
Generator windings temperature 2 max 10M (ºC)  min  55.90    66.00  71.20
                                               max 140.50   148.40  71.20
Generator windings temperature 3 max 10M (ºC)  min  56.30    66.90  72.50
                                               max 134.20   137.40  72.50
Generator’s sliprings temperature max 10M (ºC) min  40.90    51.90  51.10
                                               max  67.20    70.00  51.10
Nacelle temperature average 10M (ºC)           min  27.88    38.38  39.02
                                               max  49.82    49.08  39.02
Trafo 1 winding temperature max 10M (ºC)       min  51.30    56.50  64.60
                                               max  75.00    75.70  64.60

--- Device: G97-N42 ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  59.00    66.40  66.20
                                               max  81.50    80.10  78.00
Trafo 3 winding temperature max 10M (ºC)       min  56.00    63.10  62.60
                                               max  82.50    81.30  75.20
Bearing D.E. Temperature max 10M (ºC)          min  46.10    47.90  48.40
                                               max 100.10   100.00  84.10
Bearing N.D.E. Temperature max 10M (ºC)        min  44.70    46.90  47.10
                                               max 100.10    98.70  85.70
Gearbox bearing temperature max 10M (ºC)       min  50.60    50.20  51.60
                                               max  81.50    81.10  71.90
Gearbox oil temperature max 10M (ºC)           min  54.30    54.20  57.80
                                               max  72.90    72.30  68.50
Generator windings temperature 1 max 10M (ºC)  min  52.80    55.20  57.70
                                               max 129.90   125.20  90.40
Generator windings temperature 2 max 10M (ºC)  min  52.40    54.50  56.80
                                               max 131.40   126.60  90.10
Generator windings temperature 3 max 10M (ºC)  min  53.00    54.60  56.80
                                               max 133.50   128.00  91.20
Generator’s sliprings temperature max 10M (ºC) min  38.60    45.20  46.00
                                               max  65.20    62.60  62.30
Nacelle temperature average 10M (ºC)           min  26.88    30.31  34.65
                                               max  46.07    46.01  41.24
Trafo 1 winding temperature max 10M (ºC)       min  49.40    56.00  62.40
                                               max  80.40    77.70  72.90

--- Device: G97-N43 ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  57.30    61.40  60.00
                                               max  89.00    81.90  62.50
Trafo 3 winding temperature max 10M (ºC)       min  37.50    44.90  54.50
                                               max  77.80    75.50  56.70
Bearing D.E. Temperature max 10M (ºC)          min  46.50    54.90  51.00
                                               max  94.20    64.90  54.40
Bearing N.D.E. Temperature max 10M (ºC)        min  46.30    57.30  50.40
                                               max  91.40    69.00  55.40
Gearbox bearing temperature max 10M (ºC)       min  48.20    57.20  57.80
                                               max  77.50    74.00  64.20
Gearbox oil temperature max 10M (ºC)           min  52.50    57.70  56.90
                                               max  71.80    68.10  60.10
Generator windings temperature 1 max 10M (ºC)  min  52.70    70.60  61.20
                                               max 133.40   105.40  73.00
Generator windings temperature 2 max 10M (ºC)  min  51.90    70.10  60.20
                                               max 132.40   104.90  72.00
Generator windings temperature 3 max 10M (ºC)  min  52.00    70.20  60.10
                                               max 133.20   104.60  72.50
Generator’s sliprings temperature max 10M (ºC) min  38.90    49.80  48.50
                                               max  66.20    62.30  51.30
Nacelle temperature average 10M (ºC)           min  24.71    31.37  36.85
                                               max  45.06    45.20  41.58
Trafo 1 winding temperature max 10M (ºC)       min  42.00    48.20  54.80
                                               max  77.20    74.80  56.30

--- Device: G97-N44 ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  50.70    51.40  69.80
                                               max  80.40    80.40  74.00
Trafo 3 winding temperature max 10M (ºC)       min  58.80    58.80  64.20
                                               max  77.20    77.00  68.20
Bearing D.E. Temperature max 10M (ºC)          min  46.20    53.10  52.50
                                               max  95.40    95.30  72.90
Bearing N.D.E. Temperature max 10M (ºC)        min  46.60    47.40  49.30
                                               max 100.10   100.10  58.90
Gearbox bearing temperature max 10M (ºC)       min  51.90    53.30  55.30
                                               max  80.80    83.60  65.00
Gearbox oil temperature max 10M (ºC)           min  48.30    56.90  58.80
                                               max  71.00    74.30  62.60
Generator windings temperature 1 max 10M (ºC)  min  55.60    65.20  61.70
                                               max 126.60   135.20  83.30
Generator windings temperature 2 max 10M (ºC)  min  55.10    64.10  60.80
                                               max 129.60   137.00  82.90
Generator windings temperature 3 max 10M (ºC)  min  54.80    62.90  60.10
                                               max 127.90   135.90  82.70
Generator’s sliprings temperature max 10M (ºC) min  39.70    43.10  44.50
                                               max  64.70    66.90  46.00
Nacelle temperature average 10M (ºC)           min  25.96    30.37  33.68
                                               max  48.38    47.80  37.61
Trafo 1 winding temperature max 10M (ºC)       min  55.00    57.50  64.00
                                               max  75.10    75.10  67.80

--- Device: G97-N45 ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  56.30    60.30  72.00
                                               max  80.40    80.10  79.00
Trafo 3 winding temperature max 10M (ºC)       min  51.30    55.30  66.10
                                               max  78.40    75.80  72.60
Bearing D.E. Temperature max 10M (ºC)          min  48.00    54.40  52.40
                                               max  93.40    92.70  63.30
Bearing N.D.E. Temperature max 10M (ºC)        min  47.40    54.40  51.50
                                               max  94.30    89.10  76.00
Gearbox bearing temperature max 10M (ºC)       min  46.00    59.70  53.80
                                               max  76.60    77.10  70.30
Gearbox oil temperature max 10M (ºC)           min  48.10    57.50  57.00
                                               max  70.20    70.10  64.20
Generator windings temperature 1 max 10M (ºC)  min  55.20    67.70  62.00
                                               max 131.20   132.30  87.60
Generator windings temperature 2 max 10M (ºC)  min  54.70    67.10  61.10
                                               max 127.50   132.50  88.20
Generator windings temperature 3 max 10M (ºC)  min  55.20    67.50  61.10
                                               max 133.80   142.80  93.30
Generator’s sliprings temperature max 10M (ºC) min  39.90    45.70  48.90
                                               max  61.80    62.80  56.40
Nacelle temperature average 10M (ºC)           min  26.24    33.05  39.35
                                               max  47.60    48.62  42.43
Trafo 1 winding temperature max 10M (ºC)       min  58.60    60.10  67.80
                                               max  80.40    79.90  74.00

--- Device: G97-N46 ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  55.60    58.00  75.80
                                               max  88.60    87.90  77.80
Trafo 3 winding temperature max 10M (ºC)       min  48.90    58.30  71.50
                                               max  81.90    83.90  72.80
Bearing D.E. Temperature max 10M (ºC)          min  48.60    48.60  59.20
                                               max  95.60    98.00  84.20
Bearing N.D.E. Temperature max 10M (ºC)        min  48.30    52.90  60.70
                                               max 100.10   100.10  78.40
Gearbox bearing temperature max 10M (ºC)       min  51.40    57.40  57.40
                                               max  90.10    79.00  90.80
Gearbox oil temperature max 10M (ºC)           min  50.10    54.20  57.30
                                               max  70.20    72.60  59.30
Generator windings temperature 1 max 10M (ºC)  min  57.70    68.20  75.20
                                               max 132.10   138.80  83.10
Generator windings temperature 2 max 10M (ºC)  min  56.60    67.60  76.10
                                               max 131.10   138.00  82.60
Generator windings temperature 3 max 10M (ºC)  min  57.10    68.30  78.50
                                               max 139.80   145.30  84.00
Generator’s sliprings temperature max 10M (ºC) min  36.70    40.90  48.70
                                               max  62.50    65.50  58.40
Nacelle temperature average 10M (ºC)           min  25.96    32.26  38.65
                                               max  47.00    47.10  40.82
Trafo 1 winding temperature max 10M (ºC)       min  56.10    59.40  72.20
                                               max  94.10    96.40  73.90

--- Device: G97-N46A ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  56.60    63.00  60.70
                                               max  85.80    80.60  76.30
Trafo 3 winding temperature max 10M (ºC)       min  57.30    58.60  60.20
                                               max  83.20    83.50  71.90
Bearing D.E. Temperature max 10M (ºC)          min  45.50    53.20  50.80
                                               max  90.70    93.30  57.00
Bearing N.D.E. Temperature max 10M (ºC)        min  45.60    53.90  51.80
                                               max  97.20    97.30  60.40
Gearbox bearing temperature max 10M (ºC)       min  49.00    55.40  53.90
                                               max  78.60    79.00  65.90
Gearbox oil temperature max 10M (ºC)           min  50.20    53.50  57.40
                                               max  70.80    71.80  60.80
Generator windings temperature 1 max 10M (ºC)  min  54.30    59.20  61.50
                                               max 135.80   129.00  77.80
Generator windings temperature 2 max 10M (ºC)  min  53.90    59.00  61.00
                                               max 142.10   131.90  78.60
Generator windings temperature 3 max 10M (ºC)  min  53.90    59.50  61.20
                                               max 138.40   134.80  78.70
Generator’s sliprings temperature max 10M (ºC) min  40.60    49.90  51.60
                                               max  71.10    71.30  54.30
Nacelle temperature average 10M (ºC)           min  24.22    35.08  37.66
                                               max  49.84    49.90  42.31
Trafo 1 winding temperature max 10M (ºC)       min  47.20    54.80  54.80
                                               max  75.30    75.30  71.50

--- Device: G97-N47 ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  43.00    60.20  66.80
                                               max  93.50    86.40  74.00
Trafo 3 winding temperature max 10M (ºC)       min  42.70    51.70  65.20
                                               max  78.80    77.80  71.70
Bearing D.E. Temperature max 10M (ºC)          min  45.80    50.00  55.70
                                               max  87.50    63.40  57.00
Bearing N.D.E. Temperature max 10M (ºC)        min  44.60    48.50  59.00
                                               max  94.20    74.50  60.90
Gearbox bearing temperature max 10M (ºC)       min  49.90    52.10  58.60
                                               max  75.90    74.50  61.60
Gearbox oil temperature max 10M (ºC)           min  51.20    55.00  58.90
                                               max  70.20    70.10  59.40
Generator windings temperature 1 max 10M (ºC)  min  51.10    58.00  71.70
                                               max 130.10   113.00  83.30
Generator windings temperature 2 max 10M (ºC)  min  50.40    57.00  70.90
                                               max 133.70   116.60  82.40
Generator windings temperature 3 max 10M (ºC)  min  50.70    56.90  71.30
                                               max 139.90   119.30  82.90
Generator’s sliprings temperature max 10M (ºC) min  38.70    45.60  51.50
                                               max  65.10    58.20  52.80
Nacelle temperature average 10M (ºC)           min  24.71    28.76  38.41
                                               max  45.49    45.47  42.85
Trafo 1 winding temperature max 10M (ºC)       min  41.80    56.90  61.30
                                               max  95.90    82.00  68.30

--- Device: G97-N48 ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  58.50    65.90  69.00
                                               max  86.20    75.20  71.20
Trafo 3 winding temperature max 10M (ºC)       min  52.90    62.00  65.70
                                               max  78.30    71.60  67.60
Bearing D.E. Temperature max 10M (ºC)          min  39.60    45.50  44.00
                                               max  97.20    55.00  52.40
Bearing N.D.E. Temperature max 10M (ºC)        min  39.20    46.50  47.20
                                               max 101.50    55.00  51.10
Gearbox bearing temperature max 10M (ºC)       min  48.40    50.60  48.40
                                               max  84.20    67.10  63.50
Gearbox oil temperature max 10M (ºC)           min  46.70    54.80  52.50
                                               max  81.10    62.10  59.90
Generator windings temperature 1 max 10M (ºC)  min  46.50    52.30  53.40
                                               max 117.30    69.70  62.60
Generator windings temperature 2 max 10M (ºC)  min  46.40    52.40  53.90
                                               max 134.20    77.40  66.20
Generator windings temperature 3 max 10M (ºC)  min  45.70    52.40  52.40
                                               max 126.50    75.90  64.50
Generator’s sliprings temperature max 10M (ºC) min  31.90    44.20  41.90
                                               max  62.70    49.70  47.30
Nacelle temperature average 10M (ºC)           min  25.77    33.97  36.00
                                               max  44.70    41.14  41.10
Trafo 1 winding temperature max 10M (ºC)       min  49.80    61.80  65.30
                                               max  75.40    71.00  67.60

--- Device: G97-N48A ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  59.00    59.40  59.40
                                               max  80.70    80.30  75.40
Trafo 3 winding temperature max 10M (ºC)       min  57.60    60.90  58.30
                                               max  78.80    78.20  74.60
Bearing D.E. Temperature max 10M (ºC)          min  45.70    47.50  49.70
                                               max  89.50    70.00  69.50
Bearing N.D.E. Temperature max 10M (ºC)        min  45.30    48.50  49.00
                                               max  98.40    82.10  67.90
Gearbox bearing temperature max 10M (ºC)       min  47.90    50.00  50.90
                                               max  78.80    74.70  71.70
Gearbox oil temperature max 10M (ºC)           min  50.60    52.30  52.80
                                               max  70.50    68.10  65.10
Generator windings temperature 1 max 10M (ºC)  min  55.20    56.50  58.40
                                               max 136.60   109.80  99.50
Generator windings temperature 2 max 10M (ºC)  min  53.80    55.00  57.00
                                               max 134.60   107.40  96.70
Generator windings temperature 3 max 10M (ºC)  min  53.40    54.90  56.90
                                               max 135.80   108.10  97.10
Generator’s sliprings temperature max 10M (ºC) min  40.90    44.10  46.00
                                               max  73.60    61.60  55.10
Nacelle temperature average 10M (ºC)           min  24.44    29.24  29.85
                                               max  43.68    41.05  41.89
Trafo 1 winding temperature max 10M (ºC)       min  53.40    55.10  57.60
                                               max  76.00    75.50  71.70

--- Device: G97-N49 ---
Category                                            State  Warning
Trafo 2 winding temperature max 10M (ºC)       min  45.90    52.80
                                               max  80.40    74.00
Trafo 3 winding temperature max 10M (ºC)       min  54.40    62.30
                                               max  77.70    70.70
Bearing D.E. Temperature max 10M (ºC)          min  45.10    51.40
                                               max  90.40    65.10
Bearing N.D.E. Temperature max 10M (ºC)        min  44.20    54.20
                                               max  92.40    87.60
Gearbox bearing temperature max 10M (ºC)       min  49.60    56.60
                                               max  81.40    75.60
Gearbox oil temperature max 10M (ºC)           min  53.60    59.40
                                               max  73.70    67.20
Generator windings temperature 1 max 10M (ºC)  min  51.90    69.40
                                               max 143.60   107.90
Generator windings temperature 2 max 10M (ºC)  min  51.70    68.90
                                               max 142.70   109.20
Generator windings temperature 3 max 10M (ºC)  min  52.10    69.00
                                               max 138.00   109.50
Generator’s sliprings temperature max 10M (ºC) min  37.10    48.30
                                               max  67.00    54.40
Nacelle temperature average 10M (ºC)           min  24.16    31.38
                                               max  44.51    36.49
Trafo 1 winding temperature max 10M (ºC)       min  58.70    62.60
                                               max  77.60    70.00

--- Device: G97-N51 ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  54.80    55.40  69.20
                                               max  81.70    80.50  69.30
Trafo 3 winding temperature max 10M (ºC)       min  59.40    59.60  68.40
                                               max  83.60    83.80  68.50
Bearing D.E. Temperature max 10M (ºC)          min  47.10    52.80  54.90
                                               max 100.10    94.10  55.00
Bearing N.D.E. Temperature max 10M (ºC)        min  47.30    49.60  56.20
                                               max  91.00    83.50  56.50
Gearbox bearing temperature max 10M (ºC)       min  50.90    55.90  54.70
                                               max  77.40    78.80  55.10
Gearbox oil temperature max 10M (ºC)           min  53.00    57.00  57.40
                                               max  70.30    72.20  57.50
Generator windings temperature 1 max 10M (ºC)  min  52.90    56.30  70.80
                                               max 130.30   135.80  71.20
Generator windings temperature 2 max 10M (ºC)  min  52.30    56.30  70.60
                                               max 131.70   137.00  71.00
Generator windings temperature 3 max 10M (ºC)  min  52.30    57.10  71.20
                                               max 134.20   140.40  71.50
Generator’s sliprings temperature max 10M (ºC) min  39.60    41.50  49.80
                                               max  73.80    74.50  50.10
Nacelle temperature average 10M (ºC)           min  24.54    26.38  38.32
                                               max  44.16    45.45  39.51
Trafo 1 winding temperature max 10M (ºC)       min  53.80    54.30  65.30
                                               max  79.20    81.10  65.40

--- Device: G97-N51A ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  49.00    51.70  73.40
                                               max  81.60    80.50  73.40
Trafo 3 winding temperature max 10M (ºC)       min  47.10    49.80  69.90
                                               max  80.00    79.10  69.90
Bearing D.E. Temperature max 10M (ºC)          min  45.40    48.50  53.20
                                               max  83.70    86.10  53.20
Bearing N.D.E. Temperature max 10M (ºC)        min  44.00    48.20  54.50
                                               max  94.40    90.00  54.50
Gearbox bearing temperature max 10M (ºC)       min  48.20    51.20  57.10
                                               max  78.60    78.50  57.10
Gearbox oil temperature max 10M (ºC)           min  51.10    53.40  58.20
                                               max  71.30    70.50  58.20
Generator windings temperature 1 max 10M (ºC)  min  53.30    54.10  70.10
                                               max 126.40   130.00  70.10
Generator windings temperature 2 max 10M (ºC)  min  53.20    54.10  69.80
                                               max 139.90   137.70  69.80
Generator windings temperature 3 max 10M (ºC)  min  52.40    53.50  69.20
                                               max 136.00   135.20  69.20
Generator’s sliprings temperature max 10M (ºC) min  39.40    47.10  50.80
                                               max  68.80    72.00  50.80
Nacelle temperature average 10M (ºC)           min  24.81    33.65  40.84
                                               max  44.93    46.34  40.84
Trafo 1 winding temperature max 10M (ºC)       min  58.30    62.20  69.60
                                               max 154.70    87.00  69.60

--- Device: G97-N51B ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  51.70    68.50  59.30
                                               max  83.20    80.50  82.00
Trafo 3 winding temperature max 10M (ºC)       min  59.30    63.70  64.50
                                               max  95.60    76.60  79.60
Bearing D.E. Temperature max 10M (ºC)          min  42.20    50.10  46.80
                                               max  77.50    67.30  72.80
Bearing N.D.E. Temperature max 10M (ºC)        min  43.60    55.30  56.00
                                               max  98.50    75.20  88.50
Gearbox bearing temperature max 10M (ºC)       min  46.40    60.60  60.60
                                               max  77.70    74.10  71.10
Gearbox oil temperature max 10M (ºC)           min  50.90    58.70  60.10
                                               max  72.90    70.10  66.70
Generator windings temperature 1 max 10M (ºC)  min  53.00    69.30  71.50
                                               max 142.20   109.00 107.90
Generator windings temperature 2 max 10M (ºC)  min  52.30    68.70  71.20
                                               max 140.00   110.20 107.10
Generator windings temperature 3 max 10M (ºC)  min  51.90    68.80  70.70
                                               max 137.20   105.90 107.00
Generator’s sliprings temperature max 10M (ºC) min  38.40    46.20  41.50
                                               max  65.20    58.40  55.70
Nacelle temperature average 10M (ºC)           min  25.34    33.01  26.43
                                               max  44.68    41.93  42.94
Trafo 1 winding temperature max 10M (ºC)       min  48.70    63.50  59.70
                                               max  80.70    75.60  73.30

--- Device: G97-N51C ---
Category                                            State  Warning
Trafo 2 winding temperature max 10M (ºC)       min  58.80    70.90
                                               max  81.70    81.20
Trafo 3 winding temperature max 10M (ºC)       min  56.40    69.00
                                               max  78.60    78.60
Bearing D.E. Temperature max 10M (ºC)          min  46.70    53.90
                                               max  91.90    72.60
Bearing N.D.E. Temperature max 10M (ºC)        min  44.70    53.30
                                               max  98.20    79.40
Gearbox bearing temperature max 10M (ºC)       min  49.40    59.40
                                               max  75.80    76.40
Gearbox oil temperature max 10M (ºC)           min  52.20    56.90
                                               max  70.30    70.10
Generator windings temperature 1 max 10M (ºC)  min  52.60    68.20
                                               max 127.60   126.50
Generator windings temperature 2 max 10M (ºC)  min  52.40    68.00
                                               max 129.50   126.00
Generator windings temperature 3 max 10M (ºC)  min  52.40    67.90
                                               max 133.80   130.50
Generator’s sliprings temperature max 10M (ºC) min  39.40    51.60
                                               max  65.70    67.60
Nacelle temperature average 10M (ºC)           min  24.58    40.11
                                               max  45.12    46.74
Trafo 1 winding temperature max 10M (ºC)       min  57.70    68.30
                                               max  81.60    80.10

--- Device: G97-N51D ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  60.20    60.40  63.20
                                               max  80.70    80.50  77.60
Trafo 3 winding temperature max 10M (ºC)       min  51.40    54.60  57.80
                                               max  76.40    77.30  69.30
Bearing D.E. Temperature max 10M (ºC)          min  44.20    47.80  49.60
                                               max  91.60    89.00  52.10
Bearing N.D.E. Temperature max 10M (ºC)        min  46.80    51.20  52.80
                                               max  93.60    76.30  56.60
Gearbox bearing temperature max 10M (ºC)       min  51.40    56.30  57.50
                                               max  81.00    77.30  63.30
Gearbox oil temperature max 10M (ºC)           min  53.20    58.50  55.70
                                               max  73.30    70.30  60.40
Generator windings temperature 1 max 10M (ºC)  min  50.80    59.90  64.10
                                               max 135.60   131.30  66.00
Generator windings temperature 2 max 10M (ºC)  min  50.30    59.30  64.20
                                               max 148.70   143.60  68.50
Generator windings temperature 3 max 10M (ºC)  min  50.20    59.10  62.90
                                               max 136.50   129.40  66.00
Generator’s sliprings temperature max 10M (ºC) min  37.20    43.10  42.80
                                               max  69.70    60.00  51.60
Nacelle temperature average 10M (ºC)           min  25.30    26.25  30.64
                                               max  44.15    41.18  41.69
Trafo 1 winding temperature max 10M (ºC)       min  49.10    50.80  55.00
                                               max  73.80    72.50  68.70

--- Device: G97-N52 ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  57.50    68.80  68.10
                                               max  80.40    80.30  76.90
Trafo 3 winding temperature max 10M (ºC)       min  60.30    66.40  64.70
                                               max  78.40    76.70  71.40
Bearing D.E. Temperature max 10M (ºC)          min  44.80    47.90  53.70
                                               max  87.90    70.10  58.00
Bearing N.D.E. Temperature max 10M (ºC)        min  45.80    48.30  54.40
                                               max  90.20    77.40  63.30
Gearbox bearing temperature max 10M (ºC)       min  51.90    53.70  63.10
                                               max  83.00    82.80  72.80
Gearbox oil temperature max 10M (ºC)           min  56.00    56.00  60.50
                                               max  74.70    75.00  64.90
Generator windings temperature 1 max 10M (ºC)  min  54.00    56.00  70.20
                                               max 135.50   133.70  98.70
Generator windings temperature 2 max 10M (ºC)  min  53.50    55.70  70.40
                                               max 134.70   133.00  97.60
Generator windings temperature 3 max 10M (ºC)  min  53.60    56.20  70.90
                                               max 148.40   149.10 100.70
Generator’s sliprings temperature max 10M (ºC) min  38.70    44.40  47.80
                                               max  68.80    70.50  53.30
Nacelle temperature average 10M (ºC)           min  27.44    29.99  34.62
                                               max  47.93    46.66  41.65
Trafo 1 winding temperature max 10M (ºC)       min  56.30    64.00  63.90
                                               max  74.60    73.50  70.00

--- Device: G97-N52A ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  55.00    47.90  71.00
                                               max  80.50    80.50  72.40
Trafo 3 winding temperature max 10M (ºC)       min  52.80    46.60  67.60
                                               max  78.20    77.80  69.80
Bearing D.E. Temperature max 10M (ºC)          min  45.40    52.60  49.90
                                               max  91.40    88.00  70.00
Bearing N.D.E. Temperature max 10M (ºC)        min  44.60    47.90  52.30
                                               max  92.30    82.40  63.00
Gearbox bearing temperature max 10M (ºC)       min  50.40    55.30  51.90
                                               max  80.30    79.20  71.50
Gearbox oil temperature max 10M (ºC)           min  54.30    56.00  56.60
                                               max  70.50    73.60  66.70
Generator windings temperature 1 max 10M (ºC)  min  51.20    59.00  63.30
                                               max 130.10   136.50  91.20
Generator windings temperature 2 max 10M (ºC)  min  50.50    58.40  62.80
                                               max 136.00   146.50  98.90
Generator windings temperature 3 max 10M (ºC)  min  50.80    58.60  63.00
                                               max 142.50   137.70  97.70
Generator’s sliprings temperature max 10M (ºC) min  38.30    39.40  41.00
                                               max  64.80    66.50  51.10
Nacelle temperature average 10M (ºC)           min  27.99    32.31  36.03
                                               max  47.96    48.27  39.52
Trafo 1 winding temperature max 10M (ºC)       min  50.10    44.80  64.30
                                               max  74.70    75.20  65.20

--- Device: G97-N53 ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  60.30    60.80  67.00
                                               max  80.40    80.10  67.00
Trafo 3 winding temperature max 10M (ºC)       min  50.10    51.30  62.70
                                               max  78.20    76.30  62.70
Bearing D.E. Temperature max 10M (ºC)          min  45.80    47.90  50.20
                                               max 100.10    86.80  50.20
Bearing N.D.E. Temperature max 10M (ºC)        min  46.00    52.90  51.00
                                               max  99.10    86.10  51.00
Gearbox bearing temperature max 10M (ºC)       min  51.90    57.50  63.70
                                               max  81.70    75.40  63.70
Gearbox oil temperature max 10M (ºC)           min  53.00    56.00  59.80
                                               max  72.60    68.30  59.80
Generator windings temperature 1 max 10M (ºC)  min  53.30    64.40  63.50
                                               max 131.10   101.80  63.50
Generator windings temperature 2 max 10M (ºC)  min  52.60    63.90  63.50
                                               max 131.50   101.40  63.50
Generator windings temperature 3 max 10M (ºC)  min  53.40    67.70  65.00
                                               max 144.10   116.50  65.00
Generator’s sliprings temperature max 10M (ºC) min  38.20    43.20  47.60
                                               max  69.60    61.20  47.60
Nacelle temperature average 10M (ºC)           min  24.24    27.92  35.37
                                               max  44.18    42.40  35.37
Trafo 1 winding temperature max 10M (ºC)       min  51.90    51.90  62.50
                                               max  80.00    75.20  62.50

--- Device: G97-N53A ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  55.70    62.90  68.80
                                               max  80.40    79.90  78.10
Trafo 3 winding temperature max 10M (ºC)       min  56.30    59.10  64.20
                                               max  83.90    76.20  73.60
Bearing D.E. Temperature max 10M (ºC)          min  45.00    50.50  51.30
                                               max  90.40    65.50  65.20
Bearing N.D.E. Temperature max 10M (ºC)        min  44.70    51.20  50.90
                                               max  99.30    76.20  76.10
Gearbox bearing temperature max 10M (ºC)       min  51.80    58.30  59.50
                                               max  83.00    76.90  75.00
Gearbox oil temperature max 10M (ºC)           min  55.20    58.90  60.10
                                               max  73.40    68.20  70.10
Generator windings temperature 1 max 10M (ºC)  min  53.90    62.00  61.90
                                               max 131.50    96.30  88.50
Generator windings temperature 2 max 10M (ºC)  min  53.10    60.90  60.70
                                               max 132.60    96.00  87.60
Generator windings temperature 3 max 10M (ºC)  min  53.80    61.60  61.40
                                               max 134.90    99.50  88.60
Generator’s sliprings temperature max 10M (ºC) min  38.80    43.90  43.40
                                               max  69.10    62.70  53.90
Nacelle temperature average 10M (ºC)           min  25.99    29.34  31.48
                                               max  44.56    45.38  43.43
Trafo 1 winding temperature max 10M (ºC)       min  47.10    58.60  64.30
                                               max  77.20    75.50  72.80

--- Device: G97-N53B ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  60.20    63.40  73.10
                                               max  94.40    80.30  73.10
Trafo 3 winding temperature max 10M (ºC)       min  49.80    54.80  72.30
                                               max  80.20    78.00  72.30
Bearing D.E. Temperature max 10M (ºC)          min  47.30    54.90  57.50
                                               max  91.60    79.90  57.50
Bearing N.D.E. Temperature max 10M (ºC)        min  46.80    55.80  59.80
                                               max  98.50    80.80  59.80
Gearbox bearing temperature max 10M (ºC)       min  50.50    55.00  63.70
                                               max  78.40    71.60  63.70
Gearbox oil temperature max 10M (ºC)           min  53.50    56.50  60.20
                                               max  73.00    68.80  60.20
Generator windings temperature 1 max 10M (ºC)  min  54.70    67.70  80.60
                                               max 136.60    99.20  80.60
Generator windings temperature 2 max 10M (ºC)  min  54.20    66.90  80.30
                                               max 136.90   101.20  80.30
Generator windings temperature 3 max 10M (ºC)  min  54.50    67.00  80.80
                                               max 141.70   107.60  80.80
Generator’s sliprings temperature max 10M (ºC) min  39.00    44.30  52.90
                                               max  68.60    57.90  52.90
Nacelle temperature average 10M (ºC)           min  25.16    30.15  37.69
                                               max  44.52    40.89  37.69
Trafo 1 winding temperature max 10M (ºC)       min  51.30    55.80  70.50
                                               max  78.80    75.10  70.50

--- Device: G97-N54 ---
Category                                            State  Warning
Trafo 2 winding temperature max 10M (ºC)       min  59.10    75.40
                                               max  80.40    75.60
Trafo 3 winding temperature max 10M (ºC)       min  52.40    72.10
                                               max  78.00    72.50
Bearing D.E. Temperature max 10M (ºC)          min  44.90    52.40
                                               max  89.30    61.90
Bearing N.D.E. Temperature max 10M (ºC)        min  44.10    52.30
                                               max 113.50    67.50
Gearbox bearing temperature max 10M (ºC)       min  50.90    62.00
                                               max  84.90    69.50
Gearbox oil temperature max 10M (ºC)           min  56.80    57.50
                                               max  75.50    61.90
Generator windings temperature 1 max 10M (ºC)  min  52.00    70.10
                                               max 135.70    96.30
Generator windings temperature 2 max 10M (ºC)  min  51.10    72.70
                                               max 148.80    98.40
Generator windings temperature 3 max 10M (ºC)  min  51.60    70.90
                                               max 139.40    97.20
Generator’s sliprings temperature max 10M (ºC) min  36.30    50.90
                                               max  61.80    53.00
Nacelle temperature average 10M (ºC)           min  25.57    42.56
                                               max  44.83    44.74
Trafo 1 winding temperature max 10M (ºC)       min  56.60    70.90
                                               max  81.80    71.30

--- Device: G97-N54A ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  55.80    58.60  59.80
                                               max  80.50    78.90  77.30
Trafo 3 winding temperature max 10M (ºC)       min  58.20    60.60  61.90
                                               max  80.60    82.90  74.00
Bearing D.E. Temperature max 10M (ºC)          min  45.20    53.80  54.10
                                               max  84.20    70.50  67.90
Bearing N.D.E. Temperature max 10M (ºC)        min  45.00    57.70  58.30
                                               max  91.50    95.20  88.90
Gearbox bearing temperature max 10M (ºC)       min  50.90    57.70  58.30
                                               max  87.20    79.80  85.30
Gearbox oil temperature max 10M (ºC)           min  52.20    58.80  59.00
                                               max  85.10    73.00  85.00
Generator windings temperature 1 max 10M (ºC)  min  54.60    65.70  62.30
                                               max 125.10   130.90 101.90
Generator windings temperature 2 max 10M (ºC)  min  54.60    65.30  62.20
                                               max 131.20   132.30 101.00
Generator windings temperature 3 max 10M (ºC)  min  54.80    65.10  61.90
                                               max 125.40   130.80 101.80
Generator’s sliprings temperature max 10M (ºC) min  39.10    48.10  45.90
                                               max  63.30    63.50  55.60
Nacelle temperature average 10M (ºC)           min  24.93    33.17  37.71
                                               max  44.60    45.96  42.29
Trafo 1 winding temperature max 10M (ºC)       min  54.00    55.90  56.70
                                               max  80.40    78.10  70.40

--- Device: G97-N55 ---
Category                                            State  Warning
Trafo 2 winding temperature max 10M (ºC)       min  59.60    60.50
                                               max  81.20    80.20
Trafo 3 winding temperature max 10M (ºC)       min  49.40    54.30
                                               max  78.20    77.40
Bearing D.E. Temperature max 10M (ºC)          min  46.00    49.40
                                               max  99.50    99.50
Bearing N.D.E. Temperature max 10M (ºC)        min  44.60    54.60
                                               max 100.10    97.90
Gearbox bearing temperature max 10M (ºC)       min  50.70    55.60
                                               max  78.20    77.90
Gearbox oil temperature max 10M (ºC)           min  53.20    57.50
                                               max  70.20    70.20
Generator windings temperature 1 max 10M (ºC)  min  50.80    66.60
                                               max 130.40   133.40
Generator windings temperature 2 max 10M (ºC)  min  50.90    66.80
                                               max 141.60   139.50
Generator windings temperature 3 max 10M (ºC)  min  50.90    66.60
                                               max 135.80   138.70
Generator’s sliprings temperature max 10M (ºC) min  38.60    42.20
                                               max  76.70    64.40
Nacelle temperature average 10M (ºC)           min  24.95    27.77
                                               max  44.82    43.06
Trafo 1 winding temperature max 10M (ºC)       min  46.10    49.80
                                               max  80.40    79.00

--- Device: G97-N55A ---
Category                                            State  Warning  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  42.40    48.10  54.30
                                               max  79.50    57.90  56.10
Trafo 3 winding temperature max 10M (ºC)       min  53.80    58.10  61.20
                                               max 102.00    72.10  68.20
Bearing D.E. Temperature max 10M (ºC)          min  47.30    48.00  55.60
                                               max  78.00    61.50  60.00
Bearing N.D.E. Temperature max 10M (ºC)        min  46.10    49.90  57.50
                                               max  83.80    65.70  63.80
Gearbox bearing temperature max 10M (ºC)       min  49.70    55.40  63.70
                                               max  79.00    69.70  72.70
Gearbox oil temperature max 10M (ºC)           min  53.20    56.80  60.70
                                               max  73.70    64.20  67.30
Generator windings temperature 1 max 10M (ºC)  min  52.90    58.30  69.90
                                               max 135.20    89.50  90.40
Generator windings temperature 2 max 10M (ºC)  min  52.50    58.00  70.30
                                               max 135.40    90.30  91.10
Generator windings temperature 3 max 10M (ºC)  min  52.90    58.30  77.10
                                               max 150.10    99.60  97.80
Generator’s sliprings temperature max 10M (ºC) min  40.00    42.30  52.60
                                               max  71.20    60.30  60.20
Nacelle temperature average 10M (ºC)           min  24.71    31.65  36.65
                                               max  46.10    46.68  42.72
Trafo 1 winding temperature max 10M (ºC)       min  35.90    40.70  49.10
                                               max  64.80    52.30  50.10

--- Device: G97-N55B ---
Category                                            State  Alarm
Trafo 2 winding temperature max 10M (ºC)       min  60.20  72.10
                                               max  80.50  75.90
Trafo 3 winding temperature max 10M (ºC)       min  47.60  68.30
                                               max  76.70  72.10
Bearing D.E. Temperature max 10M (ºC)          min  41.20  49.00
                                               max 101.10  60.00
Bearing N.D.E. Temperature max 10M (ºC)        min  40.00  47.70
                                               max  76.50  56.60
Gearbox bearing temperature max 10M (ºC)       min  51.80  61.90
                                               max  78.60  68.80
Gearbox oil temperature max 10M (ºC)           min  54.30  58.40
                                               max  70.90  64.00
Generator windings temperature 1 max 10M (ºC)  min  46.00  52.50
                                               max 131.10  82.80
Generator windings temperature 2 max 10M (ºC)  min  45.30  51.20
                                               max 119.00  72.40
Generator windings temperature 3 max 10M (ºC)  min  44.40  50.60
                                               max 134.70  89.00
Generator’s sliprings temperature max 10M (ºC) min  35.30  49.90
                                               max  78.10  57.30
Nacelle temperature average 10M (ºC)           min  26.12  35.95
                                               max  44.85  39.26
Trafo 1 winding temperature max 10M (ºC)       min  45.40  67.40
                                               max  81.40  70.60
~~~

- Code2: [d04'07_temp_report_plot.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/00ccacd9122be502dd9590fe5d06da3b3c519c51/W01-SF417/d04'07_temp_report_plot.py)

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W01-SF417/img007.png?raw=true)

- Code3: [d04'08_temp_report_stkplot_max.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/00ccacd9122be502dd9590fe5d06da3b3c519c51/W01-SF417/d04'08_temp_report_stkplot_max.py)

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W01-SF417/img008.png?raw=true)

- Code4: [d04'09_temp_report_spltplot_minmax.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/00ccacd9122be502dd9590fe5d06da3b3c519c51/W01-SF417/d04'09_temp_report_spltplot_minmax.py)

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W01-SF417/img009.png?raw=true)

- Code5: [d04'10_temp_report_stkplot_minmax.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/00ccacd9122be502dd9590fe5d06da3b3c519c51/W01-SF417/d04'10_temp_report_stkplot_minmax.py)

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W01-SF417/img010.png?raw=true)

- Code6: [d04'11_temp_plot_517_error.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/00ccacd9122be502dd9590fe5d06da3b3c519c51/W01-SF417/d04'11_temp_plot_517_error.py)

![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W01-SF417/img011.png?raw=true)

### Issues Faced
- Initial visualizations were unclear because they only plotted the max temperature (losing the min value) or used overlapping bars, which caused categories to hide one another.
- The main technical challenge was correctly aligning the 10-minute sensor data with the specific Start Date and End Date of the event logs.

### Fixes Applied
- The visualization was fixed by creating "floating bars" (setting the bar bottom to the min and height to max - min) and then grouping them side-by-side with an x-axis offset to prevent overlap.
- The data alignment was solved using a two-step process: first pd.merge_asof to find the last event, then a filter to keep only the readings that were also before the event's End Date.

### Updated Observations
- The text report successfully generated the most comprehensive statistical data, creating a baseline of min/max values. For visualization, the grouped floating bar chart was clearly the most effective method, as it successfully displayed the full operational range (min-to-max) for each category in a way that was easy to compare and where no data was hidden.

### Conclusion
- This batch of scripts successfully demonstrates how to use event logs to validate and report on sensor behavior. The key technical achievements were the robust use of merge_asof for time-interval merging and the development of the "grouped floating bar chart" as the most effective way to visualize and compare operational ranges across multiple devices and categories.


