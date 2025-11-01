import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt

    # Load and convert
    df = pd.read_csv("merged_output.csv")
    df["timestamps"] = pd.to_datetime(df["pt"], unit="ms")

    # Filter relevant Unit-1 IDs
    mapping = {
        "AP01.PSP.GSUT-1.Gen_MWH_IMPORT": "import_energy",
        "AP01.PSP.GSUT-1.Gen_MWH_EXPORT": "export_energy",
        "AP01.PSP.ST1.HV_MW": "switch_1"
    }

    df = df[df["id"].isin(mapping.keys())].copy()
    df["parameter"] = df["id"].map(mapping)

    # Pivot
    pivot_df = df.pivot_table(
        index="timestamps",
        columns="parameter",
        values="v",
        aggfunc="mean"
    ).reset_index()

    # Compute daily frequency (counts per day per parameter)
    daily_freq = (
        pivot_df
        .set_index("timestamps")
        .resample("D")[["import_energy", "export_energy"]]
        .count()
    )

    # Plot both in the same graph
    plt.figure(figsize=(10,5))
    plt.plot(daily_freq.index, daily_freq["import_energy"], label="Import Energy", color="green", marker="o")
    plt.plot(daily_freq.index, daily_freq["export_energy"], label="Export Energy", color="red", marker="o")
    plt.title("Daily Data Frequency: Import vs Export (Unit-1)")
    plt.xlabel("Date")
    plt.ylabel("Number of Samples per Day")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    return (df,)


@app.cell
def _(df):
    df
    return


@app.cell
def _(mo):
    mo.ui.dropdown()
    return


@app.cell
def _(df):
    import altair as alt
    alt.data_transformers.enable("vegafusion")
    alt.Chart(df[1000:2000]).mark_line().encode(
        x="timestamps:T", y="v"
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
