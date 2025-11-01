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
    df = pd.read_csv("merged_output.csv")
    df.columns = [c.strip().lower() for c in df.columns]

    # === 2️⃣ Combine pt and dt into one column ===
    df["timestamp_raw"] = df["pt"].fillna(df["dt"])

    # === 3️⃣ Detect timestamp format ===
    def convert_to_datetime(x):
        # If already looks like a string date
        if isinstance(x, str):
            return pd.to_datetime(x, errors="coerce", utc=True)
        # If numeric — guess seconds vs milliseconds
        if pd.api.types.is_numeric_dtype(type(x)) or isinstance(x, (int, float, np.number)):
            # Large values → milliseconds
            if x > 1e11:
                return pd.to_datetime(x, unit="ms", utc=True)
            # Smaller values → seconds
            elif x > 1e9:
                return pd.to_datetime(x, unit="s", utc=True)
        return pd.NaT

    df["timestamp"] = df["timestamp_raw"].apply(convert_to_datetime)
    df.dropna(subset=["timestamp"], inplace=True)
    df.sort_values("timestamp", inplace=True)

    # === 4️⃣ Separate Monitors ===
    monitor1 = df[df["id"].str.contains("UpperReservoir.Monitor1", case=False, na=False)][["timestamp", "v"]].rename(columns={"v": "url1"})
    monitor2 = df[df["id"].str.contains("UpperReservoir.Monitor2", case=False, na=False)][["timestamp", "v"]].rename(columns={"v": "url2"})

    # === 5️⃣ Merge closest timestamps ===
    merged = pd.merge_asof(
        monitor1.sort_values("timestamp"),
        monitor2.sort_values("timestamp"),
        on="timestamp",
        direction="nearest",
        tolerance=pd.Timedelta("1min")
    )

    # === 6️⃣ Save clean version ===
    merged.to_csv("structured_output7.csv", index=False)
    print("✅ structured_output7.csv saved — timestamps fixed & human-readable!")

    # === 7️⃣ Plot ===
    plt.figure(figsize=(15, 6))
    plt.plot(merged["timestamp"], merged["url1"], label="Monitor 1", color="cyan", alpha=0.8)
    plt.plot(merged["timestamp"], merged["url2"], label="Monitor 2", color="orange", alpha=0.8)

    OPR_LOW, OPR_HIGH = 445, 460
    plt.axhline(OPR_LOW, color="green", linestyle="--", label=f"Min OPR ({OPR_LOW})")
    plt.axhline(OPR_HIGH, color="red", linestyle="--", label=f"Max OPR ({OPR_HIGH})")

    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45, ha='right')
    plt.title("Upper Reservoir Levels — Monitor 1 & 2")
    plt.xlabel("Timestamp")
    plt.ylabel("Reservoir Level (m)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

    return


if __name__ == "__main__":
    app.run()
