import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd

    # Load cleaned turbine file
    df = pd.read_csv("turbine_clean.csv", parse_dates=["TIMESTAMP"])

    # Select only required columns
    cols_required = [
        "TIMESTAMP",
        "GSUT-1_Gen_MWH_IMPORT",
        "UNIT1_UFMS_DISCHARGE_FLOW"
    ]

    df_filtered = df[cols_required]

    # Remove any exact duplicate timestamps by aggregating mean
    df_filtered = df_filtered.groupby("TIMESTAMP").mean()

    # Sort index (timestamp)
    df_filtered = df_filtered.sort_index()

    # Missing values remain NaN (default)
    # Save to new CSV
    df_filtered.to_csv("turbine_filtered.csv", index=True, index_label="TIMESTAMP")

    print("✅ Saved filtered dataset as turbine_filtered.csv")
    print("Final shape:", df_filtered.shape)

    return


if __name__ == "__main__":
    app.run()
