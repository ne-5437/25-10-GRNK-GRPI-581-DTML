import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Load data
    df = pd.read_csv("head.csv")
    df.columns = [c.strip().lower() for c in df.columns]
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Filter only LowerReservoir and target date range
    mask = (
        (df["unit"].str.lower() == "lowerreservoir")
        & (df["timestamp"] >= "2025-09-01")
        & (df["timestamp"] < "2025-10-01")
    )
    df_lr = df.loc[mask].copy()

    # Extract date column
    df_lr["date"] = df_lr["timestamp"].dt.date

    # Set up plot
    plt.figure(figsize=(14, 8))
    sns.set_style("darkgrid")

    # Color palette for 30 days
    dates_sorted = sorted(df_lr["date"].unique())
    palette = sns.color_palette("viridis", len(dates_sorted))

    # Plot each day's KDE
    for date, color in zip(dates_sorted, palette):
        subset = df_lr[df_lr["date"] == date]["head_level"].dropna()
        if len(subset) > 10:  # skip days with too few data points
            sns.kdeplot(subset, color=color, label=str(date), alpha=0.7, linewidth=1.2)

    # Aesthetic tweaks
    plt.title("Daily KDE of Lower Reservoir Head Level (Sep 1 - Oct 1, 2025)", fontsize=15)
    plt.xlabel("Head Level")
    plt.ylabel("Density")
    plt.legend(title="Date", bbox_to_anchor=(1.05, 1), loc='upper left', ncol=1, fontsize=8)
    plt.tight_layout()
    plt.show()

    return


if __name__ == "__main__":
    app.run()
