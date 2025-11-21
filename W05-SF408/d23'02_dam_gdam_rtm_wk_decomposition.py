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
    # --- 1. FUNCTION DEFINITIONS (Updated Aggregation) ---

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
        # Note: We must ensure the original data spans this range!
        return df[(df["START_TIME"] >= clip_start) & (df["START_TIME"] <= clip_end)].copy()
    return clean_df, clip_range


@app.function
# --- KEY CHANGE: Resampling to '1D' (Daily) ---
def daily_agg(df, label):
    wk = (
        df.set_index("START_TIME")
          .resample("1D") # Changed from "1W" to "1D"
          .mean(numeric_only=True)
          .reset_index()
    )
    wk["MARKET"] = label
    return wk


@app.cell
def _(clean_df, clip_range, pd):
    # --- 2. DATA LOADING AND AGGREGATION ---

    dam_raw  = pd.read_csv("DAM_2yrs.csv")
    gdam_raw = pd.read_csv("GDAM_2yrs.csv")
    rtm_raw  = pd.read_csv("RTM_2yrs.csv")

    dam_clean  = clean_df(dam_raw)
    gdam_clean = clean_df(gdam_raw)
    rtm_clean  = clean_df(rtm_raw)

    dam_clip  = clip_range(dam_clean)
    gdam_clip = clip_range(gdam_clean)
    rtm_clip  = clip_range(rtm_clean)

    # Variables are now daily
    dam_daily  = daily_agg(dam_clip,  "DAM")
    gdam_daily = daily_agg(gdam_clip, "GDAM")
    rtm_daily  = daily_agg(rtm_clip,  "RTM")

    # Dictionary of dataframes
    market_data = {
        "DAM": dam_daily,
        "GDAM": gdam_daily,
        "RTM": rtm_daily,
    }
    return (market_data,)


@app.cell
def _(STL, pd):
    # --- 3. STL DECOMPOSITION SETUP (FIXED Seasonal Period) ---

    # KEY CHANGE: Daily data, yearly seasonality is ~365 days. 
    # STL requires an odd integer, so we use 365 (or 367 for a leap year, but 365 is common).
    SEASONAL_PERIOD = 365 

    def perform_stl_decomposition(df, market_name):
        """Performs STL decomposition on the 'ACTUAL' column using daily frequency."""
        series = df.set_index("START_TIME")["ACTUAL"]

        # Infer frequency ('D') is crucial for STL to work
        series.index.freq = pd.infer_freq(series.index) 

        # STL now uses the odd period 365
        # Since we are modeling the annual cycle, we use a large window for the trend (`trend=None` uses defaults)
        stl = STL(series, seasonal=SEASONAL_PERIOD, robust=True)
        result = stl.fit()

        components = pd.DataFrame({
            "Actual": series,
            "Trend": result.trend,
            "Seasonality": result.seasonal,
            "Residual": result.resid
        }).reset_index()
        components["Market"] = market_name

        return components
    return (perform_stl_decomposition,)


@app.cell
def _(market_data, mo, pd, perform_stl_decomposition):
    # Run decomposition for all markets
    dam_components = perform_stl_decomposition(market_data["DAM"], "DAM")
    gdam_components = perform_stl_decomposition(market_data["GDAM"], "GDAM")
    rtm_components = perform_stl_decomposition(market_data["RTM"], "RTM")

    all_components = pd.concat([dam_components, gdam_components, rtm_components], ignore_index=True)

    mo.md("✅ **Step 1: Data Preparation and Daily STL Decomposition complete.**")
    return dam_components, gdam_components, rtm_components


@app.cell
def _(go, make_subplots):
    # --- 4. PLOTTING ---

    def plot_decomposition(components_df, market_name):
        """Generates a 4-panel Plotly subplot for decomposition results."""

        fig = make_subplots.make_subplots(
            rows=4, cols=1,
            shared_xaxes=True,
            subplot_titles=(
                f"Original Daily Time Series ({market_name})", 
                "Trend Component", 
                "Seasonal Component (Yearly)", 
                "Residuals"
            ),
            vertical_spacing=0.08,
        )

        time_col = components_df["START_TIME"]

        fig.add_trace(go.Scatter(x=time_col, y=components_df["Actual"], mode='lines', name='Actual', line=dict(color='blue', width=1)), row=1, col=1)
        fig.add_trace(go.Scatter(x=time_col, y=components_df["Trend"], mode='lines', name='Trend', line=dict(color='red', width=2)), row=2, col=1)
        fig.add_trace(go.Scatter(x=time_col, y=components_df["Seasonality"], mode='lines', name='Seasonality', line=dict(color='white', width=1)), row=3, col=1)
        fig.add_trace(go.Scatter(x=time_col, y=components_df["Residual"], mode='markers', name='Residual', marker=dict(color='yellow', size=2)), row=4, col=1)

        fig.update_layout(
            height=900, 
            title_text=f"Daily Time Series Decomposition (STL) for **{market_name}**",
            showlegend=False,
        )

        max_resid = components_df["Residual"].abs().max()
        fig.update_yaxes(range=[-max_resid * 1.1, max_resid * 1.1], row=4, col=1)
        fig.update_traces(xaxis='x4') # Fix for shared x-axes issue

        return fig
    return (plot_decomposition,)


@app.cell
def _(dam_components, gdam_components, mo, plot_decomposition, rtm_components):
    # Generate and Display Plots
    fig_dam = plot_decomposition(dam_components, "DAM")
    fig_gdam = plot_decomposition(gdam_components, "GDAM")
    fig_rtm = plot_decomposition(rtm_components, "RTM")

    mo.vstack([
        mo.md("## DAM Daily Decomposition"),
        mo.ui.plotly(fig_dam),
        mo.md("---"),
        mo.md("## GDAM Daily Decomposition"),
        mo.ui.plotly(fig_gdam),
        mo.md("---"),
        mo.md("## RTM Daily Decomposition"),
        mo.ui.plotly(fig_rtm)
    ])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
