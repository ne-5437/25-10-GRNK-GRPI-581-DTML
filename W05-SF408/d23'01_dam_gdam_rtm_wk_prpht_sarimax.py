import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import plotly.graph_objects as go
    import marimo as mo
    from prophet import Prophet
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    return Prophet, SARIMAX, go, mo, pd


@app.cell
def _(pd):
    # --- 1. DATA LOADING AND CLEANING (Existing Code) ---

    # NOTE: Assuming your CSV files are available in the Marimo environment's directory
    dam_raw  = pd.read_csv("DAM_2yrs.csv")
    gdam_raw = pd.read_csv("GDAM_2yrs.csv")
    rtm_raw  = pd.read_csv("RTM_2yrs.csv")

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

    dam_clean  = clean_df(dam_raw)
    gdam_clean = clean_df(gdam_raw)
    rtm_clean  = clean_df(rtm_raw)

    clip_start = pd.Timestamp("2024-10-01")
    clip_end   = pd.Timestamp("2025-09-30")

    def clip_range(df):
        return df[(df["START_TIME"] >= clip_start) & (df["START_TIME"] <= clip_end)].copy()

    dam_clip  = clip_range(dam_clean)
    gdam_clip = clip_range(gdam_clean)
    rtm_clip  = clip_range(rtm_clean)

    def weekly_agg(df, label):
        wk = (
            df.set_index("START_TIME")
              .resample("1W")
              .mean(numeric_only=True)
              .reset_index()
        )
        wk["MARKET"] = label
        return wk

    dam_weekly  = weekly_agg(dam_clip,  "DAM")
    gdam_weekly = weekly_agg(gdam_clip, "GDAM")
    rtm_weekly  = weekly_agg(rtm_clip,  "RTM")

    all_weekly = pd.concat([dam_weekly, gdam_weekly, rtm_weekly], ignore_index=True)
    return dam_weekly, gdam_weekly, rtm_weekly


@app.cell
def _(Prophet, SARIMAX, pd):
    # --- 2. MODELING FUNCTIONS ---

    # Define SARIMAX orders (p,d,q)x(P,D,Q,S)
    # S=52 for yearly seasonality on weekly data. 
    # These are reasonable starting points but would be tuned in a real project.
    SARIMAX_ORDERS = {
        "DAM": (1, 1, 1, 0, 1, 1, 52),
        "GDAM": (1, 1, 1, 0, 1, 1, 52),
        "RTM": (1, 1, 1, 0, 1, 1, 52),
    }

    def fit_prophet(df):
        """Fits Prophet and returns the forecast DataFrame."""
        # Prophet requires 'ds' and 'y' columns
        df_prophet = df.rename(columns={"START_TIME": "ds", "ACTUAL": "y"})[["ds", "y"]]

        # Initialize and fit Prophet with explicit yearly seasonality
        m = Prophet(
            growth="linear", 
            seasonality_mode='multiplicative', # Often better for price data
            weekly_seasonality=False,          # Data is already aggregated weekly
            daily_seasonality=False
        )
        m.add_seasonality(name='yearly', period=365.25, fourier_order=10)
        m.fit(df_prophet)

        # Predict for the same time range
        future = m.make_future_dataframe(periods=0, freq='W') # We use existing dates
        forecast = m.predict(future)

        # Merge prediction with actual data for plotting
        df_prophet_out = df.copy()
        df_prophet_out["PROPHET"] = forecast["yhat"].values
        return df_prophet_out

    def fit_sarimax(df, market_label):
        """Fits SARIMAX and returns the prediction series."""
        # SARIMAX requires a time series index
        series = df.set_index("START_TIME")["ACTUAL"]

        p, d, q, P, D, Q, S = SARIMAX_ORDERS[market_label]

        # Fit SARIMAX model
        model = SARIMAX(
            series,
            order=(p, d, q),
            seasonal_order=(P, D, Q, S),
            enforce_stationarity=False, 
            enforce_invertibility=False
        )

        # NOTE: The SARIMAX fit can fail if the order is poor or data is too short/sparse.
        try:
            results = model.fit(disp=False)
            # Get in-sample predictions (1 step ahead)
            predictions = results.predict(start=series.index.min(), end=series.index.max())
            return predictions.rename("SARIMAX")
        except Exception as e:
            print(f"SARIMAX failed for {market_label}: {e}")
            return pd.Series(index=series.index, data=[None] * len(series), name="SARIMAX")
    return fit_prophet, fit_sarimax


