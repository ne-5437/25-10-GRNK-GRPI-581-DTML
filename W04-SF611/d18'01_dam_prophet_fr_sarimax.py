import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import plotly.graph_objects as go

    from prophet import Prophet
    from statsmodels.tsa.statespace.sarimax import SARIMAX

    from sklearn.metrics import mean_absolute_error, mean_squared_error
    return Prophet, SARIMAX, go, pd


@app.cell
def _(pd):
    df = pd.read_csv("DAM-MAY-TO-OCT.csv", parse_dates=["START_TIME"])
    df = df.sort_values("START_TIME")

    df = df[["START_TIME", "FORECAST", "ACTUAL"]]
    df = df.set_index("START_TIME").resample("15min").mean().interpolate()

    try:
        df.index = df.index.tz_convert(None)
    except:
        try:
            df.index = df.index.tz_localize(None)
        except:
            pass

    df["WEEK"] = df.index.isocalendar().week

    # Train 
    train = df[(df["WEEK"] >= 19) & (df["WEEK"] <= 40)]

    # Test 
    test  = df[(df["WEEK"] >= 41) & (df["WEEK"] <= 43)]

    print("Train:", train.index.min(), "→", train.index.max(), "|", len(train), "records")
    print("Test :", test.index.min(), "→", test.index.max(), "|", len(test), "records")
    return test, train


@app.cell
def _(Prophet, test, train):
    df_train = train.reset_index()[["START_TIME", "ACTUAL"]].rename(
        columns={"START_TIME": "ds", "ACTUAL": "y"}
    )
    df_train["ds"] = df_train["ds"].dt.tz_localize(None)

    p_model = Prophet(
        daily_seasonality=True,
        weekly_seasonality=True
    )
    p_model.fit(df_train)

    horizon = len(test)
    future = p_model.make_future_dataframe(periods=horizon, freq="15min")
    p_fc = p_model.predict(future)

    # Forecast 
    prophet_pred = p_fc["yhat"].iloc[len(train):len(train)+len(test)]
    prophet_pred.index = test.index

    prophet_pred.head()
    return (prophet_pred,)


@app.cell
def _(SARIMAX, test, train):
    from statsmodels.tsa.deterministic import CalendarFourier, DeterministicProcess

    _fourier = CalendarFourier(freq="D", order=10)
    _dp_train = DeterministicProcess(
        index=train.index,
        constant=True,           
        order=1,                 
        seasonal=False,
        additional_terms=[_fourier],
        drop=True
    )
    _exog_train = _dp_train.in_sample()

    _dp_test = DeterministicProcess(
        index=test.index,
        constant=True,
        order=1,
        seasonal=False,
        additional_terms=[_fourier],
        drop=True
    )
    _exog_test = _dp_test.in_sample()

    # SARIMAX Fit
    _model_fx = SARIMAX(
        train["ACTUAL"],
        exog=_exog_train,
        order=(1,0,1),          
        enforce_stationarity=False,
        enforce_invertibility=False
    )
    _fit_fx = _model_fx.fit(disp=False)

    # Forecast 
    _pred_fx = _fit_fx.get_forecast(steps=len(test), exog=_exog_test)
    sarima_fixed = _pred_fx.predicted_mean
    sarima_fixed.index = test.index

    print("Fourier-SARIMAX forecast sample:")
    print(sarima_fixed.head())
    return (sarima_fixed,)


@app.cell
def _(go, prophet_pred, sarima_fixed):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=prophet_pred.index, y=prophet_pred.values,
        mode="lines", name="Prophet Forecast", line=dict(color="red")
    ))
    fig.add_trace(go.Scatter(
        x=sarima_fixed.index, y=sarima_fixed.values,
        mode="lines", name="SARIMA (Fourier) Forecast", line=dict(color="blue")
    ))
    fig.update_layout(
        title="Prophet vs SARIMA (Fourier-SARIMAX) — Weeks 41–43",
        xaxis_title="Time",
        yaxis_title="MW",
        height=500
    )
    fig
    return


@app.cell
def _(go, prophet_pred, sarima_fixed, test):
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=test.index, y=test["ACTUAL"],
        mode="lines", name="Actual", line=dict(color="green")
    ))
    fig2.add_trace(go.Scatter(
        x=prophet_pred.index, y=prophet_pred.values,
        mode="lines", name="Prophet Forecast", line=dict(color="red")
    ))
    fig2.add_trace(go.Scatter(
        x=sarima_fixed.index, y=sarima_fixed.values,
        mode="lines", name="SARIMA (Fourier) Forecast", line=dict(color="blue")
    ))
    fig2.update_layout(
        title="Actual vs Prophet vs SARIMA (Fourier-SARIMAX) — Weeks 41–43",
        xaxis_title="Time",
        yaxis_title="MW",
        height=500
    )
    fig2
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
