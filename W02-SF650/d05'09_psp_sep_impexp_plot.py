import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    # Load CSV
    df = pd.read_csv("turbine_minute_filtered.csv")
    df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"], utc=True)
    df = df.sort_values("TIMESTAMP").reset_index(drop=True)

    # Rename
    df = df.rename(columns={
        "AP01.PSP.GSUT-1.Gen_MWH_IMPORT": "IMPORT",
        "AP01.PSP.GSUT-1.Gen_MWH_EXPORT": "EXPORT"
    })

    # 1. Plot raw Import vs Export values
    plt.figure(figsize=(16,6))
    plt.plot(df["TIMESTAMP"], df["IMPORT"], label="IMPORT (MWh)", linewidth=1)
    plt.plot(df["TIMESTAMP"], df["EXPORT"], label="EXPORT (MWh)", linewidth=1)
    plt.title("Import and Export Energy Trend Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("Cumulative Energy (MWh)")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # 2. Derivatives for behavior analysis
    df["dIMPORT"] = df["IMPORT"].diff()
    df["dEXPORT"] = df["EXPORT"].diff()

    # Negative deltas are invalid due to resets
    df.loc[df["dIMPORT"] < 0, "dIMPORT"] = np.nan
    df.loc[df["dEXPORT"] < 0, "dEXPORT"] = np.nan

    # 3. More meaningful NetEnergy
    df["NetEnergy"] = df["dEXPORT"].fillna(0) - df["dIMPORT"].fillna(0)

    # 4. Operational mode reclassification
    conditions = [
        (df["dEXPORT"] > 0) & (df["dIMPORT"].isna() | (df["dIMPORT"] == 0)),
        (df["dIMPORT"] > 0) & (df["dEXPORT"].isna() | (df["dEXPORT"] == 0)),
        (df["dIMPORT"].fillna(0) == 0) & (df["dEXPORT"].fillna(0) == 0)
    ]
    choices = ["GENERATION", "PUMPING", "IDLE"]

    df["Mode"] = np.select(conditions, choices, default="TRANSITION")

    # 5. Mode timeline for understanding states
    color_map = {
        "GENERATION": "blue",
        "PUMPING": "green",
        "IDLE": "gray",
        "TRANSITION": "red"
    }
    df["Color"] = df["Mode"].map(color_map)

    plt.figure(figsize=(16,3))
    plt.scatter(df["TIMESTAMP"], [1]*len(df), c=df["Color"], s=5)
    plt.title("Operational Mode Timeline")
    plt.yticks([])
    plt.tight_layout()
    plt.show()

    # Print updated stats
    print(df["Mode"].value_counts())

    return


if __name__ == "__main__":
    app.run()
