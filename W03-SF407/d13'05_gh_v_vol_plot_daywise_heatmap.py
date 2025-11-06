import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.stats import gaussian_kde

    ghv_head_df = pd.read_csv("head.csv")
    ghv_volmap_df = pd.read_csv("head_vs_volume.csv")

    ghv_head_df["head_level"] = pd.to_numeric(ghv_head_df["head_level"], errors="coerce")
    ghv_volmap_df["head"] = pd.to_numeric(ghv_volmap_df["head"], errors="coerce")
    ghv_volmap_df["Cumm_vol_actual"] = pd.to_numeric(ghv_volmap_df["Cumm_vol_actual"], errors="coerce")
    ghv_head_df["TIMESTAMP"] = pd.to_datetime(ghv_head_df["TIMESTAMP"], errors="coerce")

    upper = ghv_head_df[ghv_head_df["UNIT"] == "UpperReservoir"].copy()
    lower = ghv_head_df[ghv_head_df["UNIT"] == "LowerReservoir"].copy()
    upper = upper.sort_values("TIMESTAMP").drop_duplicates(subset="TIMESTAMP", keep="last").set_index("TIMESTAMP")
    lower = lower.sort_values("TIMESTAMP").drop_duplicates(subset="TIMESTAMP", keep="last").set_index("TIMESTAMP")
    upper = upper[~upper.index.duplicated(keep="last")].sort_index()
    lower = lower[~lower.index.duplicated(keep="last")].sort_index()

    upper = upper.resample("1T").ffill()
    lower = lower.resample("1T").ffill()

    merged = pd.DataFrame(index=upper.index)
    merged["head_level_upper"] = upper["head_level"]
    merged["head_level_lower"] = lower["head_level"]
    merged["GH"] = merged["head_level_upper"] - merged["head_level_lower"]
    merged = merged.dropna(subset=["GH"])

    merged["Vol_interp"] = np.interp(
        merged["head_level_upper"],
        ghv_volmap_df["head"],
        ghv_volmap_df["Cumm_vol_actual"]
    )

    start, end = "2025-09-01", "2025-09-07"
    week_df = merged.loc[start:end].copy()
    week_df["DAY"] = week_df.index.date
    days = sorted(week_df["DAY"].unique())
    return days, gaussian_kde, np, plt, week_df


@app.cell
def _(days, gaussian_kde, np, plt, week_df):
    n_days = len(days)
    fig, axs = plt.subplots(2, 4, figsize=(16, 7))
    axs = axs.flatten()

    for i, day in enumerate(days):
        df_day = week_df[week_df["DAY"] == day]
        if df_day.empty:
            axs[i].axis("off")
            continue

        x = df_day["GH"].to_numpy()
        y = df_day["Vol_interp"].to_numpy()

        xy = np.vstack([x, y])
        kde = gaussian_kde(xy)
        xi, yi = np.mgrid[x.min():x.max():200j, y.min():y.max():200j]
        zi = kde(np.vstack([xi.flatten(), yi.flatten()]))

        cf = axs[i].contourf(xi, yi, zi.reshape(xi.shape),
                             levels=50, cmap="viridis")
        axs[i].scatter(np.mean(x), np.mean(y), color="white", s=20)
        axs[i].set_title(f"{day}")
        axs[i].set_xlabel("GH")
        axs[i].set_ylabel("Volume (mcm)")
        axs[i].grid(True)

    for j in range(i + 1, len(axs)):
        axs[j].axis("off")

    plt.suptitle("GH vs Volume — Day-wise 2D KDE Heatmaps (Week 1: 2025-09-01 to 09-07)",
                 fontsize=14, y=1.02)
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
