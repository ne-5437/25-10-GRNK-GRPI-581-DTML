import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from datetime import timedelta

    # === 1️⃣ Load and preprocess ===
    df = pd.read_csv("head.csv")
    df.columns = [c.strip().lower() for c in df.columns]

    # Parse timestamp — make sure all are timezone-aware (UTC)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
    df = df.dropna(subset=["timestamp"])

    # === 2️⃣ Filter for Lower Reservoir and date range ===
    lower_df = df[df["unit"].str.contains("Upper", case=False, na=False)].copy()
    lower_df["head_level"] = pd.to_numeric(lower_df["head_level"], errors="coerce")
    lower_df = lower_df.dropna(subset=["head_level"])

    # Make date range UTC-aware too
    start_date = pd.Timestamp("2025-09-01", tz="UTC")
    end_date = pd.Timestamp("2025-10-01", tz="UTC")

    # === 3️⃣ Loop through each day and plot KDE ===
    current_date = start_date
    while current_date < end_date:
        next_date = current_date + timedelta(days=1)
        day_df = lower_df[
            (lower_df["timestamp"] >= current_date) & (lower_df["timestamp"] < next_date)
        ]

        if not day_df.empty:
            plt.figure(figsize=(8, 5))
            sns.kdeplot(day_df["head_level"], fill=True, color="royalblue", alpha=0.5)
            plt.title(f"KDE of Head Level — Upper Reservoir ({current_date.date()})")
            plt.xlabel("Head Level")
            plt.ylabel("Density")
            plt.grid(alpha=0.3)
            plt.tight_layout()
            plt.show()
        else:
            print(f"⚠️ No data for {current_date.date()}")

        current_date = next_date

    return


if __name__ == "__main__":
    app.run()
