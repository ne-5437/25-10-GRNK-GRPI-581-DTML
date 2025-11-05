import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import io
    from statsmodels.tsa.holtwinters import SimpleExpSmoothing
    return SimpleExpSmoothing, io, mo, pd


@app.cell
def _(mo):
    uploader = mo.ui.file(label="📁 Upload CSV file")

    method_selector = mo.ui.dropdown(
        options=[
            "Mean Imputation",
            "Median Imputation",
            "Forward Fill",
            "Backward Fill",
            "Linear Interpolation",
            "Exponential Smoothing"
        ],
        label="Select Imputation/Smoothing Method",
        value="Mean Imputation"
    )
    return method_selector, uploader


@app.cell
def _(io, method_selector, mo, pd, uploader):
    def show_uploaded_file():
        if not uploader.value:
            return mo.md("⚠️ **Please upload a CSV file above.**")

        uploaded_file = uploader.value[0]
        file_buffer = io.BytesIO(uploaded_file.contents)

        # Detect delimiter
        sample = file_buffer.read(2048).decode("utf-8", errors="ignore")
        file_buffer.seek(0)
        if ";" in sample and sample.count(";") > sample.count(","):
            sep = ";"
        elif "\t" in sample:
            sep = "\t"
        else:
            sep = ","

        # Read CSV
        df = pd.read_csv(file_buffer, sep=sep, encoding="utf-8-sig", on_bad_lines="skip")
        df.columns = [c.strip().replace("﻿", "").replace("\ufeff", "") for c in df.columns]

        return mo.ui.dataframe(df)

    # --- Layout display ---
    mo.vstack([mo.hstack([uploader, method_selector]), show_uploaded_file()])
    return


@app.cell
def _(io, mo, pd, uploader):
    def get_column_selector():
        if not uploader.value:
            return mo.md("⚠️ **Please upload a CSV file first (Cell 3).**")

        uploaded_file = uploader.value[0]
        file_buffer = io.BytesIO(uploaded_file.contents)

        # detect delimiter
        sample = file_buffer.read(2048).decode("utf-8", errors="ignore")
        file_buffer.seek(0)
        if ";" in sample and sample.count(";") > sample.count(","):
            sep = ";"
        elif "\t" in sample:
            sep = "\t"
        else:
            sep = ","

        df = pd.read_csv(file_buffer, sep=sep, encoding="utf-8-sig", on_bad_lines="skip")
        df.columns = [c.strip().replace("﻿", "").replace("\ufeff", "") for c in df.columns]

        return mo.ui.dropdown(
            options=list(df.columns),
            label="Select Column",
            value=list(df.columns)[0],
        )

    column_selector = get_column_selector()
    column_selector
    return (column_selector,)


@app.cell
def _(
    SimpleExpSmoothing,
    column_selector,
    io,
    method_selector,
    mo,
    pd,
    uploader,
):

    def process_selected_column():
        if not uploader.value:
            return mo.md("⚠️ **Please upload a CSV file first (Cell 3).**")

        uploaded_file = uploader.value[0]
        file_buffer = io.BytesIO(uploaded_file.contents)

        # detect delimiter
        sample = file_buffer.read(2048).decode("utf-8", errors="ignore")
        file_buffer.seek(0)
        if ";" in sample and sample.count(";") > sample.count(","):
            sep = ";"
        elif "\t" in sample:
            sep = "\t"
        else:
            sep = ","

        df = pd.read_csv(file_buffer, sep=sep, encoding="utf-8-sig", on_bad_lines="skip")
        df.columns = [c.strip().replace("﻿", "").replace("\ufeff", "") for c in df.columns]

        col = column_selector.value
        method = method_selector.value

        # numeric conversion if possible
        try:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        except Exception:
            pass

        series = df[col].copy()

        # --- apply method (using ffill/bfill directly to silence warning) ---
        if method == "Mean Imputation":
            series = series.fillna(series.mean())
        elif method == "Median Imputation":
            series = series.fillna(series.median())
        elif method == "Forward Fill":
            series = series.ffill()
        elif method == "Backward Fill":
            series = series.bfill()
        elif method == "Linear Interpolation":
            series = series.interpolate(method="linear")
        elif method == "Exponential Smoothing":
            non_na = series.dropna()
            if len(non_na) >= 2:
                try:
                    model = SimpleExpSmoothing(non_na, initialization_method="heuristic").fit(
                        smoothing_level=0.2, optimized=False
                    )
                    fitted = model.fittedvalues.reindex_like(series)
                    series = fitted.combine_first(series)
                except Exception:
                    pass

        result_df = pd.DataFrame({
            "Original": df[col],
            "Processed": series
        })

        # ✅ return so Marimo shows output
        return mo.vstack([
            mo.hstack([method_selector, column_selector]),
            mo.md(f"### 🧮 {method} applied on **{col}**"),
            mo.ui.dataframe(result_df)
        ])

    process_selected_column()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
