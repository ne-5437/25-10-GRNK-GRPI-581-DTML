import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt

    # ✅ Load CSV
    df = pd.read_csv("structured_output2.csv")

    # ✅ Convert timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
    df.set_index("timestamp", inplace=True)

    # ✅ Select only MW columns (Unit 1–8)
    mw_cols = [col for col in df.columns if "MW" in col]

    # ✅ Count number of samples per minute
    freq_per_min = df[mw_cols].resample("1min").count()

    # ✅ Plot each MW unit separately
    for col in mw_cols:
        plt.figure(figsize=(15, 5))
        plt.plot(freq_per_min.index, freq_per_min[col], label=col)
        plt.title(f"Sampling Frequency per Minute - {col}")
        plt.ylabel("Samples per Minute")
        plt.xlabel("Time")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.show()
    return


if __name__ == "__main__":
    app.run()
