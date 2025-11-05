import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    return np, pd


@app.cell
def _(pd):
    df = pd.read_csv("X-Minutal5.csv", sep=';')
    df.columns = df.columns.str.strip()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df.info()
    df.head()
    return (df,)


@app.cell
def _(df, pd):
    cols_to_check = [c for c in df.columns if c not in ["Device", "Date"]]

    missing_info = pd.DataFrame({
        "Null Count": df[cols_to_check].isnull().sum(),
        "Null %": (df[cols_to_check].isnull().mean() * 100).round(2)
    })
    missing_info
    return


@app.cell
def _(df):
    df_sorted = df.sort_values("Date").reset_index(drop=True)
    df_sorted["gap_minutes"] = df_sorted["Date"].diff().dt.total_seconds() / 60
    df_sorted[["Date", "gap_minutes"]].head(10)
    return (df_sorted,)


@app.cell
def _(df_sorted, np, pd):
    filled_df = df_sorted.copy()
    value_cols = [c for c in df_sorted.columns if c not in ["Device", "Date", "gap_minutes"]]

    # Convert all numeric-like columns safely to float
    for col in value_cols:
        filled_df[col] = pd.to_numeric(df_sorted[col], errors="coerce")

    for col in value_cols:
        for i in range(len(df_sorted)):
            if pd.isnull(df_sorted.loc[i, col]):
                gap = df_sorted.loc[i, "gap_minutes"]
                if pd.isna(gap):
                    continue

                # --- Decision tree logic ---
                if gap < 1:
                    filled_df.loc[i, col] = df_sorted[col].ffill().iloc[i]
                elif gap < 5:
                    filled_df[col] = df_sorted[col].interpolate(method="linear")
                elif gap < 15:
                    window = df_sorted[col].iloc[max(0, i-2):min(len(df_sorted), i+3)]
                    # Only average numeric values
                    numeric_window = pd.to_numeric(window, errors="coerce")
                    filled_df.loc[i, col] = numeric_window.mean(skipna=True)
                else:
                    filled_df.loc[i, col] = np.nan
                    print(f"⚠️ Data quality issue in '{col}' at {df_sorted.loc[i, 'Date']}")

    final_df = filled_df.drop(columns=["gap_minutes"])
    return (final_df,)


@app.cell
def _(final_df, pd):
    cols_for_check = [c for c in final_df.columns if c not in ["Device", "Date"]]

    verification_table = pd.DataFrame({
        "Null Count": final_df[cols_for_check].isnull().sum(),
        "Null %": (final_df[cols_for_check].isnull().mean() * 100).round(2)
    })
    verification_table
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
