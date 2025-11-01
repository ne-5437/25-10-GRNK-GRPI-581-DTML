import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    # ------- Load Data ------- #
    df = pd.read_csv("turbine_minute_filtered.csv")

    # Force timestamp to datetime
    df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"], utc=True)

    # Auto-detect import/export columns
    import_col = [c for c in df.columns if "IMPORT" in c.upper()]
    export_col = [c for c in df.columns if "EXPORT" in c.upper()]

    if len(import_col) != 1 or len(export_col) != 1:
        raise ValueError(f"Expected exactly 1 Import and 1 Export column. Found: {import_col}, {export_col}")

    IMPORT = import_col[0]
    EXPORT = export_col[0]

    print(f"Detected Import Column: {IMPORT}")
    print(f"Detected Export Column: {EXPORT}")

    # Keep only required columns
    df = df[["TIMESTAMP", IMPORT, EXPORT]].sort_values("TIMESTAMP").reset_index(drop=True)

    # ------- Mode Classification ------- #
    def classify(row):
        imp, exp = row[IMPORT], row[EXPORT]

        if np.isnan(imp) and np.isnan(exp):
            return "MISSING"
        if not np.isnan(imp) and np.isnan(exp):
            return "PUMPING"
        if not np.isnan(exp) and np.isnan(imp):
            return "GENERATION"
        if not np.isnan(imp) and not np.isnan(exp):
            return "CONFLICT"
        return "UNKNOWN"

    df["MODE"] = df.apply(classify, axis=1)

    # Remove missing-only rows but preserve cycles
    df_valid = df[df["MODE"] != "MISSING"].copy()

    # ------- Cycle Grouping ------- #
    df_valid["CYCLE_GROUP"] = (df_valid["MODE"] != df_valid["MODE"].shift()).cumsum()

    cycles = (
        df_valid.groupby("CYCLE_GROUP")
        .agg(Start=("TIMESTAMP","first"),
             End=("TIMESTAMP","last"),
             Duration_min=("TIMESTAMP",lambda x:(x.iloc[-1]-x.iloc[0]).total_seconds()/60),
             MODE=("MODE","first"))
    )

    cycles = cycles[cycles["MODE"].isin(["PUMPING","GENERATION"])]

    print("\n===== Cycle Summary =====")
    print(cycles.head())

    # ------- Efficiency where both exist ------- #
    df_valid["EFFICIENCY"] = np.where(
        (~df_valid[IMPORT].isna()) & (~df_valid[EXPORT].isna()),
        (df_valid[EXPORT] / (df_valid[IMPORT] + df_valid[EXPORT])) * 100,
        np.nan
    )

    print("\n===== Efficiency Stats =====")
    print(df_valid["EFFICIENCY"].describe())

    # ------- Plotting Section ------- #
    plt.figure(figsize=(18,6))
    plt.plot(df["TIMESTAMP"], df[IMPORT], alpha=0.8, label="IMPORT")
    plt.plot(df["TIMESTAMP"], df[EXPORT], alpha=0.8, label="EXPORT")
    plt.title("Power Trends Over Time")
    plt.legend()
    plt.xlabel("Time")
    plt.ylabel("MW")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(18,3))
    plt.scatter(df_valid["TIMESTAMP"], df_valid["MODE"], s=6)
    plt.title("Operating Mode Timeline")
    plt.tight_layout()
    plt.show()

    eff_df = df_valid.dropna(subset=["EFFICIENCY"])
    plt.figure(figsize=(18,4))
    plt.plot(eff_df["TIMESTAMP"], eff_df["EFFICIENCY"])
    plt.title("Efficiency Overlaps Only")
    plt.ylabel("Efficiency (%)")
    plt.tight_layout()
    plt.show()

    print("\n✅ Completed Successfully")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
