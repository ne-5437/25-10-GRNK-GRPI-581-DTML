import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from prophet import Prophet
    from sklearn.metrics import mean_absolute_error, mean_squared_error
    from statsmodels.tsa.statespace.sarimax import SARIMAX

    plt.style.use("seaborn-v0_8-whitegrid")
    return mo, pd


@app.cell
def _(pd):
    # === Load CSV ===
    df = pd.read_csv("DAM.csv", parse_dates=["START_TIME"]).sort_values("START_TIME")

    # Keep only required columns
    df = df[["START_TIME", "FORECAST", "ACTUAL"]]
    df = df.set_index("START_TIME").resample("15min").mean().interpolate()

    # 🔧 Make index timezone-naive (Prophet doesn’t support tz-aware datetimes)
    try:
        df.index = df.index.tz_convert(None)
    except (TypeError, AttributeError):
        try:
            df.index = df.index.tz_localize(None)
        except Exception:
            pass

    # Additional columns for filtering
    df["ERROR"] = df["ACTUAL"] - df["FORECAST"]
    df["WEEK"] = df.index.isocalendar().week
    df["DATE"] = df.index.date

    print(f"✅ Data ready: {len(df)} records")
    print(f"📆 Range: {df.index.min()} → {df.index.max()}")
    df.head()
    return (df,)


@app.cell
def _(df, mo):
    # --- Create UI Controls ---
    view_mode = mo.ui.radio(
        options=["Day", "Week"],
        value="Week",
        label="Select View Mode"
    )

    unique_days = sorted(df["DATE"].unique())
    unique_weeks = sorted(df["WEEK"].unique())

    day_selector = mo.ui.dropdown(
        options=[str(d) for d in unique_days],
        value=str(unique_days[-1]),
        label="Select Day"
    )

    week_selector = mo.ui.dropdown(
        options=[f"Week {w}" for w in unique_weeks],
        value=f"Week {unique_weeks[-1]}",
        label="Select Week"
    )

    # --- Display all controls stacked ---
    mo.vstack([
        view_mode,
        day_selector,
        week_selector
    ])
    return day_selector, view_mode, week_selector


@app.cell
def _(day_selector, df, pd, view_mode, week_selector):
    def get_filtered_data():
        if view_mode.value == "Day":
            sel_day = pd.to_datetime(day_selector.value).date()
            filtered = df[df["DATE"] == sel_day]
        else:
            sel_week = int(week_selector.value.split()[-1])
            filtered = df[df["WEEK"] == sel_week]

        print(f"📆 Selected {view_mode.value}: {day_selector.value if view_mode.value == 'Day' else week_selector.value}")
        print(f"Records: {len(filtered)} | From {filtered.index.min()} → {filtered.index.max()}")
        return filtered
    return (get_filtered_data,)


@app.function
def rmse_metric(y_true, y_pred):
    import numpy as np
    from sklearn.metrics import mean_squared_error
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))


@app.cell
def _(day_selector, get_filtered_data, mo, view_mode, week_selector):
    def prophet_interactive():
        import plotly.graph_objects as go
        import pandas as pd
        from prophet import Prophet
        from sklearn.metrics import mean_absolute_error

        d = get_filtered_data()
        if len(d) < 100:
            print("⚠️ Not enough data points for Prophet model.")
            return

        df_p = (
            d.reset_index()[["START_TIME","ACTUAL"]]
              .rename(columns={"START_TIME":"ds","ACTUAL":"y"})
        )
        df_p["ds"] = pd.to_datetime(df_p["ds"]).dt.tz_localize(None)

        model_p = Prophet(daily_seasonality=True, weekly_seasonality=True)
        model_p.fit(df_p)

        future = model_p.make_future_dataframe(periods=96, freq="15min")
        forecast = model_p.predict(future)

        y_true_local = df_p["y"].values
        y_pred_local = forecast["yhat"].iloc[:len(df_p)].values
        mae_local = mean_absolute_error(y_true_local, y_pred_local)
        rmse_local = rmse_metric(y_true_local, y_pred_local)

        print(f"🔮 Prophet → MAE {mae_local:.2f} | RMSE {rmse_local:.2f}")

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=d.index, y=d["ACTUAL"], mode="lines",
                                 name="Actual", line=dict(color="red", width=1.5)))
        fig.add_trace(go.Scatter(x=d.index,
                                 y=forecast["yhat"].iloc[:len(d)],
                                 mode="lines", name="Prophet Fit",
                                 line=dict(color="royalblue", width=1.5)))

        title_sel = day_selector.value if view_mode.value=="Day" else week_selector.value
        fig.update_layout(title=f"Prophet Forecast — {view_mode.value}: {title_sel}",
                          xaxis_title="Time", yaxis_title="MW", height=450)
        fig.update_xaxes(rangeslider_visible=True)

        return mo.ui.plotly(fig)

    prophet_interactive()
    return


