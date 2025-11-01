import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    def safe_read_csv(path):
        return pd.read_csv(path, sep=None, engine="python", on_bad_lines="skip")

    # --- Load data ---
    df_temp = safe_read_csv("X-Minutal.csv")
    df_alarm = safe_read_csv("Full AWS.csv")

    df_temp.columns = df_temp.columns.str.strip()
    df_alarm.columns = df_alarm.columns.str.strip()

    device_id = "G97-N24"
    col_name = "Bearing D.E. Temperature max 10M (ºC)"

    # --- Filter by device ---
    df_temp = df_temp[df_temp["﻿Device"] == device_id].copy()
    df_temp["Date"] = pd.to_datetime(df_temp["Date"], errors="coerce", dayfirst=True)
    df_alarm = df_alarm[df_alarm["Device"] == device_id].copy()
    df_alarm["Start Date"] = pd.to_datetime(df_alarm["Start Date"], errors="coerce", dayfirst=True)
    df_alarm["End Date"] = pd.to_datetime(df_alarm["End Date"], errors="coerce", dayfirst=True)

    # --- Filter April 2024 ---
    df_temp = df_temp[(df_temp["Date"] >= "2024-04-01") & (df_temp["Date"] <= "2024-04-30")][["Date", col_name]].dropna()
    df_alarm = df_alarm[(df_alarm["Start Date"] >= "2024-04-01") & (df_alarm["Start Date"] <= "2024-04-30")]

    # --- Separate warnings and alarms ---
    warnings = df_alarm[df_alarm["Category"].str.contains("Warning", case=False, na=False)]
    alarms = df_alarm[df_alarm["Category"].str.contains("Alarm", case=False, na=False)]

    # --- Extract temperatures for periods ---
    def extract_period_values(period_df):
        vals = []
        for _, row in period_df.iterrows():
            mask = (df_temp["Date"] >= row["Start Date"]) & (df_temp["Date"] <= row["End Date"])
            vals.extend(df_temp.loc[mask, col_name].values)
        return np.array(vals)

    warning_values = extract_period_values(warnings)
    alarm_values = extract_period_values(alarms)

    # --- Normal values outside warning/alarm periods ---
    combined_warn_alarm = np.concatenate([warning_values, alarm_values]) if (warning_values.size + alarm_values.size) > 0 else np.array([])
    normal_values = df_temp[~df_temp[col_name].isin(combined_warn_alarm)][col_name].values

    # --- Threshold calculation using Mean ± k·Std ---
    # Scale factors chosen to naturally produce Normal < Warning < Alarm
    k_normal = 1
    k_warning = 2
    k_alarm = 3

    # Normal operating range
    normal_mean = np.mean(normal_values)
    normal_std = np.std(normal_values)
    normal_min = normal_mean - 2*k_normal*normal_std 
    normal_max = normal_mean + k_normal*normal_std

    # Warning threshold (mean ± k·std over warning values)
    if warning_values.size > 0:
        warn_mean = np.mean(warning_values)
        warn_std = np.std(warning_values)
        warning_min = warn_mean - k_normal*warn_std
        warning_max = warn_mean + k_warning*warn_std
    else:
        # fallback: slightly above normal
        warning_min = normal_max
        warning_max = normal_max + 2

    # Alarm threshold (mean ± k·std over alarm values)
    if alarm_values.size > 0:
        alarm_mean = np.mean(alarm_values)
        alarm_std = np.std(alarm_values)
        alarm_min = alarm_mean - k_warning*alarm_std
        alarm_max = alarm_mean + k_alarm*alarm_std
    else:
        # fallback: slightly above warning
        alarm_min = warning_max
        alarm_max = warning_max + 2

    # --- Print results ---
    print("=== Mean ± k·Std Dev Thresholds ===")
    print(f"Normal Operating Range: {normal_min:.2f} °C → {normal_max:.2f} °C")
    print(f"Warning Threshold:      {warning_min:.2f} °C")
    print(f"Alarm Threshold:        {alarm_max:.2f} °C")

    plt.figure(figsize=(14,6))
    plt.plot(df_temp["Date"], df_temp[col_name], label="Bearing D.E. Temp", color="black", linewidth=1.2)

    # Normal range lines
    plt.axhline(normal_min, color="green", linestyle="--", label="Normal Min")
    plt.axhline(normal_max, color="green", linestyle="--", label="Normal Max")

    # Warning threshold lines
    plt.axhline(warning_min, color="orange", linestyle="--", label="Warning Threshold")

    # Alarm threshold lines
    plt.axhline(alarm_max, color="red", linestyle="--", label="Alarm Threshold")

    plt.title(f"{device_id} — Bearing D.E. Temperature (Apr 2024)")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    return


if __name__ == "__main__":
    app.run()
