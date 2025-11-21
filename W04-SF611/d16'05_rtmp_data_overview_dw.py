import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell
def _():
    # === MARIMO 1: DATA OVERVIEW & INITIAL DIAGNOSTICS ===
    import marimo as mo
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from sklearn.metrics import mean_absolute_error, mean_squared_error

    plt.style.use("seaborn-v0_8-whitegrid")
    return mean_absolute_error, mean_squared_error, mo, np, pd


@app.cell
def _(pd):
    df = (
        pd.read_csv("RTM P.csv", parse_dates=["START_TIME"])
        .sort_values("START_TIME")
    )

    df["ACTUAL"] = df["ACTUAL"].interpolate()
    df = (
        df[["START_TIME", "FORECAST", "ACTUAL"]]
        .set_index("START_TIME")
        .resample("15min")
        .mean()
    )
    df["ERROR"] = df["ACTUAL"] - df["FORECAST"]
    df["APE"] = abs(df["ERROR"]) / df["ACTUAL"] * 100
    df["DATE"] = df.index.date
    df["WEEK"] = df.index.isocalendar().week

    print(f"✅ Data ready: {len(df)} records | {df.index.min()} → {df.index.max()}")
    return (df,)


@app.cell
def _(df, mo):
    # --- Primary view toggle ---
    view_mode = mo.ui.radio(
        options=["Day", "Week"],
        value="Week",
        label="Select View Mode"
    )

    # --- all possible options ---
    unique_days = sorted(df["DATE"].unique())
    unique_weeks = sorted(df["WEEK"].unique())

    # --- both dropdowns ---
    time_selector_day = mo.ui.dropdown(
        options=[str(d) for d in unique_days],
        value=str(unique_days[-1]),
        label="Select Day"
    )
    time_selector_week = mo.ui.dropdown(
        options=[f"Week {w}" for w in unique_weeks],
        value=f"Week {unique_weeks[-1]}",
        label="Select Week"
    )

    # --- display both stacked ---
    view_mode, time_selector_day, time_selector_week
    return time_selector_day, time_selector_week, view_mode


@app.cell
def _(time_selector_day, time_selector_week, view_mode):
    # --- only show the dropdown matching the selected mode ---
    if view_mode.value == "Day":
        time_selector_day
    else:
        time_selector_week
    return


@app.cell
def _(df, pd, time_selector_day, time_selector_week, view_mode):
    def get_filtered_data():
        """Return filtered dataframe based on current UI selections."""
        if view_mode.value == "Day":
            sel_day = pd.to_datetime(time_selector_day.value).date()
            return df[df["DATE"] == sel_day]
        else:
            sel_week = int(time_selector_week.value.split()[-1])
            return df[df["WEEK"] == sel_week]
    return (get_filtered_data,)


@app.cell
def _(get_filtered_data):
    def show_descriptive_stats():
        data = get_filtered_data()
        stats = data.describe().T
        stats["skew"] = data.skew(numeric_only=True)
        stats["kurtosis"] = data.kurtosis(numeric_only=True)
        return stats

    show_descriptive_stats()
    return


@app.cell
def _(get_filtered_data, mo, px):

    data = get_filtered_data()

    # --- 1️⃣ Correlation heatmap ---
    corr = data.corr(numeric_only=True)

    fig5 = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        title="Correlation Matrix: Forecast, Actual, Error, APE"
    )
    fig5.update_layout(
        xaxis_title="",
        yaxis_title="",
        coloraxis_colorbar=dict(title="Correlation")
    )

    # --- 2️⃣ Forecast vs Actual scatter plot (sample up to 500 points) ---
    sample_data = data.sample(min(500, len(data)), random_state=42)

    fig6 = px.scatter(
        sample_data,
        x="FORECAST",
        y="ACTUAL",
        title="Forecast vs Actual (Sample)",
        opacity=0.7,
    )
    # Add ideal line (y = x)
    fig6.add_scatter(
        x=[data["FORECAST"].min(), data["FORECAST"].max()],
        y=[data["FORECAST"].min(), data["FORECAST"].max()],
        mode="lines",
        line=dict(color="red", dash="dash"),
        name="Ideal line (y=x)"
    )
    fig6.update_layout(
        xaxis_title="Forecast",
        yaxis_title="Actual",
        legend=dict(x=0.01, y=0.99)
    )

    # --- Display both in Marimo ---
    mo.vstack([
        mo.ui.plotly(fig5),
        mo.ui.plotly(fig6)
    ])
    return


