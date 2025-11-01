import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt

    # Load dataset
    df = pd.read_csv("structured_output2.csv")

    # Fix timestamps
    df["timestamps"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")

    # Set datetime index
    df.set_index("timestamps", inplace=True)

    # Unit power columns
    unit_cols = [col for col in df.columns if col.endswith("_MW")]

    # Resample to minute, hour, day → null counts
    null_minute = df[unit_cols].isna().resample("1min").sum()
    null_hour   = df[unit_cols].isna().resample("1H").sum()
    null_day    = df[unit_cols].isna().resample("1D").sum()

    plots = [
        ("Null Count Per Minute", null_minute),
        ("Null Count Per Hour", null_hour),
        ("Null Count Per Day", null_day)
    ]

    # Plot for each aggregation level
    for title, data in plots:
        for col in unit_cols:
            plt.figure(figsize=(14,4))
            plt.plot(data.index, data[col])
            plt.title(f"{title} — {col}")
            plt.ylabel("Null Count")
            plt.xlabel("Time")
            plt.grid(True)
            plt.tight_layout()
            plt.show()

    return


if __name__ == "__main__":
    app.run()
