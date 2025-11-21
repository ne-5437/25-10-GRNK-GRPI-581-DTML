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
    from sklearn.metrics import mean_absolute_error, mean_squared_error

    plt.style.use("seaborn-v0_8-whitegrid")
    return mean_absolute_error, mean_squared_error, mo, np, pd, plt, sns


@app.cell
def _(pd):
    # Load DAM dataset
    df = pd.read_csv("DAM.csv", parse_dates=['START_TIME'])
    df = df.sort_values('START_TIME')

    # Fill missing Actuals if any
    df['ACTUAL'] = df['ACTUAL'].interpolate()

    # Keep relevant columns, resample to 15-min
    df = df[['START_TIME', 'FORECAST', 'ACTUAL']].set_index('START_TIME').resample('15min').mean()

    # Compute error metrics
    df['ERROR'] = df['ACTUAL'] - df['FORECAST']
    df['APE'] = abs(df['ERROR']) / df['ACTUAL'] * 100

    # Add time grouping columns for dropdowns
    df['DATE'] = df.index.date
    df['WEEK'] = df.index.isocalendar().week

    print(f"✅ Data prepared. Records: {len(df)} | Range: {df.index.min()} → {df.index.max()}")
    return (df,)


@app.cell
def _(df, mo):
    # --- create the widgets ---
    view_mode = mo.ui.radio(
        options=["Day", "Week"],
        value="Week",
        label="Select View Mode",
    )

    unique_days = sorted(df["DATE"].unique())
    unique_weeks = sorted(df["WEEK"].unique())

    time_selector_day = mo.ui.dropdown(
        options=[str(d) for d in unique_days],
        value=str(unique_days[-1]),
        label="Select Day",
    )

    time_selector_week = mo.ui.dropdown(
        options=[f"Week {w}" for w in unique_weeks],
        value=f"Week {unique_weeks[-1]}",
        label="Select Week",
    )

    # show the main toggle
    view_mode

    return time_selector_day, time_selector_week, view_mode


@app.cell
def _(time_selector_day, time_selector_week, view_mode):
    # --- show the right dropdown based on the toggle ---
    if view_mode.value == "Day":
        time_selector_day
    else:
        time_selector_week
    return


@app.cell
def _(df, pd, time_selector_day, time_selector_week, view_mode):
    def get_filtered_data():
        """Return dataframe filtered by the current dropdown selections."""
        if view_mode.value == "Day":
            selected_day = pd.to_datetime(time_selector_day.value).date()
            return df[df["DATE"] == selected_day]
        else:
            selected_week = int(time_selector_week.value.split()[-1])
            return df[df["WEEK"] == selected_week]

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
def _(get_filtered_data, plt, sns):
    def plot_correlation_and_scatter():
        data = get_filtered_data()

        corr = data.corr(numeric_only=True)
        plt.figure(figsize=(6,4))
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Correlation Matrix: Forecast, Actual, Error, APE")
        plt.show()

        plt.figure(figsize=(6,6))
        sns.scatterplot(x="FORECAST", y="ACTUAL", data=data.sample(min(500, len(data))))
        plt.plot(
            [data["FORECAST"].min(), data["FORECAST"].max()],
            [data["FORECAST"].min(), data["FORECAST"].max()],
            "r--",
        )
        plt.title("Forecast vs Actual (Sample)")
        plt.xlabel("Forecast")
        plt.ylabel("Actual")
        plt.show()

    plot_correlation_and_scatter()
    return


@app.cell
def _(
    get_filtered_data,
    plt,
    time_selector_day,
    time_selector_week,
    view_mode,
):
    def plot_forecast_vs_actual():
        data = get_filtered_data()
        plt.figure(figsize=(12,5))
        plt.plot(data.index, data["FORECAST"], label="Forecast", alpha=0.8)
        plt.plot(data.index, data["ACTUAL"], label="Actual", alpha=0.8)
        title_suffix = time_selector_day.value if view_mode.value == "Day" else time_selector_week.value
        plt.title(f"DAM Forecast vs Actual ({view_mode.value}: {title_suffix})")
        plt.xlabel("Time")
        plt.ylabel("Value")
        plt.legend()
        plt.show()

    plot_forecast_vs_actual()

    return


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
        title_suffix = time_selector_day.value if view_mode.value == "Day" else time_selector_week.value
        print(f"🔹 {view_mode.value} Performance Summary ({title_suffix})")
        print(f"MAE  = {mae:.2f}")
        print(f"RMSE = {rmse:.2f}")
        print(f"MAPE = {mape:.2f}%")
        print(f"Bias = {bias:.2f}")

    show_error_metrics()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
