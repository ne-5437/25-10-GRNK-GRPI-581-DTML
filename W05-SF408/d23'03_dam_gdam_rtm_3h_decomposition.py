import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    from statsmodels.tsa.seasonal import STL
    import plotly.graph_objects as go
    import plotly.subplots as make_subplots
    import marimo as mo
    return STL, go, make_subplots, mo, pd


@app.cell
def _(pd):
    # --- 1. Function Definitions ---

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
def _(clean_df, clip_range, pd):
    # --- 2. Data Loading and Clipping ---

    dam_raw  = pd.read_csv("DAM_2yrs.csv")
    gdam_raw = pd.read_csv("GDAM_2yrs.csv")
    rtm_raw  = pd.read_csv("RTM_2yrs.csv")

    dam_clean  = clean_df(dam_raw)
    gdam_clean = clean_df(gdam_raw)
    rtm_clean  = clean_df(rtm_raw)

    dam_clip  = clip_range(dam_clean)
    gdam_clip = clip_range(gdam_clean)
    rtm_clip  = clip_range(rtm_clean)

    market_data = {
        "DAM": dam_clip,
        "GDAM": gdam_clip,
        "RTM": rtm_clip,
    }

    # Seasonal period set to 9 (daily pattern: 8 intervals + 1)
    SEASONAL_PERIOD = 9 
    return SEASONAL_PERIOD, market_data


@app.cell
def _(SEASONAL_PERIOD, STL, market_data, pd):
    def perform_stl_decomposition(df, market_name):
        # Resample to '3H' and forward-fill gaps
        series = (
            df.set_index("START_TIME")["ACTUAL"]
            .resample('1H') 
            .mean()
            .ffill()
        )

        # Strip the frequency attribute to avoid ValueError
        series.index.freq = None

        stl = STL(series, seasonal=SEASONAL_PERIOD, robust=True)
        result = stl.fit()

        components = pd.DataFrame({
            "Actual": series,
            "Trend": result.trend,
            "Seasonality": result.seasonal,
            "Residual": result.resid
        }).reset_index().rename(columns={"index": "START_TIME"})
        components["Market"] = market_name

        return components

    dam_components = perform_stl_decomposition(market_data["DAM"], "DAM")
    gdam_components = perform_stl_decomposition(market_data["GDAM"], "GDAM")
    rtm_components = perform_stl_decomposition(market_data["RTM"], "RTM")

    all_components = pd.concat([dam_components, gdam_components, rtm_components], ignore_index=True)
    return dam_components, gdam_components, rtm_components


@app.cell
def _(go, make_subplots):
    # --- 3. Plotting Function (WITH RANGE SLIDER) ---

    def plot_decomposition(components_df, market_name):
        df_plot = components_df 

        fig = make_subplots.make_subplots(
            rows=4, cols=1,
            shared_xaxes=True,
            subplot_titles=(
                f"Original 3-Hour Time Series ({market_name}) - Oct 2024 to Sep 2025", 
                "Trend Component (Annual/Long-term Movement)", 
                "Seasonal Component (Daily/3-Hour Pattern)", 
                "Residuals"
            ),
            vertical_spacing=0.08,
        )

        time_col = df_plot["START_TIME"]

        # Use consistent colors and thin lines for the full year plot
        fig.add_trace(go.Scatter(x=time_col, y=df_plot["Actual"], mode='lines', name='Actual', line=dict(color='blue', width=0.5)), row=1, col=1)
        fig.add_trace(go.Scatter(x=time_col, y=df_plot["Trend"], mode='lines', name='Trend', line=dict(color='red', width=2)), row=2, col=1)
        fig.add_trace(go.Scatter(x=time_col, y=df_plot["Seasonality"], mode='lines', name='Seasonality', line=dict(color='white', width=1)), row=3, col=1)
        fig.add_trace(go.Scatter(x=time_col, y=df_plot["Residual"], mode='markers', name='Residual', marker=dict(color='yellow', size=2)), row=4, col=1)

        fig.update_layout(
            height=900, 
            title_text=f"3-Hour Time Series Decomposition (STL) for **{market_name}** (Full Year)",
            showlegend=False,
        )

        # Enable the range slider on the bottom X-axis (xaxis4)
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeslider_thickness=0.07,
            row=4, col=1 
        )

        # Hide the range slider on the other X-axes
        for i in range(1, 4):
             fig.update_xaxes(rangeslider_visible=False, row=i, col=1)

        max_resid = df_plot["Residual"].abs().max()
        fig.update_yaxes(range=[-max_resid * 1.1, max_resid * 1.1], row=4, col=1)

        return fig
    return (plot_decomposition,)


@app.cell
def _(dam_components):
    dam_components
    return


@app.cell
def _(dam_components, gdam_components, mo, plot_decomposition, rtm_components):
    # --- 4. Marimo Output ---

    fig_dam = plot_decomposition(dam_components[1000:2000], "DAM")
    fig_gdam = plot_decomposition(gdam_components[1000:2000], "GDAM")
    fig_rtm = plot_decomposition(rtm_components[1000:2000], "RTM")

    mo.vstack([
        mo.md("## 📈 DAM 3-Hour Decomposition (Full Year)"),
        mo.ui.plotly(fig_dam),
        mo.md("---"),
        mo.md("## 📉 GDAM 3-Hour Decomposition (Full Year)"),
        mo.ui.plotly(fig_gdam),
        mo.md("---"),
        mo.md("## ⚡ RTM 3-Hour Decomposition (Full Year)"),
        mo.ui.plotly(fig_rtm)
    ])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
