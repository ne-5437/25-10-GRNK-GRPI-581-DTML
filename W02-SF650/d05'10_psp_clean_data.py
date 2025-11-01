import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    # === Step 1: Data Ingestion ===
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    # Load import & export datasets
    df_import = pd.read_csv("import_energy.csv")
    df_export = pd.read_csv("export_energy.csv")

    print("Import Data:", df_import.shape)
    print("Export Data:", df_export.shape)
    return df_export, df_import, pd, plt


@app.cell
def _(df_export, df_import, pd):
    # === Step 2: Data Cleaning ===

    def clean_energy_df(df):
        df = df.copy()

        # Convert timestamp to datetime if available
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            df = df.sort_values(by='timestamp')

        # Numerical columns: fill missing values using linear interpolation
        num_cols = df.select_dtypes(include=['float64', 'int64']).columns
        df[num_cols] = df[num_cols].interpolate(method='linear', limit_direction='both')

        # Remove duplicates if any
        df = df.drop_duplicates()

        return df

    df_import_clean = clean_energy_df(df_import)
    df_export_clean = clean_energy_df(df_export)

    print("Import Clean:", df_import_clean.shape)
    print("Export Clean:", df_export_clean.shape)
    return df_export_clean, df_import_clean


@app.cell
def _(df_export_clean, df_import_clean):
    print("=== Import Statistical Summary ===")
    print(df_import_clean.describe())

    print("=== Export Statistical Summary ===")
    print(df_export_clean.describe())
    return


@app.cell
def _(df_export_clean, df_import_clean):
    print("Missing in Import:\n", df_import_clean.isna().sum())
    print("Missing in Export:\n", df_export_clean.isna().sum())
    return


@app.cell
def _(df_export_clean, df_import_clean):
    df_import_clean.rename(columns={"TIMESTAMP": "timestamp"}, inplace=True)
    df_export_clean.rename(columns={"TIMESTAMP": "timestamp"}, inplace=True)

    df_import_clean.rename(columns={"gen_mwh_import": "import_mwh"}, inplace=True)
    df_export_clean.rename(columns={"gen_mwh_export": "export_mwh"}, inplace=True)
    return


@app.cell
def _(df_export_clean, df_import_clean, pd):
    df_merged = pd.merge(
        df_import_clean,
        df_export_clean,
        on=["timestamp", "UNIT"],
        how="inner"
    )

    print("Merged Data:", df_merged.shape)
    df_merged.head()
    return (df_merged,)


@app.cell
def _(df_merged, plt):
    units = sorted(df_merged["UNIT"].unique())
    plt.figure(figsize=(18, 20))

    for i, unit in enumerate(units, start=1):
        df_unit = df_merged[df_merged["UNIT"] == unit]

        plt.subplot(4, 2, i)
        plt.plot(df_unit["timestamp"], df_unit["import_mwh"], label="Import")
        plt.plot(df_unit["timestamp"], df_unit["export_mwh"], label="Export")
        plt.title(f"Unit {unit} Import vs Export")
        plt.xlabel("Time")
        plt.ylabel("Generation (MWh)")
        plt.legend()

    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(df_merged, plt):
    df_agg = df_merged.copy()
    df_agg["total_import"] = df_agg.groupby("timestamp")["import_mwh"].transform("sum")
    df_agg["total_export"] = df_agg.groupby("timestamp")["export_mwh"].transform("sum")

    df_agg_unique = df_agg.drop_duplicates(subset=["timestamp"])

    plt.figure(figsize=(14,5))
    plt.plot(df_agg_unique["timestamp"], df_agg_unique["total_import"], label="Total Import")
    plt.plot(df_agg_unique["timestamp"], df_agg_unique["total_export"], label="Total Export")
    plt.title("Total Import vs Export Across All Units")
    plt.xlabel("Time")
    plt.ylabel("MWh")
    plt.legend()
    plt.show()
    return


if __name__ == "__main__":
    app.run()
