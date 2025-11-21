## GH vs Volume - Multi-Scale Analysis

**Date:** 2025-11-06  
**Category:** Data Preprocessing

### 🔍 Insights
- GH→Volume is near-linear and stable across the month.
- Weekly slopes vary slightly (likely operational window / range effects) but remain high-R².
- Day-wise patterns inside a week are consistent; KDE heatmaps show the same tight diagonal density band each day.

### 🧪 Task Definition
The task was to analyze the Gross Head (GH) vs Volume relationship for the reservoir system using minute-level data. The study covered multiple scales — a full-month plot, weekly comparisons, a one-week KDE visualization to explore daily density patterns, and day-wise slope and heatmap analyses for that week. The goal was to check the stability, linearity, and day-to-day consistency of GH–Volume behavior.

### 📎 Code Results
- Code1: [d13'01_gh_v_vol_plot_whole.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/bbe046a1a01a082354848c917e5f4022691566b2/W03-SF408/d13'01_gh_v_vol_plot_whole.py)

- ![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W03-SF408/img204.png?raw=true)

- Code2: [d13'02_gh_v_vol_plot_1m_wkly.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/bbe046a1a01a082354848c917e5f4022691566b2/W03-SF408/d13'02_gh_v_vol_plot_1m_wkly.py)

- ![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W03-SF408/img205.png?raw=true)
- ![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W03-SF408/img206.png?raw=true)

- Code3: [d13'03_gh_v_vol_plot_kde_wk1.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/bbe046a1a01a082354848c917e5f4022691566b2/W03-SF408/d13'03_gh_v_vol_plot_kde_wk1.py)

- ![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W03-SF408/img207.png?raw=true)

- Code4: [d13'04_gh_v_vol_plot_slope_wk1.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/c9a21881360f79125af7540b708cc09a815c9463/W03-SF408/d13'04_gh_v_vol_plot_slope_wk1.py)


- ![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W03-SF408/img208.png?raw=true)

- Code5: [d13'05_gh_v_vol_plot_daywise_heatmap.py](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/c9a21881360f79125af7540b708cc09a815c9463/W03-SF408/d13'05_gh_v_vol_plot_daywise_heatmap.py)


- ![Image](https://github.com/ne-5437/25-10-GRNK-GRPI-581-DTML/blob/main/W03-SF408/img209.png?raw=true)


### 🐞 Issues Faced
- Cannot reindex on an axis with duplicate labels during resample → duplicate timestamps per reservoir.
- Sparse points when using merge_asof against static map thinned minute-level rows.
- Overplot clutter in multi-day contour overlays (7 sets of contours looked chaotic).

### ✅ Fixes Applied
- Dedup + sort per UNIT: drop_duplicates(subset="TIMESTAMP", keep="last"); remove any residual dup index.
- Resample to 1T and forward-fill to ensure every minute exists for upper & lower, then compute GH.
- Replace discrete merge_asof with NumPy interpolation np.interp → a mapped volume for every minute.
- Switch from 7-contour overlay (spaghetti) to small-multiple filled KDE heatmaps (one per day).
- For the combined daily comparison: use lines-only regression overlay (clean slopes), and keep dots only when asked.

### 🔁 Updated Observations
- The GH–Volume relation remained highly linear and consistent across the entire month, with weekly slope variations being minimal and within normal operational limits.
- Day-wise KDE and heatmap views showed nearly identical diagonal density bands, confirming stable hydraulic behavior and no visible drift or anomalies through the week.

### 🏷️ Conclusion
The analysis confirms that the GH–Volume correlation is stable, repeatable, and linearly predictable across all time scales examined. Both weekly and day-wise visualizations reinforce that reservoir operation and measurement systems are performing reliably without fluctuation or nonlinear deviations.