@app.cell
def _(dam_weekly, fit_prophet, fit_sarimax, gdam_weekly, rtm_weekly):
    # Apply models
    dam_prophet  = fit_prophet(dam_weekly)
    gdam_prophet = fit_prophet(gdam_weekly)
    rtm_prophet  = fit_prophet(rtm_weekly)

    dam_sarimax_series  = fit_sarimax(dam_weekly, "DAM")
    gdam_sarimax_series = fit_sarimax(gdam_weekly, "GDAM")
    rtm_sarimax_series  = fit_sarimax(rtm_weekly, "RTM")

    # Combine all results into one DataFrame per market
    dam_results = dam_prophet.merge(
        dam_sarimax_series, 
        left_on="START_TIME", 
        right_index=True, 
        how="left"
    )
    gdam_results = gdam_prophet.merge(
        gdam_sarimax_series, 
        left_on="START_TIME", 
        right_index=True, 
        how="left"
    )
    rtm_results = rtm_prophet.merge(
        rtm_sarimax_series, 
        left_on="START_TIME", 
        right_index=True, 
        how="left"
    )
    return dam_results, gdam_results, rtm_results


@app.cell
def _(go):
    # --- 3. PLOTTING FUNCTION ---

    def create_comparison_plot(df, market):
        """Generates a Plotly figure comparing Actual, Prophet, and SARIMAX."""
        fig = go.Figure()

        # Define common trace arguments (excluding line, which changes per trace)
        common_args = {
            "x": df["START_TIME"], 
            "mode": "lines",
        }

        # Define a default line width
        LINE_WIDTH = 2.5 

        # Add Actual Data
        fig.add_trace(go.Scatter(
            y=df["ACTUAL"], 
            name="Actual",
            line={"color": "green", "dash": "solid", "width": LINE_WIDTH},
            **common_args # Only unpacks x and mode
        ))

        # Add Prophet Prediction
        fig.add_trace(go.Scatter(
            y=df["PROPHET"], 
            name="Prophet Trend",
            line={"color": "red", "dash": "dash", "width": LINE_WIDTH},
            **common_args
        ))

        # Add SARIMAX Prediction
        fig.add_trace(go.Scatter(
            y=df["SARIMAX"], 
            name="SARIMAX Trend",
            line={"color": "blue", "dash": "dot", "width": LINE_WIDTH},
            **common_args
        ))

        # Add season shading (for context)
        seasons = [
            ("Autumn",  "2024-10-01", "2024-12-31", "rgba(255,165,0,0.15)"),
            ("Winter",  "2025-01-01", "2025-02-28", "rgba(135,206,250,0.15)"),
            ("Summer",  "2025-03-01", "2025-05-31", "rgba(255,99,71,0.15)"),
            ("Monsoon", "2025-06-01", "2025-09-30", "rgba(0,128,128,0.15)")
        ]

        for name, s, e, color in seasons:
            fig.add_vrect(
                x0=s, x1=e, fillcolor=color, opacity=0.25, line_width=0,
                layer="below",
                annotation_text=name, annotation_position="top left"
            )

        fig.update_layout(
            title=f"**{market}** Market: Actual vs. Prophet vs. SARIMAX (Weekly Average)",
            xaxis_title="Week",
            yaxis_title="Weekly Avg ACTUAL",
            height=450,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        return fig
    return (create_comparison_plot,)


@app.cell
def _(create_comparison_plot, dam_results, gdam_results, rtm_results):
    # Generate all three figures
    fig_dam = create_comparison_plot(dam_results, "DAM")
    fig_gdam = create_comparison_plot(gdam_results, "GDAM")
    fig_rtm = create_comparison_plot(rtm_results, "RTM")

    # --- 4. MARIMO OUTPUT ---
    # Use Marimo's formatting to display the three figures clearly
    return fig_dam, fig_gdam, fig_rtm


@app.cell
def _(fig_dam, mo):
    mo.ui.plotly(fig_dam), # Remove 'width="100%"'
    return


@app.cell
def _(fig_gdam, mo):
    mo.ui.plotly(fig_gdam), # Remove 'width="100%"'
    return


@app.cell
def _(fig_rtm, mo):
    mo.ui.plotly(fig_rtm)  # Remove 'width="100%"'
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
