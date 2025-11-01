import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import re

    # Load
    df = pd.read_csv("combined_output.csv")

    # Filter rows where id contains UNITx discharge flow
    pattern = r"AP01\.PSP\.(UNIT\d)\.UFMS_DISCHARGE_FLOW"
    filtered = df[df["id"].str.contains(pattern, regex=True, na=False)]

    # Extract unit name (UNIT1 / UNIT2 / UNIT3 / UNIT4)
    filtered["unit"] = filtered["id"].str.extract(pattern)

    # Convert UNIX milliseconds to proper datetime
    filtered["timestamp"] = pd.to_datetime(
        filtered["dt"].fillna(filtered["pt"]).astype(float),
        unit="ms",
        errors="coerce"
    )

    # Select required columns & rename v -> discharge_value
    clean_df = filtered[["timestamp", "unit", "v"]].rename(columns={"v": "discharge_value"})

    # Fill empty / NaN discharge values with 0
    clean_df["discharge_value"] = (
        pd.to_numeric(clean_df["discharge_value"], errors="coerce")
        .fillna(0)
    )

    # Fill missing discharge values with 0
    clean_df["discharge_value"] = pd.to_numeric(clean_df["discharge_value"], errors="coerce").fillna(0)

    # Sort by timestamp & unit (optional)
    clean_df = clean_df.sort_values(["unit", "timestamp"])

    # Save output
    clean_df.to_csv("clean_discharge_output.csv", index=False)

    clean_df.head()

    return


if __name__ == "__main__":
    app.run()