@app.cell
def _(day_selector, get_filtered_data, mo, view_mode, week_selector):
    def sarima_interactive():
        import plotly.graph_objects as go
        from statsmodels.tsa.statespace.sarimax import SARIMAX
        from sklearn.metrics import mean_absolute_error

        d = get_filtered_data()
        if len(d) < 100:
            print("⚠️ Not enough data points for SARIMA model.")
            return

        sarima_model = SARIMAX(d["ACTUAL"], order=(1,1,1), seasonal_order=(1,1,1,96))
        sarima_fit = sarima_model.fit(disp=False)

        y_true_local = d["ACTUAL"].values
        y_pred_local = sarima_fit.fittedvalues.values
        mae_local = mean_absolute_error(y_true_local, y_pred_local)
        rmse_local = rmse_metric(y_true_local, y_pred_local)

        print(f"📈 SARIMA → MAE {mae_local:.2f} | RMSE {rmse_local:.2f}")

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=d.index, y=d["ACTUAL"], mode="lines",
                                 name="Actual", line=dict(color="green", width=1.3)))
        fig.add_trace(go.Scatter(x=d.index, y=sarima_fit.fittedvalues, mode="lines",
                                 name="SARIMA Fit", line=dict(color="pink")))

        title_sel = day_selector.value if view_mode.value=="Day" else week_selector.value
        fig.update_layout(title=f"SARIMA Fit — {view_mode.value}: {title_sel}",
                          xaxis_title="Time", yaxis_title="MW", height=450)
        fig.update_xaxes(rangeslider_visible=True)

        return mo.ui.plotly(fig)

    sarima_interactive()
    return


@app.cell
def _(day_selector, get_filtered_data, mo, view_mode, week_selector):
    def compare_models_interactive():
        import plotly.graph_objects as go
        import pandas as pd
        from prophet import Prophet
        from statsmodels.tsa.statespace.sarimax import SARIMAX
        from sklearn.metrics import mean_absolute_error

        d = get_filtered_data()
        if len(d) < 100:
            print("⚠️ Not enough data for combined comparison.")
            return

        # Prophet fit
        df_p = (
            d.reset_index()[["START_TIME","ACTUAL"]]
              .rename(columns={"START_TIME":"ds","ACTUAL":"y"})
        )
        df_p["ds"] = pd.to_datetime(df_p["ds"]).dt.tz_localize(None)
        p_model = Prophet(daily_seasonality=True, weekly_seasonality=True)
        p_model.fit(df_p)
        p_fc = p_model.predict(p_model.make_future_dataframe(periods=96, freq="15min"))

        # SARIMA fit
        s_model = SARIMAX(d["ACTUAL"], order=(1,1,1), seasonal_order=(1,1,1,96))
        s_fit = s_model.fit(disp=False)

        # Metrics
        y_true_p = df_p["y"].values
        y_pred_p = p_fc["yhat"].iloc[:len(df_p)].values
        mae_p = mean_absolute_error(y_true_p, y_pred_p)
        rmse_p = rmse_metric(y_true_p, y_pred_p)

        y_true_s = d["ACTUAL"].values
        y_pred_s = s_fit.fittedvalues.values
        mae_s = mean_absolute_error(y_true_s, y_pred_s)
        rmse_s = rmse_metric(y_true_s, y_pred_s)

        print(f"⚖️ Prophet → MAE {mae_p:.2f} | RMSE {rmse_p:.2f}")
        print(f"⚖️ SARIMA  → MAE {mae_s:.2f} | RMSE {rmse_s:.2f}")

        # Plotly figure
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=d.index, y=d["ACTUAL"], mode="lines",
                                 name="Actual", line=dict(color="green")))
        fig.add_trace(go.Scatter(x=d.index, y=d["FORECAST"], mode="lines",
                                 name="IEX Forecast", line=dict(color="pink")))
        fig.add_trace(go.Scatter(x=d.index, y=s_fit.fittedvalues, mode="lines",
                                 name="SARIMA Fit", line=dict(color="blue")))
        fig.add_trace(go.Scatter(x=d.index, y=p_fc["yhat"].iloc[:len(d)], mode="lines",
                                 name="Prophet Fit", line=dict(color="red")))

        title_sel = day_selector.value if view_mode.value=="Day" else week_selector.value
        fig.update_layout(title=f"Model Comparison — {view_mode.value}: {title_sel}",
                          xaxis_title="Time", yaxis_title="MW", height=500)
        fig.update_xaxes(rangeslider_visible=True)

        return mo.ui.plotly(fig)

    compare_models_interactive()
    return


