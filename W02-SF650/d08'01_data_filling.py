import numpy as np
import pandas as pd


def conditional_linearinterpolation_fill(series, timestamps, max_gap_seconds=900):
    s = series.to_numpy(copy=True)
    mask = np.isnan(s)
    if not np.any(mask):
        return series
    isnan = np.concatenate(([False], mask, [False]))
    starts = np.flatnonzero(~isnan[:-1] & isnan[1:])
    ends = np.flatnonzero(isnan[:-1] & ~isnan[1:])
    for start, end in zip(starts, ends):
        if start > 0 and end < len(s):
            time_gap = (timestamps[end] - timestamps[start - 1]) / np.timedelta64(
                1, "s"
            )
            if np.sign(s[start - 1]) == np.sign(s[end]) and time_gap <= max_gap_seconds:
                t1, t2 = timestamps[start - 1], timestamps[end]
                v1, v2 = s[start - 1], s[end]

                interp_times = timestamps[start:end]
                s[start:end] = v1 + (v2 - v1) * (
                    (interp_times - t1) / (t2 - t1)
                ).astype(float)
    return pd.Series(s, index=series.index)


def conditional_forward_fill(series, timestamps, max_gap_seconds=900):
    """
    Fills NaN values using forward fill if the values on both sides of the missing timestamps
    have the same sign. The filling is applied only when the time gap between the two known
    values is less than or equal to 900 seconds.
    """
    s = series.to_numpy(copy=True)
    mask = np.isnan(s)
    if not np.any(mask):
        return series
    isnan = np.concatenate(([False], mask, [False]))
    starts = np.flatnonzero(~isnan[:-1] & isnan[1:])
    ends = np.flatnonzero(isnan[:-1] & ~isnan[1:])
    for start, end in zip(starts, ends):
        if start > 0 and end < len(s):
            time_gap = (timestamps[end] - timestamps[start - 1]) / np.timedelta64(
                1, "s"
            )
            if np.sign(s[start - 1]) == np.sign(s[end]) and time_gap <= max_gap_seconds:
                s[start:end] = s[start - 1]
    return pd.Series(s, index=series.index)


df_cpss_energy_import = (
    df_cpss_energy_import.pivot(
        index="TIMESTAMP", columns="UNIT", values="cpss_import_energy"
    )
    .sort_index()
    .reset_index()
)
print(df_cpss_energy_import.head(50))
full_index = pd.date_range(
    start=df_cpss_energy_import["TIMESTAMP"].min(),
    end=df_cpss_energy_import["TIMESTAMP"].max(),
    freq="1S",
)
full_df = pd.DataFrame({"TIMESTAMP": full_index})
unit_full = pd.merge(full_df, df_cpss_energy_import, on="TIMESTAMP", how="left")
cols = unit_full.columns.difference(["TIMESTAMP"])
timestamps_np = unit_full["TIMESTAMP"].values
unit_full[cols] = unit_full[cols].apply(
    lambda s: conditional_linearinterpolation_fill(s, timestamps_np)
)
unit_full = unit_full.set_index("TIMESTAMP")
