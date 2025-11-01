import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import numpy as np

    df = pd.read_csv("merged_output.csv")

    df['id'] = df['id'].astype(str)

    # Timestamp selection: use pt if present else dt
    df['timestamp_ms'] = df['pt'].fillna(df['dt'])

    df['timestamp'] = (
        pd.to_datetime(df['timestamp_ms'], unit='ms')
          .dt.tz_localize('UTC')
          .dt.tz_convert('Asia/Kolkata')
    )

    # Filter only active power measurements: MW
    df = df[df['id'].str.contains(r'\.UNIT\d+\.MW$', regex=True, na=False)]

    # Extract unit name
    df['unit_name'] = df['id'].str.extract(r'(UNIT\d+)')

    # Rename value column to power
    df.rename(columns={'v': 'power_MW'}, inplace=True)

    clean_df = df[['timestamp', 'unit_name', 'power_MW']].sort_values('timestamp').reset_index(drop=True)

    clean_df.to_csv("clean_windmill_data.csv", index=False)

    print("✅ Cleaned result:", clean_df.shape)
    clean_df.head(20)

    return


if __name__ == "__main__":
    app.run()
