import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    # === 1️⃣ Load and convert timestamps ===
    df = pd.read_csv("merged_output.csv")
    df.columns = [c.strip().lower() for c in df.columns]

    # Combine pt/dt timestamps
    df["timestamp_raw"] = df.get("pt", pd.Series(dtype=object)).combine_first(df.get("dt", pd.Series(dtype=object)))

    def smart_parse(x):
        """Robust timestamp converter (handles strings + epoch s/ms)"""
        if isinstance(x, str):
            t = pd.to_datetime(x, errors="coerce", utc=True)
            if not pd.isna(t):
                return t
        try:
            val = float(x)
        except Exception:
            return pd.NaT
        if val > 1e11:       # milliseconds
            return pd.to_datetime(val, unit="ms", utc=True)
        elif val > 1e9:      # seconds
            return pd.to_datetime(val, unit="s", utc=True)
        else:
            return pd.to_datetime(val, unit="s", utc=True)

    df["timestamp"] = df["timestamp_raw"].apply(smart_parse)
    df = df.dropna(subset=["timestamp"]).sort_values("timestamp")

    # === 2️⃣ Select Monitor 2 ===
    m2 = df[df["id"].str.contains("LowerReservoir.Monitor1", case=False, na=False)].copy()
    m2["v"] = pd.to_numeric(m2["v"], errors="coerce")
    m2 = m2.dropna(subset=["v"])
    m2.set_index("timestamp", inplace=True)
    m2.sort_index(inplace=True)

    if m2.empty:
        print("⚠️ No Monitor2 data found.")
    else:
        # === 3️⃣ Define operational range ===
        OPR_LOW, OPR_HIGH = 320.5, 335.5

        # Mark points outside operational range
        m2["out_of_range"] = (m2["v"] < OPR_LOW) | (m2["v"] > OPR_HIGH)

        # === 4️⃣ Daily frequency plot ===
        daily_counts = m2["out_of_range"].resample("D").sum()

        plt.figure(figsize=(12,5))
        plt.plot(daily_counts.index, daily_counts.values, "-o", color="royalblue")
        plt.title("Daily Out-of-Range Frequency — Monitor 1")
        plt.xlabel("Date")
        plt.ylabel("Count of Values Outside Operational Range")
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.xticks(rotation=45)
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.show()

        # === 5️⃣ Hourly breakdown for worst day ===
        if daily_counts.sum() > 0:
            max_day = daily_counts.idxmax().normalize()
            day_df = m2.loc[str(max_day.date())]
            hourly_counts = day_df["out_of_range"].resample("H").sum()

            plt.figure(figsize=(12,5))
            plt.plot(hourly_counts.index, hourly_counts.values, "-o", color="crimson")
            plt.title(f"Hourly Out-of-Range Frequency — {max_day.date()} — Monitor 1")
            plt.xlabel("Hour (UTC)")
            plt.ylabel("Out-of-Range Count")
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
            plt.xticks(rotation=45)
            plt.grid(alpha=0.3)
            plt.tight_layout()
            plt.show()
        else:
            print("✅ No values outside operational range — skipping hourly plot.")

        print(f"📊 Total samples: {len(m2)} | Out-of-range: {m2['out_of_range'].sum()} samples")
    return


if __name__ == "__main__":
    app.run()
