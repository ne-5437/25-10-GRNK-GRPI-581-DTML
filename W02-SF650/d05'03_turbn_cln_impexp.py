import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd

    # 1. Load the combined input
    df = pd.read_csv("combined_output.csv")

    # 2. Convert timestamp from pt (UNIX ms) to datetime UTC
    df['TIMESTAMP'] = pd.to_datetime(df['pt'], unit='ms', utc=True, errors='coerce')

    # Remove rows without valid timestamp
    df = df.dropna(subset=['TIMESTAMP'])

    # 3. Split the signal ID into components
    split_cols = df['id'].str.split('.', expand=True)
    df['PLANT'] = split_cols[0]
    df['TYPE'] = split_cols[1]
    df['UNIT'] = split_cols[2]
    df['PARAMETER'] = split_cols[3]

    # 4. Create a unique tag for pivoting
    df['TAG'] = df['UNIT'] + "_" + df['PARAMETER']

    # 5. Pivot to wide format
    pivot_df = df.pivot_table(
        index='TIMESTAMP',
        columns='TAG',
        values='v',
        aggfunc='mean'  # mean removes duplicate timestamps per parameter
    )

    # 6. Sort by timestamp
    pivot_df = pivot_df.sort_index()

    # 7. Remove any duplicate timestamps (after pivot)
    pivot_df = pivot_df[~pivot_df.index.duplicated(keep='first')]

    # 8. Save final cleaned dataset
    pivot_df.to_csv("turbine_clean.csv", index=True, index_label="TIMESTAMP")

    print("Final cleaned dataset saved as turbine_clean.csv")
    print("Final Shape:", pivot_df.shape)

    return


if __name__ == "__main__":
    app.run()
