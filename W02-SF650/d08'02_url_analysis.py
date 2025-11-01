import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np

    # Load file
    df = pd.read_csv("url.csv")

    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]

    # Detect timestamp/value column
    time_col = "timestamp"
    url_col = [c for c in df.columns if "reservoir" in c or "url" in c][0]

    # Parse timestamp
    df[time_col] = pd.to_datetime(df[time_col], errors="coerce", utc=True)
    df.set_index(time_col, inplace=True)
    df.sort_index(inplace=True)

    # Inspect range
    print(df[url_col].describe())

    # Define realistic operational range
    OPR_LOW, OPR_HIGH = 445, 460

    # Rolling average for smooth visualization
    df["smoothed"] = df[url_col].rolling(window=10, min_periods=1).mean()

    # Detect outliers (IQR)
    Q1 = df[url_col].quantile(0.25)
    Q3 = df[url_col].quantile(0.75)
    IQR = Q3 - Q1
    low_iqr, high_iqr = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    outliers = (df[url_col] < low_iqr) | (df[url_col] > high_iqr)

    # Nulls
    null_pct = df[url_col].isna().mean() * 100

    # Plot 1️⃣: Trend with Operational Limits
    plt.figure(figsize=(15, 6))
    plt.plot(df.index, df["smoothed"], color="cyan", label="URL (Smoothed)", alpha=0.8)
    plt.scatter(df.index[outliers], df[url_col][outliers], color="red", s=10, label="Outliers")
    plt.axhline(OPR_LOW, color="green", linestyle="--", label=f"Min OPR ({OPR_LOW})")
    plt.axhline(OPR_HIGH, color="orange", linestyle="--", label=f"Max OPR ({OPR_HIGH})")
    plt.title("Upper Reservoir Level — Valid Range & Outlier Visualization")
    plt.xlabel("Time")
    plt.ylabel("Reservoir Level (m)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

    # Plot 2️⃣: Boxplot for Data Distribution
    plt.figure(figsize=(10, 3))
    plt.boxplot(df[url_col].dropna(), vert=False, patch_artist=True, boxprops=dict(facecolor='skyblue'))
    plt.title("Reservoir Level Distribution (Box Plot)")
    plt.xlabel("Reservoir Level (m)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

    # Plot 3️⃣: Sampling frequency
    freq_per_min = df[url_col].resample("1min").count()
    plt.figure(figsize=(15, 4))
    plt.plot(freq_per_min.index, freq_per_min.values, color="violet")
    plt.title("Sampling Frequency per Minute — Upper Reservoir Level")
    plt.ylabel("Samples/min")
    plt.xlabel("Time")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

    print(f"\n⚙️ Missing Data: {null_pct:.2f}%")
    print(f"⚙️ Outliers: {outliers.sum()} points")
    print(f"⚙️ Range Violations: {(df[url_col] < OPR_LOW).sum()} below, {(df[url_col] > OPR_HIGH).sum()} above")
    return


if __name__ == "__main__":
    app.run()
