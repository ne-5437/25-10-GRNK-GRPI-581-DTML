import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    return mo, pd


@app.cell
def _(pd):
    # --- Load CSV ---
    df = pd.read_csv("IEX.open_meteo_forecast.csv")

    # --- Convert to date only + remove duplicates + sort ---
    df['start_time'] = pd.to_datetime(df['start_time']).dt.date
    dates = sorted(df['start_time'].unique())

    # --- Identify consecutive date ranges ---
    ranges = []
    start = dates[0]
    prev = dates[0]
    return dates, df, prev, ranges, start


@app.cell
def _(dates, mo, prev, ranges, start):
    for d in dates[1:]:
        # If not consecutive, close current range
        if (d - prev).days != 1:
            ranges.append((start, prev))
            start1 = d
        prev1 = d

    # Add final range
    ranges.append((start1, prev1))

    # --- Format output ---
    formatted = ", ".join([f"{a} → {b}" for a, b in ranges])

    mo.md(f"""
    ### 📅 Consecutive Date Ranges  
    **Detected ranges:**  
    {formatted}
    """)
    return


@app.cell
def _(df):
    df
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