@app.cell
def _(get_filtered_data, mo):
    import plotly.express as px
    gen_data = get_filtered_data()
    fig = px.line(gen_data, x=gen_data.index, y=['ACTUAL', 'FORECAST'], title='Actual vs Forecast')
    fig.update_xaxes(rangeslider_visible=True)
    mo.ui.plotly(fig)
    return (px,)


@app.cell
def _(
    get_filtered_data,
    mean_absolute_error,
    mean_squared_error,
    np,
    time_selector_day,
    time_selector_week,
    view_mode,
):
    def show_error_metrics():
        data = get_filtered_data()
        mae = mean_absolute_error(data["ACTUAL"], data["FORECAST"])
        rmse = np.sqrt(mean_squared_error(data["ACTUAL"], data["FORECAST"]))
        mape = np.mean(data["APE"])
        bias = np.mean(data["ERROR"])
        sel_label = time_selector_day.value if view_mode.value=="Day" else time_selector_week.value

        print(f"🔹 {view_mode.value} Performance Summary ({sel_label})")
        print(f"MAE  = {mae:.2f}")
        print(f"RMSE = {rmse:.2f}")
        print(f"MAPE = {mape:.2f}%")
        print(f"Bias = {bias:.2f}")

    show_error_metrics()
    return


@app.cell
def _(get_filtered_data, mo, px):
    dat1a = get_filtered_data()
    fig1 = px.histogram(dat1a, x="ERROR", nbins=40, title="Error Distribution (Actual - Forecast)")
    fig1.add_vline(x=0, line_dash="dash", line_color="red")
    mo.ui.plotly(fig1)
    return (dat1a,)


@app.cell
def _(dat1a, mo, px):
    # Error Boxplot
    fig2 = px.box(dat1a, y="ERROR", title="Error Boxplot", color_discrete_sequence=["skyblue"])
    mo.ui.plotly(fig2)
    return


@app.cell
def _(dat1a, mo, px):
    # IQR-based threshold visualization for ERROR

    Q1 = dat1a["ERROR"].quantile(0.25)
    Q3 = dat1a["ERROR"].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = dat1a[(dat1a["ERROR"] < lower_bound) | (dat1a["ERROR"] > upper_bound)]

    print(f"📊 IQR Range: Q1={Q1:.2f}, Q3={Q3:.2f}, IQR={IQR:.2f}")
    print(f"🟢 Acceptable Range: [{lower_bound:.2f}, {upper_bound:.2f}]")
    print(f"🚨 Outliers Detected: {len(outliers)} points")

    # Base line plot
    fig3 = px.line(
        dat1a,
        x=dat1a.index,
        y="ERROR",
        title="Forecast Error with IQR Threshold Range"
    )

    # Add shaded “normal” region between lower and upper bounds
    fig3.add_hrect(
        y0=lower_bound,
        y1=upper_bound,
        fillcolor="lightgreen",
        opacity=0.2,
        layer="below",
        line_width=0,
        annotation_text="Normal range",
        annotation_position="top left"
    )

    # Add horizontal lines for Q1, Q3, and thresholds
    fig3.add_hline(y=Q1, line_dash="dot", line_color="blue", annotation_text="Q1")
    fig3.add_hline(y=Q3, line_dash="dot", line_color="blue", annotation_text="Q3")
    fig3.add_hline(y=lower_bound, line_dash="dash", line_color="orange", annotation_text="Lower 1.5×IQR")
    fig3.add_hline(y=upper_bound, line_dash="dash", line_color="red", annotation_text="Upper 1.5×IQR")

    fig3.update_layout(
        xaxis_title="Time",
        yaxis_title="Error",
        hovermode="x unified",
        legend=dict(x=0.01, y=0.99)
    )

    mo.ui.plotly(fig3)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
