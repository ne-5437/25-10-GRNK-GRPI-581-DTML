import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt

    # === 1️⃣ Load merged data ===
    df = pd.read_csv("merged_output.csv")

    # --- Normalize column names ---
    df.columns = [c.strip().lower() for c in df.columns]

    # --- Create a unified timestamp column ---
    # Prefer 'pt' if it exists, else 'dt'
    df["timestamp"] = pd.to_datetime(df["pt"].fillna(df["dt"]), errors="coerce", utc=True)
    df.dropna(subset=["timestamp"], inplace=True)
    df.sort_values("timestamp", inplace=True)

    # === 2️⃣ Separate Monitor1 and Monitor2 ===
    monitor1 = df[df["id"].str.contains("UpperReservoir.Monitor1", case=False, na=False)][["timestamp", "v"]].rename(columns={"v": "url1"})
    monitor2 = df[df["id"].str.contains("UpperReservoir.Monitor2", case=False, na=False)][["timestamp", "v"]].rename(columns={"v": "url2"})

    # === 3️⃣ Merge both based on timestamp ===
    merged = pd.merge_asof(
        monitor1.sort_values("timestamp"),
        monitor2.sort_values("timestamp"),
        on="timestamp",
        direction="nearest",  # match closest timestamps
        tolerance=pd.Timedelta("1min")  # optional, skip if too different
    )

    # === 4️⃣ Save structured output ===
    merged.to_csv("structured_output4.csv", index=False)
    print("✅ structured_output4.csv saved successfully!")

    # === 5️⃣ Visualization (like before) ===

    OPR_LOW, OPR_HIGH = 445, 460

    plt.figure(figsize=(15, 6))
    plt.plot(merged["timestamp"], merged["url1"], label="Upper Reservoir Monitor 1", color="cyan", alpha=0.7)
    plt.plot(merged["timestamp"], merged["url2"], label="Upper Reservoir Monitor 2", color="orange", alpha=0.7)
    plt.axhline(OPR_LOW, color="green", linestyle="--", label=f"Min OPR ({OPR_LOW} m)")
    plt.axhline(OPR_HIGH, color="red", linestyle="--", label=f"Max OPR ({OPR_HIGH} m)")
    plt.title("Upper Reservoir Level — Monitor 1 & Monitor 2")
    plt.xlabel("Timestamp")
    plt.ylabel("Reservoir Level (m)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

    # === 6️⃣ Distribution comparison ===
    plt.figure(figsize=(10, 3))
    plt.boxplot([merged["url1"].dropna(), merged["url2"].dropna()],
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
