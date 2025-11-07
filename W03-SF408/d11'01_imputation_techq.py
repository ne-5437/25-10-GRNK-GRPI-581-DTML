import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    from statsmodels.tsa.holtwinters import SimpleExpSmoothing
    return SimpleExpSmoothing, mo, pd


@app.cell
def _(pd):
    data = {'value': [10, None, 12, None, 14, 15, None, 17, None, 19]}
    df = pd.DataFrame(data)
    return (df,)


@app.cell
def _(mo):
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

    method_selector
    return (method_selector,)


@app.cell
def _(SimpleExpSmoothing, df, method_selector):
    method = method_selector.value
    df_copy = df.copy()

    if method == "Mean Imputation":
        df_copy['value'] = df_copy['value'].fillna(df_copy['value'].mean())
    elif method == "Median Imputation":
        df_copy['value'] = df_copy['value'].fillna(df_copy['value'].median())
    elif method == "Forward Fill":
        df_copy['value'] = df_copy['value'].fillna(method='ffill')
    elif method == "Backward Fill":
        df_copy['value'] = df_copy['value'].fillna(method='bfill')
    elif method == "Linear Interpolation":
        df_copy['value'] = df_copy['value'].interpolate(method='linear')
    elif method == "Exponential Smoothing":
        model = SimpleExpSmoothing(df_copy['value'].dropna())
        fit = model.fit(smoothing_level=0.2, optimized=False)
        df_copy['value'] = fit.fittedvalues.reindex(df_copy.index)

    df_copy
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
