import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd

    # Load your merged output CSV
    df = pd.read_csv("clean_windmill_data.csv")

    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed', utc=False)


    # Create a column name from unit_name
    df['unit_column'] = df['unit_name'].str.replace(" ", "") + "_MW"

    # Pivot the table
    df_pivot = df.pivot_table(
        index='timestamp',
        columns='unit_column',
        values='power_MW',
        aggfunc='first'
    )

    # Sort by timestamp
    df_pivot = df_pivot.sort_values(by='timestamp')

    # Save structured CSV
    df_pivot.to_csv("structured_output2.csv", index=True)

    print("✅ structured_output2.csv saved!")
    df_pivot.head()

    return


if __name__ == "__main__":
    app.run()
