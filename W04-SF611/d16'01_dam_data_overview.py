import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    import seaborn as sns
    from statsmodels.tsa.seasonal import seasonal_decompose

    # Load DAM data
    dam_df = pd.read_csv("DAM.csv", parse_dates=['START_TIME'])
    dam_df = dam_df.sort_values('START_TIME')

    # Clean + prepare
    dam_df['ACTUAL'] = dam_df['ACTUAL'].interpolate()
    dam_df = dam_df[['START_TIME','FORECAST','ACTUAL']]
    dam_df.set_index('START_TIME', inplace=True)

    # Resample to 15-min to ensure consistent spacing
    dam_df = dam_df.resample('15T').mean()
    dam_df['ERROR'] = dam_df['ACTUAL'] - dam_df['FORECAST']
    dam_df['APE'] = abs(dam_df['ERROR']) / dam_df['ACTUAL'] * 100

    # Add Week Number
    dam_df['WEEK'] = dam_df.index.isocalendar().week
    dam_df['DAY'] = dam_df.index.day_name()
    dam_df.head()

    return dam_df, np, pd, plt, seasonal_decompose, sns


@app.cell
def _(dam_df, plt):
    # Only numeric columns
    weekly = dam_df.select_dtypes(include='number').resample('W').mean()

    plt.figure(figsize=(13,5))
    plt.plot(weekly.index, weekly['FORECAST'], label='Forecast', marker='o')
    plt.plot(weekly.index, weekly['ACTUAL'], label='Actual', marker='o')
    plt.title("Weekly Average Forecast vs Actual")
    plt.xlabel("Week")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)
    plt.show()

    return


@app.cell
def _(dam_df, np, pd, plt):
    from sklearn.metrics import mean_absolute_error, mean_squared_error

    def weekly_metrics(group):
        mae = mean_absolute_error(group['ACTUAL'], group['FORECAST'])
        rmse = np.sqrt(mean_squared_error(group['ACTUAL'], group['FORECAST']))
        mape = np.mean(np.abs((group['ACTUAL'] - group['FORECAST']) / group['ACTUAL'])) * 100
        return pd.Series({'MAE': mae, 'RMSE': rmse, 'MAPE': mape})

    weekly_errors = dam_df.groupby('WEEK').apply(weekly_metrics)

    weekly_errors.plot(kind='bar', figsize=(10,5))
    plt.title("Weekly Error Metrics (MAE / RMSE / MAPE)")
    plt.xlabel("Week Number")
    plt.ylabel("Error Value")
    plt.grid(axis='y')
    plt.show()

    return (weekly_errors,)


@app.cell
def _(dam_df, plt, sns):
    plt.figure(figsize=(10,5))
    sns.boxplot(x='WEEK', y='ERROR', data=dam_df)
    plt.title("Weekly Distribution of Forecast Errors")
    plt.xlabel("Week Number")
    plt.ylabel("Error (Actual - Forecast)")
    plt.axhline(0, color='red', linestyle='--')
    plt.show()

    return


@app.cell
def _(dam_df, plt):
    # Create block numbers
    dam_df['BLOCK'] = ((dam_df.index.hour * 60 + dam_df.index.minute) / 15 + 1).astype(int)

    block_avg = dam_df.groupby('BLOCK')[['FORECAST','ACTUAL']].mean()

    plt.figure(figsize=(12,5))
    plt.plot(block_avg.index, block_avg['FORECAST'], label='Forecast Avg')
    plt.plot(block_avg.index, block_avg['ACTUAL'], label='Actual Avg')
    plt.title("Average 96-Block Pattern (2-Month Aggregate)")
    plt.xlabel("Block (1–96)")
    plt.ylabel("MW")
    plt.legend()
    plt.show()

    return


@app.cell
def _(dam_df, plt, sns):
    heatmap_df = dam_df.pivot_table(index='WEEK', columns='BLOCK', values='APE', aggfunc='mean')

    plt.figure(figsize=(14,6))
    sns.heatmap(heatmap_df, cmap='coolwarm', center=0)
    plt.title("Weekly-Block Heatmap of % Absolute Error (APE)")
    plt.xlabel("Block (1–96)")
    plt.ylabel("Week Number")
    plt.show()

    return


@app.cell
def _(dam_df, plt, seasonal_decompose):
    result = seasonal_decompose(dam_df['ACTUAL'], model='additive', period=96*7)
    result.plot()
    plt.suptitle("7-Day Seasonal Decomposition of Actuals", y=1.02)
    plt.show()

    return


@app.cell
def _(dam_df, plt, sns):
    sns.lmplot(x='FORECAST', y='ACTUAL', data=dam_df.sample(500))  # sample for visual clarity
    plt.title("Forecast vs Actual Correlation")
    plt.xlabel("Forecast")
    plt.ylabel("Actual")
    plt.show()

    return


@app.cell
def _(dam_df, weekly_errors):
    summary = weekly_errors.copy()
    summary['Bias'] = dam_df.groupby('WEEK')['ERROR'].mean()
    summary['Mean Forecast'] = dam_df.groupby('WEEK')['FORECAST'].mean()
    summary['Mean Actual'] = dam_df.groupby('WEEK')['ACTUAL'].mean()
    summary

    return


@app.cell
def _(dam_df, plt):
    rolling_mape = dam_df['APE'].rolling(96*3).mean()

    plt.figure(figsize=(10,5))
    plt.plot(rolling_mape.index, rolling_mape, color='purple')
    plt.title("Rolling 3-Day MAPE Trend")
    plt.ylabel("MAPE (%)")
    plt.xlabel("Date")
    plt.grid(True)
    plt.show()

    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
