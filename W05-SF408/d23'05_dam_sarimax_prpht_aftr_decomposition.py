import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import plotly.graph_objects as go
    from statsmodels.tsa.seasonal import STL
    from prophet import Prophet
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    import pmdarima as pm
    import marimo as mo
    return Prophet, SARIMAX, STL, go, mo, np, pd, pm


@app.cell
def _(pd):
    # --- 1. Data Preparation Functions ---

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
def _(STL, clean_df, clip_range, mo, pd):
    # --- 2. Data Loading, Aggregation, and Decomposition ---

    dam_raw = pd.read_csv("DAM_2yrs.csv")
    dam_clean = clean_df(dam_raw)
    dam_clip = clip_range(dam_clean)

    # Seasonal period set to 9 for 3-hour daily cycle
    SEASONAL_PERIOD = 9 

    def get_dam_decomposition(df):
        # Resample to '3H' and forward-fill gaps
        series = (
            df.set_index("START_TIME")["ACTUAL"]
            .resample('3H') 
            .mean()
            .ffill()
        )
        series.index.freq = None

        # Decompose into Trend, Seasonal, and Residual
        stl = STL(series, seasonal=SEASONAL_PERIOD, robust=True)
        result = stl.fit()

        components = pd.DataFrame({
            "ds": series.index, 
            "y_actual": series.values,
            "y_trend": result.trend.values,
            "y_seasonal": result.seasonal.values,
            "y_residual": result.resid.values # This is the stationary data we will train on
        }).dropna()
        return components

    dam_data = get_dam_decomposition(dam_clip)

    mo.md(f"### 📊 Data Decomposition Complete\n\n- The original series is split into Trend, Seasonal, and **Residual (Stationary)** components.\n- Number of 3-hour intervals: **{len(dam_data)}**.")
    return SEASONAL_PERIOD, dam_data


@app.cell
def _(dam_data):
    # --- 1. Prepare Data for Modeling ---
    # We treat the entire series as both the training set and the test set 
    # for in-sample reconstruction.

    # Prophet requires 'ds' and 'y' columns. We use y_residual as 'y'
    prophet_df = dam_data.rename(columns={"y_residual": "y"})[["ds", "y"]]

    # SARIMAX requires an indexed series.
    sarimax_series = dam_data.set_index("ds")["y_residual"]

    return prophet_df, sarimax_series


@app.cell
def _(Prophet, SEASONAL_PERIOD, dam_data, prophet_df):
    # --- 2. Prophet Modeling (Residuals) ---
    m_prophet = Prophet(
        growth="linear", 
        seasonality_mode='additive', 
        weekly_seasonality=True, # Weekly seasonality is often found in residuals
        daily_seasonality=False
    )
    m_prophet.add_seasonality(name='seasonal_period', period=SEASONAL_PERIOD * (3/24), fourier_order=5)
    m_prophet.fit(prophet_df)
    forecast_prophet = m_prophet.predict(prophet_df)
    dam_data["prophet_residual"] = forecast_prophet["yhat"].values

    return


@app.cell
def _(pm, sarimax_series):
    # --- 3. SARIMAX Modeling (Residuals) ---
    # Use auto_arima to find the best stationary model for the residuals
    auto_model = pm.auto_arima(
        sarimax_series,
        d=0, D=0,             # Set differencing to zero as residuals are already stationary
        max_p=3, max_q=3,
        max_P=1, max_Q=1,
        m=56,                 # Use weekly seasonality (7 days * 8 intervals = 56)
        seasonal=True,
        trace=False,
        stepwise=True,
        suppress_warnings=True,
        error_action='ignore'
    )
    return (auto_model,)


@app.cell
def _(SARIMAX, auto_model, dam_data, sarimax_series):
    # Fit SARIMAX with optimized orders
    sarimax_model = SARIMAX(
        sarimax_series, 
        order=auto_model.order, 
        seasonal_order=auto_model.seasonal_order
    ).fit(disp=False)

    # Get in-sample prediction for the residuals
    sarimax_pred_residual = sarimax_model.predict(
        start=sarimax_series.index.min(), 
        end=sarimax_series.index.max()
    )
    dam_data["sarimax_residual"] = sarimax_pred_residual.values
    return


@app.cell
def _(auto_model, dam_data, mo):
    # --- 4. Reconstruct the Full Price Series ---
    # Reconstructed Price = Trend + Seasonality + Predicted Residuals
    dam_data["prophet_reconstructed"] = dam_data["y_trend"] + dam_data["y_seasonal"] + dam_data["prophet_residual"]
    dam_data["sarimax_reconstructed"] = dam_data["y_trend"] + dam_data["y_seasonal"] + dam_data["sarimax_residual"]

    mo.md(f"### 🤖 Modeling Complete\n\n- **Prophet:** Fitted to residuals, then reconstructed.\n- **SARIMAX:** Optimized orders found for residuals: {auto_model.order}x{auto_model.seasonal_order}.\n- Final reconstructed forecasts ready for comparison.")
    return


