import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import os
    import pandas as pd

    root_folder = r"D:\09(2)\09"

    all_dfs = []

    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith(".parquet"):
                file_path = os.path.join(root, file)
                print("Reading:", file_path)
                df_temp = pd.read_parquet(file_path)
                all_dfs.append(df_temp)

    # Combine all parquet DataFrames
    df_combined = pd.concat(all_dfs, ignore_index=True)
    print("✅ Combined shape:", df_combined.shape)

    # Optional: Save as CSV
    df_combined.to_csv("combined_output.csv", index=False)
    print("✅ Saved as combined_output.csv")

    return


if __name__ == "__main__":
    app.run()
