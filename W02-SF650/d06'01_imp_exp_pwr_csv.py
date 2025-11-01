import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    # Load the raw combined dataset
    df = pd.read_csv("combined_output.csv")

    # Convert millisecond timestamp
    df["TIMESTAMP"] = pd.to_datetime(df["pt"], unit="ms", errors="coerce")

    # Select required SIGNAL IDs
    POWER = "AP01.PSP.UNIT1.MW"
    IMPORT = "AP01.PSP.GSUT-1.Gen_MWH_IMPORT"
    EXPORT = "AP01.PSP.GSUT-1.Gen_MWH_EXPORT"

    df = df[df["id"].isin([POWER, IMPORT, EXPORT])].copy()

    # Pivot to wide format
    df_pivot = df.pivot_table(
        index="TIMESTAMP",
        columns="id",
        values="v",
        aggfunc="mean"
    ).reset_index()

    # Rename columns
    df_pivot.rename(columns={
        POWER: "MW",
        IMPORT: "MWH_IMPORT",
        EXPORT: "MWH_EXPORT"
    }, inplace=True)

    # Sort by time and set index
    df_pivot = df_pivot.sort_values("TIMESTAMP").set_index("TIMESTAMP")

    # Resample to 15-minute intervals
    df_15m = pd.DataFrame()
    df_15m["MW"] = df_pivot["MW"].resample("15T").mean()

    # Energy difference per 15 minutes
    df_15m["ΔIMPORT"] = df_pivot["MWH_IMPORT"].resample("15T").last() - df_pivot["MWH_IMPORT"].resample("15T").first()
    df_15m["ΔEXPORT"] = df_pivot["MWH_EXPORT"].resample("15T").last() - df_pivot["MWH_EXPORT"].resample("15T").first()

    # Energy difference may have negative jumps or zeros due to meter rollover
    df_15m["ΔIMPORT"] = df_15m["ΔIMPORT"].where(df_15m["ΔIMPORT"] >= 0)
    df_15m["ΔEXPORT"] = df_15m["ΔEXPORT"].where(df_15m["ΔEXPORT"] >= 0)

    # Convert ΔEnergy to Power (MW)
    df_15m["MW_FROM_IMPORT"] = df_15m["ΔIMPORT"] * 4
    df_15m["MW_FROM_EXPORT"] = df_15m["ΔEXPORT"] * 4

    # Final output file
    output_file = "unit1_power_energy_15min.csv"
    df_15m.to_csv(output_file)
    print("✅ Saved:", output_file)

    # ============================
    # Visualization Section
    # ============================

    plt.figure(figsize=(14,6))
    plt.plot(df_15m.index, df_15m["MW"], label="Actual MW")
    plt.plot(df_15m.index, df_15m["MW_FROM_IMPORT"], linestyle="dashed", label="MW from Import ΔEnergy")
    plt.plot(df_15m.index, df_15m["MW_FROM_EXPORT"], linestyle="dotted", label="MW from Export ΔEnergy")
    plt.xlabel("Time")
    plt.ylabel("MW")
    plt.title("Unit-1 Power: Actual vs Computed from Energy (15-min)")
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(14,6))
    plt.plot(df_15m.index, df_15m["ΔIMPORT"], label="Δ Import MWh")
    plt.plot(df_15m.index, df_15m["ΔEXPORT"], label="Δ Export MWh")
    plt.xlabel("Time")
    plt.ylabel("Energy Δ per 15 min (MWh)")
    plt.title("Energy Change Trend")
    plt.legend()
    plt.grid(True)
    plt.show()

    print("\nSummary:")
    print(df_15m.describe())

    return df_15m, plt


@app.cell
def _(df_15m, plt):
    # Verification: calculate correlation between power and energy-derived estimates
    corr_import = df_15m["MW"].corr(df_15m["MW_FROM_IMPORT"])
    corr_export = df_15m["MW"].corr(df_15m["MW_FROM_EXPORT"])

    print("===== VERIFICATION OF POWER FROM ENERGY =====")
    print(f"Correlation (MW vs Import-based power): {corr_import:.3f}")
    print(f"Correlation (MW vs Export-based power): {corr_export:.3f}")

    # Compute Mean Absolute Error (MW)
    mae_import = (df_15m["MW"] - df_15m["MW_FROM_IMPORT"]).abs().mean()
    mae_export = (df_15m["MW"] - df_15m["MW_FROM_EXPORT"]).abs().mean()

    print(f"\nMean Absolute Error vs Import Power: {mae_import:.2f} MW")
    print(f"Mean Absolute Error vs Export Power: {mae_export:.2f} MW")

    # Scatter plots for visual verification
    plt.figure(figsize=(8,5))
    plt.scatter(df_15m["MW"], df_15m["MW_FROM_IMPORT"], alpha=0.5)
    plt.xlabel("Actual MW")
    plt.ylabel("Computed MW from Import Energy")
    plt.title("Verification: Actual vs Import-derived MW")
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(8,5))
    plt.scatter(df_15m["MW"], df_15m["MW_FROM_EXPORT"], alpha=0.5)
    plt.xlabel("Actual MW")
    plt.ylabel("Computed MW from Export Energy")
    plt.title("Verification: Actual vs Export-derived MW")
    plt.grid(True)
    plt.show()

    return


if __name__ == "__main__":
    app.run()
