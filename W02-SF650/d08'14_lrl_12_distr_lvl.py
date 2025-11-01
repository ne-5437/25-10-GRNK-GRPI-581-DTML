import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    # === 1️⃣ Load merged data ===
    df = pd.read_csv("merged_output.csv")

    # Normalize columns
    df.columns = [c.strip().lower() for c in df.columns]

    # === 2️⃣ Combine pt and dt into unified timestamp ===
    # Prioritize pt if it exists; fallback to dt
    df["timestamp_raw"] = df["pt"].fillna(df["dt"])

    # Convert to datetime explicitly with timezone awareness
    df["timestamp"] = pd.to_datetime(df["timestamp_raw"], utc=True, errors="coerce")

    # Drop invalid or missing timestamps
    df.dropna(subset=["timestamp"], inplace=True)

    # Sort chronologically
    df.sort_values("timestamp", inplace=True)

    # === 3️⃣ Separate by Monitor ===
    monitor1 = df[df["id"].str.contains("LowerReservoir.Monitor1", case=False, na=False)][["timestamp", "v"]].rename(columns={"v": "lrl1"})
    monitor2 = df[df["id"].str.contains("LowerReservoir.Monitor2", case=False, na=False)][["timestamp", "v"]].rename(columns={"v": "lrl2"})

    # === 4️⃣ Merge based on timestamp proximity ===
    merged = pd.merge_asof(
        monitor1.sort_values("timestamp"),
        monitor2.sort_values("timestamp"),
        on="timestamp",
        direction="nearest",
        tolerance=pd.Timedelta("1min")
    )

    # Save structured version
    merged.to_csv("structured_output5.csv", index=False)
    print("✅ structured_output5.csv saved successfully with clean timestamps!")

    # === 5️⃣ Plot configuration ===
    plt.figure(figsize=(15, 6))

    # Plot URL1 and URL2
    plt.plot(merged["timestamp"], merged["lrl1"], label="Monitor 1", color="cyan", alpha=0.8)
    plt.plot(merged["timestamp"], merged["lrl2"], label="Monitor 2", color="orange", alpha=0.8)

    # Operational thresholds
    OPR_LOW, OPR_HIGH = 320.5, 335.5
    plt.axhline(OPR_LOW, color="green", linestyle="--", label=f"Min OPR ({OPR_LOW})")
    plt.axhline(OPR_HIGH, color="red", linestyle="--", label=f"Max OPR ({OPR_HIGH})")

    # === 🧭 Beautify X-axis (datetime formatting) ===
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))  # Show readable format
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())  # Auto spacing
    plt.xticks(rotation=45, ha='right')

    plt.title("Lower Reservoir Level — Monitor 1 & Monitor 2")
    plt.xlabel("Timestamp")
    plt.ylabel("Reservoir Level (m)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

    # === 6️⃣ Boxplot comparison ===
    plt.figure(figsize=(10, 3))
    plt.boxplot([merged["lrl1"].dropna(), merged["lrl2"].dropna()],
                 vert=False, patch_artist=True,
                 labels=["Monitor 1", "Monitor 2"],
                 boxprops=dict(facecolor='skyblue'))
    plt.title("Reservoir Level Distribution — Monitor 1 vs Monitor 2")
    plt.xlabel("Reservoir Level (m)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()
    return


if __name__ == "__main__":
    app.run()
