import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import numpy as np

    # === 1️⃣ Load file ===
    df = pd.read_csv("url.csv")
    df.columns = [c.strip().lower() for c in df.columns]

    # Detect timestamp and value column
    time_col = "timestamp"
    url_col = [c for c in df.columns if "reservoir" in c or "url" in c][0]

    # === 2️⃣ Parse timestamp ===
    df[time_col] = pd.to_datetime(df[time_col], errors="coerce", utc=True)
    df.set_index(time_col, inplace=True)
    df.sort_index(inplace=True)

    # === 3️⃣ Filter month range ===
    df = df.loc["2025-09-01":"2025-10-01"]

    # === 4️⃣ Define operational range ===
    OPR_LOW, OPR_HIGH = 445.5, 461

    # === 5️⃣ Detect values outside range ===
    df["out_of_range"] = (df[url_col] < OPR_LOW) | (df[url_col] > OPR_HIGH)

    # === 6️⃣ Daily out-of-range frequency ===
    daily_counts = df["out_of_range"].resample("D").sum()

    plt.figure(figsize=(12,5))
    plt.plot(daily_counts.index, daily_counts.values, "-o", color="royalblue")
    plt.title("Daily Out-of-Range Frequency — Upper Reservoir Level")
    plt.xlabel("Date")
    plt.ylabel("Count of Values Outside Operational Range")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=45)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

    # === 7️⃣ Hourly breakdown for worst (max-violation) day ===
    if daily_counts.sum() > 0:
        max_day = daily_counts.idxmax().normalize()
        day_df = df.loc[str(max_day.date())]
        hourly_counts = day_df["out_of_range"].resample("H").sum()

        plt.figure(figsize=(12,5))
        plt.plot(hourly_counts.index, hourly_counts.values, "-o", color="crimson")
        plt.title(f"Hourly Out-of-Range Frequency — {max_day.date()} — Upper Reservoir Level")
        plt.xlabel("Hour (UTC)")
        plt.ylabel("Out-of-Range Count")
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        plt.xticks(rotation=45)
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.show()
    else:
        print("✅ No values outside operational range — skipping hourly plot.")

    # === 8️⃣ Summary ===
    below = (df[url_col] < OPR_LOW).sum()
    above = (df[url_col] > OPR_HIGH).sum()
    print(f"📊 Total samples: {len(df)}")
    print(f"⚙️ Out-of-range samples: {df['out_of_range'].sum()} (Below: {below}, Above: {above})")
    return


if __name__ == "__main__":
    app.run()
