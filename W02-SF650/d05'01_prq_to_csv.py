import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import os
    import pandas as pd

    parquet_dir = r"D:\raw_data"

    parquet_files = [f for f in os.listdir(parquet_dir) if f.endswith(".parquet")]

    dfs = []
    for file in parquet_files:
        file_path = os.path.join(parquet_dir, file)
        df = pd.read_parquet(file_path)
        dfs.append(df)
        print("Loaded:", file)

    final_df = pd.concat(dfs, ignore_index=True)
    print("Total rows:", len(final_df))

    # Export to CSV
    output_csv = os.path.join(parquet_dir, "combined_output.csv")
    final_df.to_csv(output_csv, index=False)
    print("CSV Saved at:", output_csv)

    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
