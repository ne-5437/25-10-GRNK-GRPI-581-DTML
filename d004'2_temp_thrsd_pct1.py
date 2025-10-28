import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import tensorflow as tf

    def safe_read_csv(path):
        return pd.read_csv(path, sep=None, engine="python", on_bad_lines="skip")

    # Load data
    df_temp = safe_read_csv("X-Minutal.csv")
    df_alarm = safe_read_csv("Full AWS.csv")

    df_temp.columns = df_temp.columns.str.strip()
    df_alarm.columns = df_alarm.columns.str.strip()

    device_id = "G97-N24"
    col_name = "Bearing D.E. Temperature max 10M (ºC)"

    df_temp = df_temp[df_temp["﻿Device"] == device_id].copy()
    df_temp["Date"] = pd.to_datetime(df_temp["Date"], errors="coerce", dayfirst=True)
    df_alarm = df_alarm[df_alarm["Device"] == device_id].copy()
    df_alarm["Start Date"] = pd.to_datetime(df_alarm["Start Date"], errors="coerce", dayfirst=True)
    df_alarm["End Date"] = pd.to_datetime(df_alarm["End Date"], errors="coerce", dayfirst=True)

    # Filter April 2024
    mask_temp = (df_temp["Date"] >= "2024-04-01") & (df_temp["Date"] <= "2024-04-30")
    mask_alarm = (df_alarm["Start Date"] >= "2024-04-01") & (df_alarm["Start Date"] <= "2024-04-30")
    df_temp = df_temp.loc[mask_temp, ["Date", col_name]].dropna()
    df_alarm = df_alarm.loc[mask_alarm]

    # Separate warnings and alarms
    warnings = df_alarm[df_alarm["Category"].str.contains("Warning", case=False, na=False)]
    alarms = df_alarm[df_alarm["Category"].str.contains("Alarm", case=False, na=False)]

    # Extract temperatures for each period
    def extract_period_values(period_df):
        vals = []
        for _, row in period_df.iterrows():
            mask = (df_temp["Date"] >= row["Start Date"]) & (df_temp["Date"] <= row["End Date"])
            vals.extend(df_temp.loc[mask, col_name].values)
        return np.array(vals)

    warning_values = extract_period_values(warnings)
    alarm_values = extract_period_values(alarms)

    # Normal values are outside warning/alarm periods
    combined_warn_alarm = np.concatenate([warning_values, alarm_values]) if (warning_values.size + alarm_values.size) > 0 else np.array([])
    normal_values = df_temp[~df_temp[col_name].isin(combined_warn_alarm)][col_name].values

    # --- Thresholds ---
    normal_min = normal_values.min() if normal_values.size > 0 else df_temp[col_name].min()
    normal_max = normal_values.max() if normal_values.size > 0 else df_temp[col_name].max()

    # For warning and alarm, use percentile to avoid cooling-down issue
    warning_thr = np.percentile(warning_values, 90) if warning_values.size > 0 else normal_max + 2
    alarm_thr = np.percentile(alarm_values, 98) if alarm_values.size > 0 else warning_thr + 2

    # Tensor for ML
    temp_tensor = tf.constant(df_temp[col_name].values, dtype=tf.float32)

    # --- Plot ---
    plt.figure(figsize=(12, 6))
    plt.plot(df_temp["Date"], df_temp[col_name], label="Bearing D.E. Temp", linewidth=1.4)

    plt.axhline(normal_max, color="green", linestyle="--", label="Normal Max")
    plt.axhline(warning_thr, color="orange", linestyle="--", label="Warning Threshold")
    plt.axhline(alarm_thr, color="red", linestyle="--", label="Alarm Threshold")

    plt.title(f"{device_id} — Bearing D.E. Temperature (Apr 2024) [Using AWS Logs]")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # --- Print thresholds ---
    print("\n=== Thresholds Using Full AWS.csv (Apr 2024) ===")
    print(f"Normal Operating Min:  {normal_min:.2f} °C")
    print(f"Normal Operating Max:  {normal_max:.2f} °C")
    print(f"Warning Threshold:     >{normal_max:.2f} °C and ≤{warning_thr:.2f} °C")
    print(f"Alarm Threshold:       >{warning_thr:.2f} °C and ≤{alarm_thr:.2f} °C")

    return


if __name__ == "__main__":
    app.run()