@app.cell
def _(dam_data, go, mo):
    def plot_forecast_comparison(df, market_name):
        fig = go.Figure()

        # 1. Actual Price
        fig.add_trace(go.Scatter(
            x=df["ds"], 
            y=df["y_actual"], 
            mode='lines', 
            name='Actual Price', 
            line=dict(color='blue', width=1.5)
        ))

        # 2. Prophet Reconstructed Forecast
        fig.add_trace(go.Scatter(
            x=df["ds"], 
            y=df["prophet_reconstructed"], 
            mode='lines', 
            name='Prophet Forecast', 
            line=dict(color='red', width=1.5)
        ))

        # 3. SARIMAX Reconstructed Forecast
        fig.add_trace(go.Scatter(
            x=df["ds"], 
            y=df["sarimax_reconstructed"], 
            mode='lines', 
            name='SARIMAX Forecast', 
            line=dict(color='green', width=1.5)
        ))

        fig.update_layout(
            title=f"Actual vs. Forecast (Trained on Stationary Residuals) for {market_name}",
            xaxis_title="Date (3-Hour Intervals)",
            yaxis_title="Price (ACTUAL)",
            height=700,
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        # Enable Range Slider (the horizontal bar)
        # AND ADD THE RANGE SELECTOR BUTTONS
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeslider_thickness=0.07,
            # --- CRITICAL CHANGE: Add Range Selector Buttons ---
            rangeselector=dict(
                buttons=list([
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=3, label="3m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(step="all")
                ])
            )
            # ----------------------------------------------------
        )

        return fig

    # Execute this function in your Marimo notebook (assuming dam_data is defined)
    fig_comparison = plot_forecast_comparison(dam_data, "DAM")

    mo.vstack([
        mo.md("### 📈 Forecast Comparison (DAM)"),
        mo.md("The forecasts below show the reconstructed price: **Trend + Seasonal + Predicted Residuals**."),
        mo.ui.plotly(fig_comparison)
    ])
    return


@app.cell
def _(np):
    from sklearn.metrics import mean_absolute_error, mean_squared_error

    # --- 1. Define a function to calculate all metrics ---
    def calculate_metrics(y_true, y_pred):
        """Calculates MAE, RMSE, and MAPE for a forecast."""
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    
        # Calculate MAPE, avoiding division by zero
        y_true_safe = y_true[y_true != 0]
        y_pred_safe = y_pred[y_true != 0]
        mape = np.mean(np.abs((y_true_safe - y_pred_safe) / y_true_safe)) * 100 if len(y_true_safe) > 0 else np.nan
    
        return {"MAE": mae, "RMSE": rmse, "MAPE (%)": mape}
    return (calculate_metrics,)


@app.cell
def _(calculate_metrics, dam_data):
    # --- 2. Calculate metrics for each model ---
    prophet_metrics = calculate_metrics(dam_data["y_actual"], dam_data["prophet_reconstructed"])
    sarimax_metrics = calculate_metrics(dam_data["y_actual"], dam_data["sarimax_reconstructed"])
    return prophet_metrics, sarimax_metrics


@app.cell
def _(pd, prophet_metrics, sarimax_metrics):
    # --- 3. Create a comparison DataFrame ---
    metrics_df = pd.DataFrame([prophet_metrics, sarimax_metrics], index=["Prophet", "SARIMAX"]).T
    metrics_df = metrics_df.round(3) # Round for better readability
    return (metrics_df,)


@app.cell
def _(metrics_df, mo):
    # --- 4. Display the results in a Marimo table ---
    mo.vstack([
        mo.md("### 📝 Model Performance Evaluation"),
        mo.md(
            """
            The table below compares the performance of the Prophet and SARIMAX models 
            against the actual price data using common forecasting metrics. **Lower values are better for all metrics.**

            - **MAE (Mean Absolute Error):** The average absolute difference between the predicted and actual values.
            - **RMSE (Root Mean Squared Error):** Similar to MAE but penalizes larger errors more heavily.
            - **MAPE (Mean Absolute Percentage Error):** The average absolute percentage difference, useful for understanding error relative to the actual value.
            """
        ),
        mo.ui.table(
            metrics_df.reset_index().rename(columns={'index': 'Metric'}), 
            label="Model Performance Metrics"
        )
    ])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
