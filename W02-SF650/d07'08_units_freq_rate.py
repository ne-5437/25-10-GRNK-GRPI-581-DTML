import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt

    df = pd.read_csv("structured_output2.csv")

    # ✅ Convert timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
    df.set_index("timestamp", inplace=True)

    # ✅ Select only MW columns (Unit 1–8)
    mw_cols = [col for col in df.columns if "MW" in col]

    # ✅ Count number of samples per minute
    freq_per_min = df[mw_cols].resample("1min").count()

    # ✅ Plot frequency for each unit
    freq_per_min.plot(figsize=(15, 6))
    plt.title("Sampling Frequency per Minute for Units")
    plt.ylabel("Number of Samples (count/min)")
    plt.xlabel("Time")
    plt.show()

    # ✅ Export to Excel for reporting
    freq_per_min.to_excel("frequency_report_per_min.xlsx")
    print("✅ Frequency Report Saved: frequency_report_per_min.xlsx")

    return


if __name__ == "__main__":
    app.run()
