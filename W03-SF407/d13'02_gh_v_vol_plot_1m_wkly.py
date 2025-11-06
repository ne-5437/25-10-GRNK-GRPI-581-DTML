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
    return ghv_volmap_df, lower, np, pd, plt, upper


@app.cell
def _(ghv_volmap_df, lower, np, pd, upper):
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

    weeks = [
        ("Week 1", "2025-09-01", "2025-09-07"),
        ("Week 2", "2025-09-08", "2025-09-14"),
        ("Week 3", "2025-09-15", "2025-09-21"),
        ("Week 4", "2025-09-22", "2025-09-30")
    ]
    return merged, weeks


@app.cell
def _(merged, np, plt, weeks):
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    axs = axs.flatten()

    for i, (label, start, end) in enumerate(weeks):
        week_df = merged.loc[start:end]
        if week_df.empty:
            axs[i].set_title(f"{label} — No Data")
            axs[i].axis("off")
            continue

        x = week_df["GH"].to_numpy()
        y = week_df["Vol_interp"].to_numpy()

        slope, intercept = np.polyfit(x, y, 1)
        line = slope * x + intercept
        r2 = 1 - np.sum((y - line)**2) / np.sum((y - y.mean())**2)

        axs[i].scatter(x, y, s=2, alpha=0.4, label=f"{label} Data ({len(x)} mins)")
        axs[i].plot(np.sort(x), slope*np.sort(x)+intercept, color="orange",
                    linewidth=2, label=f"y={slope:.4f}x+{intercept:.2f}\nR²={r2:.4f}")
        axs[i].set_xlabel("GH")
        axs[i].set_ylabel("Volume (mcm)")
        axs[i].set_title(f"{label} — {start} to {end}")
        axs[i].legend()
        axs[i].grid(True)

    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 6))
    colors = ["cyan", "yellow", "violet", "red"]
    for (label, start, end), c in zip(weeks, colors):
        df = merged.loc[start:end]
        if df.empty:
            continue
        x, y = df["GH"].to_numpy(), df["Vol_interp"].to_numpy()
        slope, intercept = np.polyfit(x, y, 1)
        plt.scatter(x, y, s=2, alpha=0.25, label=f"{label} Data", color=c)
        plt.plot(np.sort(x), slope*np.sort(x)+intercept, linewidth=2, color=c,
                 label=f"{label} Fit (R²={1 - np.sum((y - (slope*x+intercept))**2)/np.sum((y - y.mean())**2):.3f})")

    plt.xlabel("GH")
    plt.ylabel("Volume (mcm)")
    plt.title("GH vs Volume (1-minute, 4-Week Overlay — Sept 2025)")
    plt.legend()
    plt.grid(True)
    plt.show()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
