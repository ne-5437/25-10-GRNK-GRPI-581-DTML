import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import os
    import pandas as pd
    from pathlib import Path

    # Root folder containing subfolders + parquet files
    root_dir = r"D:\Pro Journey\GRNK-GRPI-581-DTML\W02-SF\09"

    # Collect all parquet file paths
    parquet_files = list(Path(root_dir).rglob("*.parquet"))

    print(f"Total Parquet files found: {len(parquet_files)}")

    # Load and concatenate
    df_list = []
    for file in parquet_files:
        try:
            print(f"Reading: {file}")
            df_list.append(pd.read_parquet(file))
        except Exception as e:
            print(f"❌ Error reading {file}: {e}")

    if df_list:
        final_df = pd.concat(df_list, ignore_index=True)

        # Save as CSV
        output_csv = os.path.join(root_dir, "merged_output.csv")
        final_df.to_csv(output_csv, index=False)
    
        print("\n✅ Merging Complete!")
        print(f"📌 Saved CSV at: {output_csv}")
        print(f"🧮 Final CSV Shape: {final_df.shape}")
    else:
        print("❌ No parquet files found or readable.")

    return


if __name__ == "__main__":
    app.run()
