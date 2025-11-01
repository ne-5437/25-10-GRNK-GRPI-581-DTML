import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import numpy as np

    # Load combined dataset
    df = pd.read_csv("combined_output.csv")

    # Convert timestamp from pt milliseconds to datetime
    df["TIMESTAMP"] = pd.to_datetime(df["pt"], unit="ms", errors="coerce", utc=True)
    df = df.dropna(subset=["TIMESTAMP"])

    # Filter required signals
    required_ids = [
        "AP01.PSP.GSUT-1.Gen_MWH_IMPORT",
        "AP01.PSP.GSUT-1.Gen_MWH_EXPORT"
    ]

    df = df[df["id"].isin(required_ids)]

    # Replace zero values with NaN (for ignoring in mean)
    df["v"] = df["v"].replace(0, np.nan)

    # Convert to minute timestamps
    df["TIMESTAMP"] = df["TIMESTAMP"].dt.floor("min")

    # Pivot table to wide format: timestamp vs values
    df_wide = df.pivot_table(
        index="TIMESTAMP",
        columns="id",
        values="v",
        aggfunc="mean"
    )

    # Sort by timestamp
    df_wide = df_wide.sort_index()

    # Save result
    output_file = "turbine_minute_filtered.csv"
    df_wide.to_csv(output_file, index=True, index_label="TIMESTAMP")

    print("✅ Completed and saved:", output_file)
    print("✅ Final shape:", df_wide.shape)
    df_wide.head()
    return


if __name__ == "__main__":
    app.run()
