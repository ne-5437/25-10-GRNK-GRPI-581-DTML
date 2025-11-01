import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import numpy as np

    # Load with correct timestamp + unit_name + power_MW
    df = pd.read_csv("clean_windmill_data.csv")

    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])
    df = df.sort_values(['unit_name', 'timestamp'])

    result = []

    for unit, unit_df in df.groupby('unit_name'):
        unit_df = unit_df.set_index('timestamp')

        # ✅ Collapse duplicates per second: take last known value
        unit_df = unit_df[~unit_df.index.duplicated(keep='last')]

        # ✅ Set target frequency to 1 second
        per_sec = unit_df.resample("1s").ffill()

        # ✅ Identify gaps ≥ 5 minutes → break forward fill
        gap_mask = per_sec.index.to_series().diff() > pd.Timedelta(minutes=5)
        per_sec.loc[gap_mask] = np.nan

        per_sec['unit_name'] = unit
        result.append(per_sec)

    final_df = pd.concat(result).reset_index()
    final_df.rename(columns={"index": "timestamp"}, inplace=True)

    # ✅ Save output
    out_file = "windmill_1sec_cleaned.csv"
    final_df.to_csv(out_file, index=False)

    print("✅ Output saved to:", out_file)
    print("✅ Total rows:", len(final_df))
    print(final_df.head())

    return


if __name__ == "__main__":
    app.run()
