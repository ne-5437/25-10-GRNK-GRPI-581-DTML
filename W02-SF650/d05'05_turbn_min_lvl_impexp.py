import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import numpy as np

    # Load previously filtered file
    df = pd.read_csv("turbine_filtered.csv")

    # Ensure proper datetime conversion
    df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"], errors="coerce", utc=True)

    # Remove rows where timestamp failed conversion
    df = df.dropna(subset=["TIMESTAMP"])

    # Floor to minute resolution
    df["TIMESTAMP"] = df["TIMESTAMP"].dt.floor("min")

    # Columns to process
    value_cols = ["GSUT-1_Gen_MWH_IMPORT", "UNIT1_UFMS_DISCHARGE_FLOW"]

    # Ignore zero values when averaging
    df[value_cols] = df[value_cols].replace(0, np.nan)

    # Group by minute
    df_minute = df.groupby("TIMESTAMP")[value_cols].mean()

    # Sort by timestamp
    df_minute = df_minute.sort_index()

    # Save final dataset
    df_minute.to_csv("turbine_minute_level.csv", index=True, index_label="TIMESTAMP")

    print("✅ Minute-level dataset saved as turbine_minute_level.csv")
    print("Final shape:", df_minute.shape)

    return


if __name__ == "__main__":
    app.run()
