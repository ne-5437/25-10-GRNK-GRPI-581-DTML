import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

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

    week_label, start, end = ("Week 1", "2025-09-01", "2025-09-07")
    week_df = merged.loc[start:end].copy()

    week_df["DAY"] = week_df.index.date
    days = sorted(week_df["DAY"].unique())

    n_days = len(days)
    n_cols = 3
    n_rows = int(np.ceil(n_days / n_cols))

    fig, axs = plt.subplots(n_rows, n_cols, figsize=(15, 8))
    axs = axs.flatten()

    for i, day in enumerate(days):
        df_day = week_df[week_df["DAY"] == day]
        if df_day.empty:
            continue

        x = df_day["GH"].to_numpy()
        y = df_day["Vol_interp"].to_numpy()

        slope, intercept = np.polyfit(x, y, 1)
        line = slope * x + intercept
        r2 = 1 - np.sum((y - line)**2) / np.sum((y - y.mean())**2)

        axs[i].scatter(x, y, s=3, alpha=0.4, label="Data")
        axs[i].plot(np.sort(x), slope*np.sort(x)+intercept, color="orange", linewidth=2,
                    label=f"Slope={slope:.4f}\nR²={r2:.3f}")
        axs[i].set_title(f"{day}")
        axs[i].set_xlabel("GH")
        axs[i].set_ylabel("Volume (mcm)")
        axs[i].legend(fontsize=8)
        axs[i].grid(True)

    for j in range(i+1, len(axs)):
        axs[j].axis("off")

    plt.suptitle(f"GH vs Volume — {week_label} ({start} to {end})\nDay-wise Patterns", fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.show()

    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
