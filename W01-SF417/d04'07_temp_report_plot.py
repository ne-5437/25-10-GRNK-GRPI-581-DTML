import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    PARAMETER = 'Trafo 2 winding temperature max 10M (ºC)'

    def plot_temperature_bar():
        print("Loading CSV files...")

        df_minutal = pd.read_csv("X-Minutal.csv", delimiter=';')
        df_aws = pd.read_csv("Full AWS.csv", delimiter=';')

        # Date conversions
        df_minutal['Date'] = pd.to_datetime(df_minutal['Date'], errors='coerce')
        df_aws['Start Date'] = pd.to_datetime(df_aws['Start Date'], errors='coerce')
        df_aws['End Date'] = pd.to_datetime(df_aws['End Date'], errors='coerce')

        # Clean temp values
        df_minutal[PARAMETER] = pd.to_numeric(df_minutal[PARAMETER], errors='coerce')
        df_minutal[PARAMETER] = df_minutal[PARAMETER].apply(lambda x: x if x > 0 else np.nan)

        df_minutal = df_minutal.dropna(subset=['Date', 'Device', PARAMETER])
        df_aws = df_aws.dropna(subset=['Start Date', 'End Date', 'Device', 'Category'])

        df_minutal = df_minutal.sort_values('Date')
        df_aws = df_aws.sort_values('Start Date')

        print("Merging...")
        merged_df = pd.merge_asof(
            df_minutal, df_aws,
            left_on='Date', right_on='Start Date',
            by='Device', direction='backward'
        )

        merged_df = merged_df[
            (merged_df['Date'] >= merged_df['Start Date']) &
            (merged_df['Date'] <= merged_df['End Date'])
        ]

        filtered_df = merged_df[merged_df['Category'].isin(['State', 'Warning', 'Alarm'])]

        if filtered_df.empty:
            print("No valid data for selected parameter.")
            return

        print("Calculating stats...")
        stats = filtered_df.groupby(['Device', 'Category'])[PARAMETER].max().unstack('Category')

        devices = stats.index.tolist()
        x = np.arange(len(devices))
        width = 0.25

        plt.figure(figsize=(18, 8))

        categories = ['State', 'Warning', 'Alarm']
        for i, cat in enumerate(categories):
            if cat in stats.columns:
                plt.bar(
                    x + i * width,
                    stats[cat],
                    width,
                    label=cat,
                    alpha=0.85
                )

        plt.xticks(x + width, devices, rotation=45, ha='right')
        plt.ylabel('Temperature (°C)')
        plt.xlabel('Devices')
        plt.title(f'Max Temperature Comparison for {PARAMETER}')
        plt.grid(axis='y', linestyle='--', alpha=0.4)
        plt.legend()
        plt.tight_layout()
        plt.show()

        print("Plot complete")

    if __name__ == "__main__":
        plot_temperature_bar()
    return


if __name__ == "__main__":
    app.run()
