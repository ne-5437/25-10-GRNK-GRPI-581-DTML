import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np

    # Load data
    df = pd.read_csv("merged_output.csv")

    # Convert pt (epoch ms → datetime)
    df["timestamps"] = pd.to_datetime(df["pt"], unit="ms")

    # Map IDs to meaningful names
    mapping = {
        "AP01.PSP.GSUT-1.Gen_MWH_IMPORT": "import_energy",
        "AP01.PSP.ST1.HV_MW": "switch_1",
        "AP01.PSP.GSUT-1.Gen_MWH_EXPORT": "export_energy"
    }

    # Filter and map
    df = df[df["id"].isin(mapping.keys())].copy()
    df["parameter"] = df["id"].map(mapping)

    # Pivot to wide format
    pivot_df = df.pivot_table(
        index="timestamps",
        columns="parameter",
        values="v",
        aggfunc="mean"
    ).reset_index()

    # Restrict to available date range (for safety)
    pivot_df = pivot_df.sort_values("timestamps")
    start, end = pivot_df["timestamps"].min(), pivot_df["timestamps"].max()
    print(f"Available timestamps: {start} → {end}")

    # ---------- 1️⃣ Null Count per Parameter ----------
    plt.figure(figsize=(6,4))
    pivot_df[["import_energy","export_energy","switch_1"]].isna().sum().plot(
        kind="bar", color="tomato"
    )
    plt.title("Null Count per Parameter (Unit-1)")
    plt.ylabel("Count")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

    # ---------- 2️⃣ Correlation ----------
    plt.figure(figsize=(6,5))
    sns.heatmap(
        pivot_df[["import_energy","export_energy","switch_1"]].corr(),
        annot=True, cmap="coolwarm", center=0
    )
    plt.title("Correlation between Import, Export, and Switch (Unit-1)")
    plt.show()

    # ---------- 3️⃣ Time Series ----------
    plt.figure(figsize=(12,4))
    plt.plot(pivot_df["timestamps"], pivot_df["import_energy"], label="Import Energy", color="green", alpha=0.7)
    plt.plot(pivot_df["timestamps"], pivot_df["export_energy"], label="Export Energy", color="red", alpha=0.7)
    plt.plot(pivot_df["timestamps"], pivot_df["switch_1"], label="Switch 1 (HV MW)", color="blue", alpha=0.5)
    plt.legend()
    plt.title("Time Series: Import vs Export vs Switch")
    plt.xlabel("Timestamp")
    plt.ylabel("Value")
    plt.tight_layout()
    plt.show()

    # ---------- 4️⃣ KDE Plot for Import (Daily Overlays) ----------
    pivot_df["date"] = pivot_df["timestamps"].dt.date
    plt.figure(figsize=(10,5))
    for d, subset in pivot_df.groupby("date"):
        if subset["import_energy"].dropna().empty:
            continue
        sns.kdeplot(subset["import_energy"], label=str(d), alpha=0.3)
    plt.title("Daily KDE Distribution - Import Energy (Sept 2025)")
    plt.xlabel("Import Energy Value")
    plt.ylabel("Density")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='x-small', ncol=2)
    plt.tight_layout()
    plt.show()

    # ---------- 5️⃣ KDE Plot for Export (Daily Overlays) ----------
    plt.figure(figsize=(10,5))
    for d, subset in pivot_df.groupby("date"):
        if subset["export_energy"].dropna().empty:
            continue
        sns.kdeplot(subset["export_energy"], label=str(d), alpha=0.3)
    plt.title("Daily KDE Distribution - Export Energy (Sept 2025)")
    plt.xlabel("Export Energy Value")
    plt.ylabel("Density")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='x-small', ncol=2)
    plt.tight_layout()
    plt.show()


    return


if __name__ == "__main__":
    app.run()
