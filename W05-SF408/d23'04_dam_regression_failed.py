import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import numpy as np
    from statsmodels.tsa.seasonal import STL
    import plotly.graph_objects as go
    import marimo as mo
    return STL, go, mo, np, pd


@app.cell
def _(pd):
    # --- 1. Setup and Data Preparation Functions ---

    def to_naive(series):
        ts = pd.to_datetime(series, errors="coerce", utc=True)
        return ts.dt.tz_convert(None)

    def clean_df(df):
        out = df.copy()
        out["START_TIME"] = to_naive(out["START_TIME"])
        out["ACTUAL"] = pd.to_numeric(out["ACTUAL"], errors="coerce")
        out.dropna(subset=["START_TIME", "ACTUAL"], inplace=True)
        out.reset_index(drop=True, inplace=True)
        return out

    def clip_range(df):
        clip_start = pd.Timestamp("2024-10-01")
        clip_end   = pd.Timestamp("2025-09-30")
        return df[(df["START_TIME"] >= clip_start) & (df["START_TIME"] <= clip_end)].copy()
    return clean_df, clip_range


@app.cell
def _(STL, clean_df, clip_range, pd):
    # --- 2. Data Loading, Aggregation, and Decomposition ---

    dam_raw  = pd.read_csv("DAM_2yrs.csv")
    dam_clean  = clean_df(dam_raw)
    dam_clip  = clip_range(dam_clean)

    # Seasonal period set to 9 for 3-hour daily cycle (8 intervals + 1)
    SEASONAL_PERIOD = 9 

    def perform_stl_decomposition(df):
        series = (
            df.set_index("START_TIME")["ACTUAL"]
            .resample('3H') 
            .mean()
            .ffill()
        )
        series.index.freq = None

        stl = STL(series, seasonal=SEASONAL_PERIOD, robust=True)
        result = stl.fit()

        components = pd.DataFrame({
            "START_TIME": series.index,
            "Trend": result.trend,
        })
        return components

    dam_components = perform_stl_decomposition(dam_clip)
    return (dam_components,)


@app.cell
def _(go, np, pd):
    # --- 3. Seasonal Trend Fitting Logic ---

    SUMMER_START = pd.Timestamp("2025-03-01")
    SUMMER_END   = pd.Timestamp("2025-05-31")
    SEASON_NAME  = "Summer 2025"
    MARKET_NAME  = "DAM"

    def fit_and_plot_seasonal_trend(components_df, start_date, end_date, market_name, season_name):

        df_season = components_df[
            (components_df["START_TIME"] >= start_date) & 
            (components_df["START_TIME"] <= end_date)
        ].copy()

        X = np.arange(len(df_season))
        Y = df_season["Trend"].values

        # Linear Fit (Degree 1)
        p_linear = np.polyfit(X, Y, 1)
        f_linear = np.poly1d(p_linear)

        # Quadratic Fit (Degree 2)
        p_quadratic = np.polyfit(X, Y, 2)
        f_quadratic = np.poly1d(p_quadratic)

        # --- NEW: Cubic Fit (Degree 3) ---
        p_cubic = np.polyfit(X, Y, 3)
        f_cubic = np.poly1d(p_cubic)

        # Extract Equations for Labels
        linear_eq = f"y = {p_linear[0]:.2f}x + {p_linear[1]:.2f}"
        quadratic_eq = f"y = {p_quadratic[0]:.2e}x² + {p_quadratic[1]:.2f}x + {p_quadratic[2]:.2f}"
        cubic_eq = f"y = {p_cubic[0]:.2e}x³ + {p_cubic[1]:.2e}x² + {p_cubic[2]:.2f}x + {p_cubic[3]:.2f}"

        # Create Plotly Figure
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df_season["START_TIME"],
            y=df_season["Trend"],
            mode='lines+markers',
            name=f'Actual Trend ({market_name})',
            line=dict(color='red', width=3),
            marker=dict(size=4)
        ))

        fig.add_trace(go.Scatter(
            x=df_season["START_TIME"],
            y=f_linear(X),
            mode='lines',
            name=f'Linear Fit: {linear_eq}',
            line=dict(color='yellow', dash='dash', width=2)
        ))

        fig.add_trace(go.Scatter(
            x=df_season["START_TIME"],
            y=f_quadratic(X),
            mode='lines',
            name=f'Quadratic Fit: {quadratic_eq}',
            line=dict(color='lime', dash='dot', width=2)
        ))

        # --- NEW: Add Cubic Fit Trace ---
        fig.add_trace(go.Scatter(
            x=df_season["START_TIME"],
            y=f_cubic(X),
            mode='lines',
            name=f'Cubic Fit: {cubic_eq}',
            line=dict(color='purple', dash='dashdot', width=2)
        ))

        fig.update_layout(
            title=f"Trend Analysis: Polynomial Fit for {market_name} during {season_name}",
            xaxis_title="Date (3-Hour Intervals)",
            yaxis_title="Trend Component Value (Smoothed Price)",
            height=600
        )

        return fig, linear_eq, quadratic_eq, cubic_eq
    return (
        MARKET_NAME,
        SEASON_NAME,
        SUMMER_END,
        SUMMER_START,
        fit_and_plot_seasonal_trend,
    )


@app.cell
def _(
    MARKET_NAME,
    SEASON_NAME,
    SUMMER_END,
    SUMMER_START,
    dam_components,
    fit_and_plot_seasonal_trend,
    mo,
):
    # --- 4. Execution and Output ---

    fig_dam_trend_fit, linear_eq, quadratic_eq, cubic_eq = fit_and_plot_seasonal_trend(
        dam_components, 
        SUMMER_START, 
        SUMMER_END, 
        MARKET_NAME, 
        SEASON_NAME
    )

    mo.vstack([
        mo.md(f"### 📈 {MARKET_NAME} Trend Analysis for {SEASON_NAME}"),
        mo.md(f"The analysis fits the isolated **Trend Component** to quantify its momentum."),
        mo.md(f"* **Linear Fit:** `{linear_eq}` (Overall average direction)"),
        mo.md(f"* **Quadratic Fit:** `{quadratic_eq}` (Overall curvature/acceleration)"),
        mo.md(f"* **Cubic Fit:** `{cubic_eq}` (Captures more complex changes with two inflection points)"),
        mo.ui.plotly(fig_dam_trend_fit)
    ])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
