import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


app._unparsable_cell(
    r"""
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np

    # === 1️⃣ Load and clean the data ===
    df = pd.read_csv(\"structured_output.csv\")

    # Normalize column names
    df.columns = [c.strip() for c in df.columns]

    # Extract relevant columns
    df = df[[\"TIMESTAMP\", \"UpperReservoir_Monitor2\"]].copy()

    # Convert timestamp to datetime (handle timezone too)
    df[\"TIMESTAMP\"] = pd.to_datetime(df[\"TIMESTAMP\"], errors=\"coerce\", utc=True)

    # Sort chronologically
    df.sort_values(\"TIMESTAMP\", inplace=True)
    df.set_index(\"TIMESTAMP\", inplace=True)

    # === 2️⃣ Define operational range ===
    OPR_LOW, OPR_HIGH = 445, 460  # meters

    # === 3️⃣ Smooth data (rolling average) for visualization ===
    df[\"Smoothed\"] = df[\"UpperReservoir_Monitor2\"].rolling(window=10, min_periods=1).mean()

    # === 4️⃣ Outlier detection using IQR (Interquartile Range) ===
    Q1 = df[\"UpperReservoir_Monitor2\"].quantile(0.25)
    Q3 = df[\"UpperReservoir_Monitor2\"].quantile(0.75)
    IQR = Q3 - Q1
    LOW_IQR = Q1 - 1.5 * IQR
    HIGH_IQR = Q3 + 1.5 * IQR

    # Points beyond IQR range = outliers
    outliers = (df[\"UpperReservoir_Monitor2\"] < LOW_IQR) | (df[\"UpperReservoir_Monitor2\"] > HIGH_IQR)

    # === 5️⃣ Missing values percentage ===
    null_pct = df[\"UpperReservoir_Monitor2\"].isna().mean() * 100

    # === 6️⃣ Visualization ===

    # --- Plot 1: Trend and outliers ---
    plt.figure(figsize=(15, 6))
    plt.plot(df.index, df[\"Smoothed\"], color=\"cyan\", label=\"Reservoir Level (Smoothed)\", alpha=0.8)
    plt.scatter(df.index[outliers], df[\"UpperReservoir_Monitor2\"][outliers], color=\"red\", s=15, label=\"Outliers\")
    plt.axhline(OPR_LOW, color=\"green\", linestyle=\"--\", label=f\"Min OPR ({OPR_LOW} m)\")
    plt.axhline(OPR_HIGH, color=\"orange\", linestyle=\"--\", label=f\"Max OPR ({OPR_HIGH} m)\")
    plt.title(\"Upper Reservoir Level — Trend, Outliers, and Operational Range\")
    plt.xlabel(\"Timestamp\")
    plt.ylabel(\"Reservoir Level (m)\")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

    # --- Plot 2: Boxplot for distribution ---
    plt.figure(figsize=(10, 3))
    plt.boxplot(df[\"UpperReservoir_Monitor2\"].dropna(), vert=False, patch_artist=True,
                boxprops=dict(facecolor='skyblue'))
    plt.title(\"Reservoir Level Distribution (Box Plot)\")
    plt.xlabel(\"Reservoir Level (m)\")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

    # --- Plot 3: Sampling frequency per minute ---
    freq_per_min = df[\"UpperReservoir_Monitor2\"].resample(\"1min\").count()
    plt.figure(figsize=(15, 4))
    plt.plot(freq_per_min.index, freq_per_min.values, color=\"violet\")
    plt.title(\"Sampling Frequency per Minute — Upper Reservoir Level\")
    plt.ylabel(\"Samples/min\")
    plt.xlabel(\"Time\")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

    # === 7️⃣ Summary Statistics ===
    below_low = (df[\"UpperReservoir_Monitor2\"] < OPR_LOW).sum()
    above_high = (df[\"UpperReservoir_Monitor2\"] > OPR_HIGH).sum()

    print(\"\n⚙️ Data Summary:\")
    print(f\"Total samples: {len(df)}\")
    print(f\"Missing Data: {null_pct:.2f}%\")
    print(f\"Outliers detected: {outliers.sum()}\")
    print(f\"Range Violations: {below_low} below {OPR_LOW}, {above_high} above {OPR_HIGH}\")
    print(f\"Data range: {df['UpperReservoir_Monitor2'].min():.2f} – {df['UpperReservoir_Monitor2'].max():.2f}\"
    """,
    name="_"
)


if __name__ == "__main__":
    app.run()