@app.cell
def _(df, mo, pd):
    # Ensure DATE column is timezone-naive
    df["DATE"] = pd.to_datetime(df["DATE"]).dt.tz_localize(None)

    # Derive month (start of each month)
    df["MONTH"] = df["DATE"].dt.to_period("M").dt.to_timestamp()

    unique_months = sorted(df["MONTH"].unique())

    month_selector = mo.ui.dropdown(
        options=[str(m) for m in unique_months],
        value=str(unique_months[-1]),
        label="Select Month for 4-Week Trend Analysis"
    )

    month_selector
    return (month_selector,)


@app.cell
def _(df, mo, month_selector):
    def prophet_monthly_trend():
        import plotly.graph_objects as go
        from prophet import Prophet
        from sklearn.metrics import mean_absolute_error
        import pandas as pd

        # filter month
        sel_month = pd.to_datetime(month_selector.value)
        month_df = df[df["MONTH"] == sel_month]

        if month_df.empty:
            print("⚠️ No data for selected month.")
            return

        # group by week
        weeks = sorted(month_df["WEEK"].unique())[:4]  # limit to 4 weeks max
        fig = go.Figure()

        for w in weeks:
            week_data = month_df[month_df["WEEK"] == w]
            if len(week_data) < 100:
                continue

            df_p = (
                week_data.reset_index()[["START_TIME", "ACTUAL"]]
                .rename(columns={"START_TIME": "ds", "ACTUAL": "y"})
            )
            df_p["ds"] = pd.to_datetime(df_p["ds"]).dt.tz_localize(None)

            model_p = Prophet(daily_seasonality=True, weekly_seasonality=True)
            model_p.fit(df_p)
            fc = model_p.predict(model_p.make_future_dataframe(periods=96, freq="15min"))

            fig.add_trace(go.Scatter(
                x=week_data.index,
                y=fc["yhat"].iloc[:len(week_data)],
                mode="lines",
                name=f"Week {w} (Prophet)",
                line=dict(dash="solid")
            ))

        fig.add_trace(go.Scatter(
            x=month_df.index, y=month_df["ACTUAL"],
            mode="lines", name="Actual", line=dict(color="white", width=1)
        ))

        fig.update_layout(
            title=f"Prophet Monthly Trend Overlay — {sel_month.strftime('%B %Y')}",
            xaxis_title="Time", yaxis_title="MW", height=500,
            legend_title="Weeks"
        )
        fig.update_xaxes(rangeslider_visible=True)

        return mo.ui.plotly(fig)

    prophet_monthly_trend()
    return


@app.cell
def _(df, mo, month_selector):
    def sarima_monthly_trend():
        import plotly.graph_objects as go
        from statsmodels.tsa.statespace.sarimax import SARIMAX
        import pandas as pd

        sel_month = pd.to_datetime(month_selector.value)
        month_df = df[df["MONTH"] == sel_month]

        if month_df.empty:
            print("⚠️ No data for selected month.")
            return

        weeks = sorted(month_df["WEEK"].unique())[:4]
        fig = go.Figure()

        for w in weeks:
            week_data = month_df[month_df["WEEK"] == w]
            if len(week_data) < 100:
                continue

            sarima_model = SARIMAX(week_data["ACTUAL"], order=(1,1,1), seasonal_order=(1,1,1,96))
            sarima_fit = sarima_model.fit(disp=False)

            fig.add_trace(go.Scatter(
                x=week_data.index,
                y=sarima_fit.fittedvalues,
                mode="lines",
                name=f"Week {w} (SARIMA)",
                line=dict(dash="solid")
            ))

        fig.add_trace(go.Scatter(
            x=month_df.index, y=month_df["ACTUAL"],
            mode="lines", name="Actual", line=dict(color="white", width=1)
        ))

        fig.update_layout(
            title=f"SARIMA Monthly Trend Overlay — {sel_month.strftime('%B %Y')}",
            xaxis_title="Time", yaxis_title="MW", height=500,
            legend_title="Weeks"
        )
        fig.update_xaxes(rangeslider_visible=True)

        return mo.ui.plotly(fig)

    sarima_monthly_trend()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
