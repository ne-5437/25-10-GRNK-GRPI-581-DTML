import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    # Standalone Marimo cell — full analytics for minute-level import/export CSV
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import os

    # ------- CONFIG -------
    INPUT_CSV = "turbine_minute_filtered.csv"   # adjust if filename differs
    OUTPUT_SUMMARY = "turbine_analysis_summary.csv"
    # ----------------------

    # 1) Load file (standalone)
    if not os.path.exists(INPUT_CSV):
        raise FileNotFoundError(f"Input file not found: {INPUT_CSV}")

    df_raw = pd.read_csv(INPUT_CSV)

    # 2) Auto-detect import/export column names (flexible)
    cols = df_raw.columns.tolist()
    # find columns that contain 'IMPORT' and 'EXPORT' (case-insensitive)
    import_col = next((c for c in cols if "IMPORT" in c.upper()), None)
    export_col = next((c for c in cols if "EXPORT" in c.upper()), None)

    if import_col is None or export_col is None:
        raise ValueError(f"Could not find IMPORT/EXPORT columns in {INPUT_CSV}. Found columns: {cols}")

    # 3) Prepare dataframe
    df = df_raw.copy()
    df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"], errors="coerce", utc=True)
    df = df.dropna(subset=["TIMESTAMP"]).sort_values("TIMESTAMP").reset_index(drop=True)

    # Normalize column names for processing
    df = df.rename(columns={import_col: "IMPORT", export_col: "EXPORT"})

    # Convert to numeric, keep NaN if parsing fails
    df["IMPORT"] = pd.to_numeric(df["IMPORT"], errors="coerce")
    df["EXPORT"] = pd.to_numeric(df["EXPORT"], errors="coerce")

    # 4) Compute per-minute deltas (energy increments)
    # Deltas are meaningful for cumulative counters; negative deltas indicate resets — mark as NaN
    df["dIMPORT"] = df["IMPORT"].diff()
    df["dEXPORT"] = df["EXPORT"].diff()

    df.loc[df["dIMPORT"] < 0, "dIMPORT"] = np.nan
    df.loc[df["dEXPORT"] < 0, "dEXPORT"] = np.nan

    # Replace very small negative/positive numerical noise with 0 if needed (optional)
    # df["dIMPORT"] = df["dIMPORT"].apply(lambda x: 0 if abs(x) < 1e-9 else x)
    # df["dEXPORT"] = df["dEXPORT"].apply(lambda x: 0 if abs(x) < 1e-9 else x)

    # 5) Net energy and efficiency
    df["NET"] = df["dEXPORT"].fillna(0) - df["dIMPORT"].fillna(0)
    # Efficiency defined per minute where import > 0: export/import
    df["EFF"] = np.where(df["dIMPORT"] > 0, df["dEXPORT"] / df["dIMPORT"], np.nan)

    # 6) Mode classification (robust)
    def classify_mode(r):
        di = r["dIMPORT"]
        de = r["dEXPORT"]
        # If both NaN -> likely data gap / both counters missing
        if pd.isna(di) and pd.isna(de):
            return "ERROR"
        # If export increased and import not increased
        if (not pd.isna(de) and de > 0) and (pd.isna(di) or di == 0):
            return "GENERATION"
        # If import increased and export not increased
        if (not pd.isna(di) and di > 0) and (pd.isna(de) or de == 0):
            return "PUMPING"
        # If both zero or very small -> idle
        if (pd.isna(di) or di == 0) and (pd.isna(de) or de == 0):
            return "IDLE"
        # If both increased simultaneously (rare) treat as TRANSITION/RECONCILE
        if (not pd.isna(di) and di > 0) and (not pd.isna(de) and de > 0):
            return "BOTH_INC"
        return "UNKNOWN"

    df["MODE"] = df.apply(classify_mode, axis=1)

    # 7) Print quick summaries
    print("\n=== File and columns ===")
    print("Input file:", INPUT_CSV)
    print("Detected IMPORT column:", import_col)
    print("Detected EXPORT column:", export_col)
    print("\n=== Mode counts ===")
    print(df["MODE"].value_counts(dropna=False))

    print("\n=== Efficiency summary (where import>0) ===")
    print(df["EFF"].describe())

    # 8) Save a compact diagnostics CSV (first/last 100 rows not to be huge)
    diag = df[["TIMESTAMP", "IMPORT", "EXPORT", "dIMPORT", "dEXPORT", "NET", "EFF", "MODE"]]
    diag.to_csv(OUTPUT_SUMMARY, index=False)
    print(f"\nDiagnostics saved to: {OUTPUT_SUMMARY}")

    # -----------------------
    # 9) PLOTTING (clear line plots)
    # -----------------------
    plt.rcParams.update({'figure.facecolor':'white'})  # ensure readable backg

    return


if __name__ == "__main__":
    app.run()
