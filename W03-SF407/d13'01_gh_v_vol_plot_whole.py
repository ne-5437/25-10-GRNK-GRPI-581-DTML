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

    for col in ["head_level", "head"]:
        if col in ghv_head_df.columns:
            ghv_head_df["head_level"] = pd.to_numeric(ghv_head_df["head_level"], errors="coerce")
        if col in ghv_volmap_df.columns:
            ghv_volmap_df["head"] = pd.to_numeric(ghv_volmap_df["head"], errors="coerce")
    ghv_volmap_df["Cumm_vol_actual"] = pd.to_numeric(ghv_volmap_df["Cumm_vol_actual"], errors="coerce")

    ghv_upper = ghv_head_df[ghv_head_df["UNIT"] == "UpperReservoir"]
    ghv_lower = ghv_head_df[ghv_head_df["UNIT"] == "LowerReservoir"]

    ghv_merged = pd.merge(
        ghv_upper, ghv_lower,
        on="TIMESTAMP", suffixes=("_upper", "_lower")
    )

    ghv_merged["GH"] = ghv_merged["head_level_upper"] - ghv_merged["head_level_lower"]

    ghv_merged = ghv_merged.dropna(subset=["head_level_upper", "head_level_lower", "GH"])
    ghv_volmap_df = ghv_volmap_df.dropna(subset=["head", "Cumm_vol_actual"])
    return ghv_merged, ghv_volmap_df, np, pd, plt


@app.cell
def _(ghv_merged, ghv_volmap_df):
    print(
        "Upper-head range:", float(ghv_merged["head_level_upper"].min()),
        "to", float(ghv_merged["head_level_upper"].max()),
        "| Map-head range:", float(ghv_volmap_df["head"].min()),
        "to", float(ghv_volmap_df["head"].max())
    )
    return


@app.cell
def _(ghv_merged, ghv_volmap_df, pd):
    ghv_joined = pd.merge_asof(
        ghv_merged.sort_values("head_level_upper"),
        ghv_volmap_df.sort_values("head"),
        left_on="head_level_upper",
        right_on="head",
        direction="nearest"
    ).dropna(subset=["GH", "Cumm_vol_actual"])
    return (ghv_joined,)


@app.cell
def _(ghv_joined, np):
    ghv_x = ghv_joined["GH"].astype(float).to_numpy()
    ghv_y = ghv_joined["Cumm_vol_actual"].astype(float).to_numpy()

    ghv_slope, ghv_intercept = np.polyfit(ghv_x, ghv_y, 1)
    ghv_line = ghv_slope * ghv_x + ghv_intercept
    ghv_r2 = 1 - (np.sum((ghv_y - ghv_line)**2) / np.sum((ghv_y - ghv_y.mean())**2))
    return ghv_intercept, ghv_r2, ghv_slope, ghv_x, ghv_y


@app.cell
def _(ghv_intercept, ghv_r2, ghv_slope, ghv_x, ghv_y, np, plt):
    print(f"Slope: {ghv_slope:.10f}, Intercept: {ghv_intercept:.10f}, R²: {ghv_r2:.5f}")

    plt.figure(figsize=(8,5))
    plt.scatter(ghv_x, ghv_y, label="Actual Data")
    plt.plot(np.sort(ghv_x), ghv_slope*np.sort(ghv_x)+ghv_intercept, linewidth=2,
             label=f"y = {ghv_slope:.10f}x + {ghv_intercept:.10f}")
    plt.xlabel("GH")
    plt.ylabel("Vol_mcm")
    plt.title("GH vs Volume")
    plt.legend()
    plt.grid(True)
    plt.show()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
