import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    # ==========================================
    # 1. Load CSV
    # ==========================================
    df = pd.read_csv("turbine_minute_filtered.csv")

    # Ensure correct timestamp format
    timestamp_col = "TIMESTAMP"
    df[timestamp_col] = pd.to_datetime(df[timestamp_col], utc=True)
    df = df.set_index(timestamp_col).sort_index()

    # Rename for convenience
    df.rename(columns={
        "AP01.PSP.GSUT-1.Gen_MWH_IMPORT": "IMPORT",
        "AP01.PSP.GSUT-1.Gen_MWH_EXPORT": "EXPORT"
    }, inplace=True)

    # Drop any empty rows or duplicates
    df = df.dropna(subset=["IMPORT", "EXPORT"]).drop_duplicates()

    # ==========================================
    # 2. Classify Modes
    # PUMP mode: IMPORT > 0 and EXPORT == 0
    # GEN mode : EXPORT > 0 and IMPORT == 0
    # ==========================================
    conditions = [
        (df["IMPORT"] > 0) & (df["EXPORT"] == 0),
        (df["IMPORT"] == 0) & (df["EXPORT"] > 0)
    ]
    choices = ["PUMP", "GEN"]
    df["MODE"] = np.select(conditions, choices, "IDLE/ERROR")

    # Summary
    print("\n===== Mode Summary =====")
    print(df["MODE"].value_counts())

    # ==========================================
    # 3. Convert power to energy per minute (MWh)
    # Power (MW) × (1/60) hr = MWh per minute
    # ==========================================
    df["IMPORT_MWh"] = df["IMPORT"].clip(lower=0) * (1/60)
    df["EXPORT_MWh"] = df["EXPORT"].clip(lower=0) * (1/60)

    # Total energy metrics
    total_import = df["IMPORT_MWh"].sum()
    total_export = df["EXPORT_MWh"].sum()

    efficiency = (total_export / total_import) * 100

    print(f"\nTotal Import Energy   = {total_import:.3f} MWh")
    print(f"Total Export Energy   = {total_export:.3f} MWh")
    print(f"Round Trip Efficiency = {efficiency:.2f}%\n")

    # ==========================================
    # 4. Inefficiency Detection Rules
    # Rule 1: GEN mode but EXPORT < threshold (stalled turbine)
    # Rule 2: PUMP mode but IMPORT spike without expected return later
    # ==========================================

    # Rule 1 threshold
    low_export_threshold = df["EXPORT"].quantile(0.05)  # bottom 5 percent
    rule1 = df[(df["MODE"] == "GEN") & (df["EXPORT"] < low_export_threshold)]

    print("===== Generation Anomalies (Rule 1: Low Export) =====")
    print(rule1[["IMPORT","EXPORT","MODE"]].head(), "\n")

    # ==========================================
    # 5. Power Trend Plot
    # ==========================================
    plt.figure(figsize=(22,6))
    plt.plot(df.index, df["IMPORT"], label="Import Power (MW)")
    plt.plot(df.index, df["EXPORT"], label="Export Power (MW)")

    # Highlight pump/generation transitions
    pump = df[df["MODE"] == "PUMP"]
    gen  = df[df["MODE"] == "GEN"]

    plt.scatter(pump.index, pump["IMPORT"], s=5, color="cyan", label="Pump Mode")
    plt.scatter(gen.index, gen["EXPORT"], s=5, color="yellow", label="Generation Mode")

    plt.title("Power Trend: Pump vs Generation")
    plt.xlabel("Time")
    plt.ylabel("Power (MW)")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # ==========================================
    # 6. Efficiency Rolling Trend (Optional Insight)
    # Efficiency is only meaningful across full cycles
    # This rolling ratio shows local return performance
    # ==========================================
    df["Rolling_RTOE"] = (df["EXPORT_MWh"].rolling(180).sum() /
                          df["IMPORT_MWh"].rolling(180).sum()) * 100

    plt.figure(figsize=(22,6))
    plt.plot(df.index, df["Rolling_RTOE"], linewidth=1.2)
    plt.axhline(efficiency, color="red", linestyle="--",
                label=f"Overall Efficiency ({efficiency:.1f}%)")
    plt.title("Rolling Round Trip Efficiency (180-minute window)")
    plt.xlabel("Time")
    plt.ylabel("Efficiency %")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return df, pd


@app.cell
def _(df, pd):
    df["is_pump"] = (df["MODE"] == "PUMP").astype(int)
    df["pump_group"] = (df["is_pump"].diff() == 1).cumsum()

    cycles = []
    for g, data in df.groupby("pump_group"):
        pump_time = (data["MODE"] == "PUMP").sum()
        gen_time = (data["MODE"] == "GEN").sum()
        if pump_time > 0:
            ratio = gen_time / pump_time
            cycles.append({
                "Cycle_ID": g,
                "Pump_Time_min": pump_time,
                "Gen_Time_min": gen_time,
                "Time_Efficiency_Ratio": ratio,
                "Status": "Inefficient" if ratio < 0.7 else "OK"
            })

    cycle_df = pd.DataFrame(cycles)
    print("\n===== Cycle Duration Efficiency Report =====")
    print(cycle_df)

    return


if __name__ == "__main__":
    app.run()
