import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt

    # Load structured data
    df = pd.read_csv("structured_output2.csv")
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed', utc=False)
    df = df.set_index('timestamp')

    # Restrict to only MW columns
    mw_cols = [c for c in df.columns if "MW" in c]
    df = df[mw_cols]

    # 1️⃣ DAILY ANALYSIS → Nulls per minute (select any specific day)
    day = "2025-09-01"
    df_day = df[df.index.date == pd.to_datetime(day).date()]
    null_per_min = df_day.isna().resample("1min").sum()

    plt.figure(figsize=(15,6))
    for col in mw_cols:
        plt.plot(null_per_min.index, null_per_min[col], label=col)
    plt.title(f"Null Count per Minute - {day}")
    plt.xlabel("Time")
    plt.ylabel("Null Count per Minute")
    plt.legend()
    plt.grid(True)
    plt.show()

    # 2️⃣ WEEKLY ANALYSIS → Nulls per hour
    week_start = "2025-09-01"
    week_end = "2025-09-07"
    df_week = df[week_start:week_end]
    null_per_hour = df_week.isna().resample("1H").sum()

    plt.figure(figsize=(15,6))
    for col in mw_cols:
        plt.plot(null_per_hour.index, null_per_hour[col], label=col)
    plt.title("Null Count per Hour - Weekly View")
    plt.xlabel("Date & Hour")
    plt.ylabel("Hourly Null Count")
    plt.legend()
    plt.grid(True)
    plt.show()

    # 3️⃣ MONTHLY ANALYSIS → Nulls per day
    month = "2025-09"
    df_month = df[df.index.month == pd.to_datetime(month).month]
    null_per_day = df_month.isna().resample("1D").sum()

    plt.figure(figsize=(15,6))
    for col in mw_cols:
        plt.plot(null_per_day.index, null_per_day[col], marker='o', label=col)
    plt.title("Null Count per Day - Monthly View")
    plt.xlabel("Date")
    plt.ylabel("Daily Null Count")
    plt.legend()
    plt.grid(True)
    plt.show()

    return


if __name__ == "__main__":
    app.run()
