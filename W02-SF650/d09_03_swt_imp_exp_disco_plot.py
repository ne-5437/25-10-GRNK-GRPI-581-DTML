import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np

    # --- Load + preprocess ---
    df = pd.read_csv("merged_output.csv")
    df["timestamps"] = pd.to_datetime(df["pt"], unit="ms")

    mapping = {
        "AP01.PSP.GSUT-1.Gen_MWH_IMPORT": "import_energy",
        "AP01.PSP.ST1.HV_MW": "switch_1",
        "AP01.PSP.GSUT-1.Gen_MWH_EXPORT": "export_energy"
    }

    df = df[df["id"].isin(mapping.keys())].copy()
    df["parameter"] = df["id"].map(mapping)

    pivot_df = df.pivot_table(
        index="timestamps",
        columns="parameter",
        values="v",
        aggfunc="mean"
    ).reset_index().sort_values("timestamps")

    # --- Create switch state (mode) ---
    pivot_df["mode"] = np.where(pivot_df["switch_1"] >= 0, "EXPORT", "IMPORT")

    # --- Detect mode change points ---
    pivot_df["mode_change"] = pivot_df["mode"].ne(pivot_df["mode"].shift())

    # --- Plot ---
    fig, ax1 = plt.subplots(figsize=(12,5))

    # Area background by mode
    for i in range(1, len(pivot_df)):
        if pivot_df["mode"].iloc[i] == "IMPORT":
            ax1.axvspan(pivot_df["timestamps"].iloc[i-1], pivot_df["timestamps"].iloc[i],
                        color="royalblue", alpha=0.1)
        else:
            ax1.axvspan(pivot_df["timestamps"].iloc[i-1], pivot_df["timestamps"].iloc[i],
                        color="limegreen", alpha=0.1)

    # Import / Export lines
    ax1.plot(pivot_df["timestamps"], pivot_df["import_energy"], color="green", label="Import Energy", linewidth=1.2)
    ax1.plot(pivot_df["timestamps"], pivot_df["export_energy"], color="red", label="Export Energy", linewidth=1.2)

    # Mark switch transitions
    switch_points = pivot_df.loc[pivot_df["mode_change"], "timestamps"]
    for t in switch_points:
        ax1.axvline(t, color="yellow", linestyle="--", alpha=0.6)

    ax1.set_title("Switch-driven Mode Transitions: Import ↔ Export")
    ax1.set_xlabel("Timestamp")
    ax1.set_ylabel("Energy Value")
    ax1.legend(loc="upper left")
    plt.tight_layout()
    plt.show()

    return


if __name__ == "__main__":
    app.run()
