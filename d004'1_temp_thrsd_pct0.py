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

    # Load temperature data
    df_temp = safe_read_csv("X-Minutal.csv")
    df_temp.columns = df_temp.columns.str.strip()

    device_id = "G97-N24"
    col_name = "Bearing D.E. Temperature max 10M (ºC)"

    df_temp = df_temp[df_temp["﻿Device"] == device_id].copy()
    df_temp["Date"] = pd.to_datetime(df_temp["Date"], errors="coerce", dayfirst=True)

    # Filter April 2024
    mask_temp = (df_temp["Date"] >= "2024-04-01") & (df_temp["Date"] <= "2024-04-30")
    df_temp = df_temp.loc[mask_temp, ["Date", col_name]].dropna()

    values = df_temp[col_name].values

    # --- Compute thresholds using percentiles ---
    normal_min = np.min(values)
    normal_max = np.percentile(values, 75)
    warning_thr = np.percentile(values, 90)
    alarm_thr = np.percentile(values, 98)  # use 98th percentile to avoid extreme outliers

    # Tensor for ML
    temp_tensor = tf.constant(values, dtype=tf.float32)

    # --- Plot ---
    plt.figure(figsize=(12, 6))
    plt.plot(df_temp["Date"], values, label="Bearing D.E. Temp", linewidth=1.4)

    plt.axhline(normal_min, color="green", linestyle="--", label="Normal Min")
    plt.axhline(normal_max, color="green", linestyle="--", label="Normal Max")
    plt.axhline(warning_thr, color="orange", linestyle="--", label="Warning Threshold")
    plt.axhline(alarm_thr, color="red", linestyle="--", label="Alarm Threshold")

    plt.title(f"{device_id} — Bearing D.E. Temperature (Apr 2024)")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # --- Print thresholds ---
    print("\n=== Data-Driven Thresholds (Apr 2024) ===")
    print(f"Normal Operating Range:  {normal_min:.2f} - {normal_max:.2f} °C")
    print(f"Warning Threshold:     {normal_max:.2f} °C")
    print(f"Alarm Threshold:       {warning_thr:.2f} °C")

    return


if __name__ == "__main__":
    app.run()
