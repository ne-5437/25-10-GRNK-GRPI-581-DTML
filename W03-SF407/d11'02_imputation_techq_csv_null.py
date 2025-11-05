import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from statsmodels.tsa.holtwinters import SimpleExpSmoothing

    # === 1️⃣ Load the CSV ===
    df = pd.read_csv("X-Minutal6.csv", encoding="utf-8-sig", sep=None, engine="python")
    df.columns = df.columns.str.strip()

    mo.md(f"✅ Loaded CSV with {len(df)} rows and {len(df.columns)} columns.")
    return SimpleExpSmoothing, df, mo, pd, plt


@app.cell
def _(mo):
    # === 2️⃣ Dropdown to select imputation method ===
    method_selector = mo.ui.dropdown(
        options=[
            "Mean Imputation",
            "Median Imputation",
            "Forward Fill",
            "Backward Fill",
            "Linear Interpolation",
            "Exponential Smoothing"
        ],
        label="Select Imputation Method",
        value="Mean Imputation"
    )

    method_selector
    return (method_selector,)


@app.cell
def _(SimpleExpSmoothing, df, method_selector, mo):
    # === 3️⃣ Process selected column and apply imputation ===
    col = "Bearing D.E. Temperature max 10M (ºC)"

    def process_and_display(method):
        df_copy = df.copy()

        # Filter by device (if column exists)
        if "Device" in df_copy.columns:
            filtered = df_copy[df_copy["Device"] == "G97-N24"].copy()
        else:
            filtered = df_copy.copy()

        if col not in filtered.columns:
            return mo.md(f"❌ Column **'{col}'** not found in CSV.")

        # Mask abnormal values
        mask = filtered[col] > 60
        temp_series = filtered.loc[mask, col].copy()

        # Imputation logic
        if method == "Mean Imputation":
            temp_series = temp_series.fillna(temp_series.mean())
        elif method == "Median Imputation":
            temp_series = temp_series.fillna(temp_series.median())
        elif method == "Forward Fill":
            temp_series = temp_series.fillna(method="ffill")
        elif method == "Backward Fill":
            temp_series = temp_series.fillna(method="bfill")
        elif method == "Linear Interpolation":
            temp_series = temp_series.interpolate(method="linear")
        elif method == "Exponential Smoothing":
            model = SimpleExpSmoothing(temp_series.dropna())
            fit = model.fit(smoothing_level=0.2, optimized=False)
            temp_series = fit.fittedvalues.reindex(temp_series.index)

        # Apply cleaned values
        filtered.loc[mask, col] = temp_series

        # Save for plotting next cell
        global filtered_result
        filtered_result = filtered.copy()

        # Display table and stats
        stats_md = mo.md(f"### 📊 Summary for `{col}` ({method})\n```\n{filtered[[col]].describe()}\n```")
        table_ui = mo.ui.table(filtered[[col]].head(1000))
        return mo.vstack([stats_md, table_ui])

    process_and_display(method_selector.value)
    return col, filtered_result


@app.cell
def _(col, df, filtered_result, plt):
    # === 4️⃣ Plot Original vs Cleaned Values ===
    original_series = df[col]
    cleaned_series = filtered_result[col]

    fig, ax = plt.subplots(figsize=(12,5))

    ax.plot(original_series.index, original_series.values, label="Original", color="orange", alpha=0.6)
    ax.plot(cleaned_series.index, cleaned_series.values, label="After Imputation", color="blue")

    ax.set_title(f"Original vs Imputed Values — {col}")
    ax.set_xlabel("Index")
    ax.set_ylabel("Temperature (ºC)")
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()

    fig  # ✅ Return figure (Marimo will render this)
    return


@app.cell
def _(df, mo, pd):
    # === 5️⃣ Count Null Values per Column ===
    null_counts = df.isnull().sum()
    non_null_counts = df.notnull().sum()

    summary_df = pd.DataFrame({
        "Total Rows": len(df),
        "Non-Null Count": non_null_counts,
        "Null Count": null_counts,
        "Null %": (null_counts / len(df) * 100).round(2)
    })

    mo.md("### 🧮 Null Value Summary per Column")
    mo.ui.table(summary_df.reset_index().rename(columns={"index": "Column"}))
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
