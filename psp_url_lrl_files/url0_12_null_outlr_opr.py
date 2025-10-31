import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import numpy as np

    # Data Loading
    df = pd.read_csv("merged_output.csv")
    df.columns = [c.strip().lower() for c in df.columns]
    df["timestamp_raw"] = df["pt"].fillna(df["dt"])

    # Timestamp conversion
    def convert_to_datetime(x):
        if isinstance(x, str):
            return pd.to_datetime(x, errors="coerce", utc=True)
        if pd.api.types.is_number(x):
            if x > 1e11:  # milliseconds
                return pd.to_datetime(x, unit="ms", utc=True)
            elif x > 1e9:  # seconds
                return pd.to_datetime(x, unit="s", utc=True)
        return pd.NaT

    df["timestamp"] = df["timestamp_raw"].apply(convert_to_datetime)
    df.dropna(subset=["timestamp"], inplace=True)
    df.sort_values("timestamp", inplace=True)

    # Monitor seperation
    monitor1 = df[df["id"].str.contains("UpperReservoir.Monitor1", case=False, na=False)][["timestamp", "v"]].rename(columns={"v": "url1"})
    monitor2 = df[df["id"].str.contains("UpperReservoir.Monitor2", case=False, na=False)][["timestamp", "v"]].rename(columns={"v": "url2"})

    merged = pd.merge_asof(
        monitor1.sort_values("timestamp"),
        monitor2.sort_values("timestamp"),
        on="timestamp",
        direction="nearest",
        tolerance=pd.Timedelta("1min")
    )

    # Operating ranges
    OPR_LOW, OPR_HIGH = 445.5, 461
    merged.set_index("timestamp", inplace=True)

    # Outlier Detection
    def sigma_outliers(series, sigma=3):
        mean, std = series.mean(), series.std()
        upper, lower = mean + sigma * std, mean - sigma * std
        mask = (series > upper) | (series < lower)
        return mask, lower, upper

    out3_m1, low3_m1, up3_m1 = sigma_outliers(merged["url1"], 3)
    out5_m1, low5_m1, up5_m1 = sigma_outliers(merged["url1"], 5)
    out3_m2, low3_m2, up3_m2 = sigma_outliers(merged["url2"], 3)
    out5_m2, low5_m2, up5_m2 = sigma_outliers(merged["url2"], 5)

    #Plotting
    plt.figure(figsize=(15,6))
    plt.plot(merged.index, merged["url1"], color="cyan", alpha=0.7, label="Monitor 1")
    plt.plot(merged.index, merged["url2"], color="orange", alpha=0.7, label="Monitor 2")
    plt.scatter(merged.index[out3_m1], merged["url1"][out3_m1], color="red", s=10, label="3σ Outliers M1")
    plt.scatter(merged.index[out3_m2], merged["url2"][out3_m2], color="purple", s=10, label="3σ Outliers M2")
    plt.axhline(low3_m1, color="blue", linestyle="--", alpha=0.4)
    plt.axhline(up3_m1, color="blue", linestyle="--", alpha=0.4)
    plt.axhline(low5_m1, color="gray", linestyle="--", alpha=0.3)
    plt.axhline(up5_m1, color="gray", linestyle="--", alpha=0.3)
    plt.title("Outlier Detection — 3σ / 5σ Range")
    plt.xlabel("Timestamp")
    plt.ylabel("Reservoir Level (m)")
    plt.legend()
    plt.grid(alpha=0.3)
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    print(f"Monitor1: {out3_m1.sum()} (3σ), {out5_m1.sum()} (5σ) outliers")
    print(f"Monitor2: {out3_m2.sum()} (3σ), {out5_m2.sum()} (5σ) outliers")

    # Null check
    null_m1 = merged["url1"].isna().sum()
    null_m2 = merged["url2"].isna().sum()

    plt.figure(figsize=(6,4))
    plt.bar(["Monitor 1", "Monitor 2"], [null_m1, null_m2], color=["cyan","orange"])
    plt.title("Null Value Counts")
    plt.ylabel("Count of Missing Values")
    plt.tight_layout()
    plt.show()

    print(f"Null % — M1: {merged['url1'].isna().mean()*100:.2f}% | M2: {merged['url2'].isna().mean()*100:.2f}%")

    # Frequency check
    merged["delta"] = merged.index.to_series().diff().dt.total_seconds()

    plt.figure(figsize=(12,4))
    plt.hist(merged["delta"].dropna(), bins=50, color="violet", edgecolor="black")
    plt.title("Sampling Interval Distribution (seconds)")
    plt.xlabel("Interval (s)")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(15,4))
    plt.plot(merged.index, merged["delta"], color="gray", alpha=0.7)
    plt.title("Sampling Interval Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("Interval (s)")
    plt.grid(alpha=0.3)
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    print(f"Average Sampling Interval: {merged['delta'].mean():.2f} seconds")

    # Operational range
    below1 = merged["url1"] < OPR_LOW
    above1 = merged["url1"] > OPR_HIGH
    below2 = merged["url2"] < OPR_LOW
    above2 = merged["url2"] > OPR_HIGH

    plt.figure(figsize=(15,6))
    plt.plot(merged.index, merged["url1"], color="cyan", alpha=0.8, label="Monitor 1")
    plt.plot(merged.index, merged["url2"], color="orange", alpha=0.8, label="Monitor 2")
    plt.fill_between(merged.index, OPR_LOW, OPR_HIGH, color="green", alpha=0.1, label="Normal Range")
    plt.scatter(merged.index[below1|above1], merged["url1"][below1|above1], color="red", s=10, label="Range Violations M1")
    plt.scatter(merged.index[below2|above2], merged["url2"][below2|above2], color="purple", s=10, label="Range Violations M2")
    plt.axhline(OPR_LOW, color="green", linestyle="--")
    plt.axhline(OPR_HIGH, color="red", linestyle="--")
    plt.title("Operational Range Violations (445.5–461 m)")
    plt.xlabel("Timestamp")
    plt.ylabel("Reservoir Level (m)")
    plt.legend()
    plt.grid(alpha=0.3)
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    print(f"M1 Violations: {(below1|above1).sum()} | M2 Violations: {(below2|above2).sum()}")

    return


if __name__ == "__main__":
    app.run()
