import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    # === 1️⃣ Load data ===
    df = pd.read_csv("head.csv")
    df.columns = [c.strip().lower() for c in df.columns]  # normalize column names

    # === 2️⃣ Parse timestamp and filter date range ===
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
    df = df.dropna(subset=["timestamp"])
    df = df[(df["timestamp"] >= "2025-09-01") & (df["timestamp"] <= "2025-10-01")]

    # === 3️⃣ Filter for Lower Reservoir unit ===
    lower_df = df[df["unit"].str.contains("lower", case=False, na=False)].copy()
    lower_df["head_level"] = pd.to_numeric(lower_df["head_level"], errors="coerce")
    lower_df = lower_df.dropna(subset=["head_level"])
    lower_df.set_index("timestamp", inplace=True)
    lower_df.sort_index(inplace=True)

    # === 4️⃣ Define operational range and mark out-of-range samples ===
    OPR_LOW, OPR_HIGH = 320.5, 335.5
    lower_df["out_of_range"] = (lower_df["head_level"] < OPR_LOW) | (lower_df["head_level"] > OPR_HIGH)

    # === 5️⃣ Count out-of-range values per day ===
    daily_counts = lower_df["out_of_range"].resample("D").sum()

    # === 6️⃣ Plot ===
    plt.figure(figsize=(12,5))
    plt.plot(daily_counts.index, daily_counts.values, "-o", color="royalblue")
    plt.title("Daily Out-of-Range Frequency — Lower Reservoir Level")
    plt.xlabel("Date")
    plt.ylabel("Count of Values Outside Operational Range")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=45)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

    print(f"📊 Total samples: {len(lower_df)} | Out-of-range: {lower_df['out_of_range'].sum()} samples")

    return


if __name__ == "__main__":
    app.run()
