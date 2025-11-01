import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import tensorflow as tf
    import matplotlib.pyplot as plt


    def safe_read_csv(path):
        return pd.read_csv(path, sep=None, engine="python", on_bad_lines="skip")

    df_temp = safe_read_csv("X-Minutal.csv")   
    df_alarm = safe_read_csv("Full AWS.csv")   


    df_temp.columns = df_temp.columns.str.strip()
    df_alarm.columns = df_alarm.columns.str.strip()


    device_id = "G97-N24"
    df_temp = df_temp[df_temp["﻿Device"] == device_id].copy()
    df_alarm = df_alarm[df_alarm["Device"] == device_id].copy()


    df_temp["Date"] = pd.to_datetime(df_temp["Date"], errors="coerce", dayfirst=True)
    df_alarm["Start Date"] = pd.to_datetime(df_alarm["Start Date"], errors="coerce", dayfirst=True)
    df_alarm["End Date"] = pd.to_datetime(df_alarm["End Date"], errors="coerce", dayfirst=True)


    mask_temp = (df_temp["Date"] >= "2024-04-01") & (df_temp["Date"] <= "2024-04-30")
    mask_alarm = (df_alarm["Start Date"] >= "2024-04-01") & (df_alarm["Start Date"] <= "2024-04-30")
    df_temp = df_temp.loc[mask_temp]
    df_alarm = df_alarm.loc[mask_alarm]


    col_name = "Bearing D.E. Temperature max 10M (ºC)"
    df_temp = df_temp[["Date", col_name]].dropna()


    alarms = df_alarm[df_alarm["Category"].str.contains("Alarm", case=False, na=False)]
    warnings = df_alarm[df_alarm["Category"].str.contains("Warning", case=False, na=False)]


    alarm_periods = []
    warning_periods = []

    for _, row in alarms.iterrows():
        mask = (df_temp["Date"] >= row["Start Date"]) & (df_temp["Date"] <= row["End Date"])
        alarm_periods.append(df_temp.loc[mask, col_name].values)

    for _, row in warnings.iterrows():
        mask = (df_temp["Date"] >= row["Start Date"]) & (df_temp["Date"] <= row["End Date"])
        warning_periods.append(df_temp.loc[mask, col_name].values)

    import numpy as np
    alarm_values = np.concatenate(alarm_periods) if alarm_periods else np.array([])
    warning_values = np.concatenate(warning_periods) if warning_periods else np.array([])

    alarm_min = alarm_values.min() if alarm_values.size > 0 else None
    alarm_max = alarm_values.max() if alarm_values.size > 0 else None
    warn_min = warning_values.min() if warning_values.size > 0 else None
    warn_max = warning_values.max() if warning_values.size > 0 else None

    print("\n=== Bearing D.E. Temperature Thresholds for April 2024 ===")
    print(f"Alarm range (°C): {alarm_min} – {alarm_max}")
    print(f"Warning range (°C): {warn_min} – {warn_max}")


    temp_tensor = tf.constant(df_temp[col_name].values, dtype=tf.float32)


    plt.figure(figsize=(12, 6))
    plt.plot(df_temp["Date"], df_temp[col_name], label="Bearing D.E. Temp (max 10M)", color="teal")
    if warn_min is not None:
        plt.axhline(warn_min, color="yellow", linestyle="--", label="Warning Min")
        plt.axhline(warn_max, color="gold", linestyle="--", label="Warning Max")
    if alarm_min is not None:
        plt.axhline(alarm_min, color="red", linestyle="--", label="Alarm Min")
        plt.axhline(alarm_max, color="darkred", linestyle="--", label="Alarm Max")

    plt.title(f"Device {device_id} — Bearing D.E. Temperature (Apr 2024)")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return alarm_max, alarm_min, col_name, device_id, warn_max, warn_min


@app.cell
def _(alarm_max, alarm_min, col_name, device_id, warn_max, warn_min):
    print("\n=== Summary of April 2024 Temperature Ranges ===")
    print(f"Device: {device_id}")
    print(f"Parameter: {col_name}")
    print(f"Warning Range : {warn_min:.2f} °C – {warn_max:.2f} °C")
    print(f"Alarm Range   : {alarm_min:.2f} °C – {alarm_max:.2f} °C")

    return


if __name__ == "__main__":
    app.run()
