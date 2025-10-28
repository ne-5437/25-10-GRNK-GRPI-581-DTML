import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    PARAMETER = 'Trafo 2 winding temperature max 10M (ºC)'

    def plot_overlapping_temperature_bar():
        print("Loading CSV files...")

        df_minutal = pd.read_csv("X-Minutal.csv", delimiter=';')
        df_aws = pd.read_csv("Full AWS.csv", delimiter=';')

        # Convert date columns
        df_minutal['Date'] = pd.to_datetime(df_minutal['Date'], errors='coerce')
        df_aws['Start Date'] = pd.to_datetime(df_aws['Start Date'], errors='coerce')
        df_aws['End Date'] = pd.to_datetime(df_aws['End Date'], errors='coerce')

        # Clean temperature values
        df_minutal[PARAMETER] = pd.to_numeric(df_minutal[PARAMETER], errors='coerce')
        df_minutal[PARAMETER] = df_minutal[PARAMETER].apply(lambda x: x if x > 0 else np.nan)

        # Drop invalid rows
        df_minutal = df_minutal.dropna(subset=['Date', 'Device', PARAMETER])
        df_aws = df_aws.dropna(subset=['Start Date', 'End Date', 'Device', 'Category'])

        # Sort for merge_asof
        df_minutal = df_minutal.sort_values('Date')
        df_aws = df_aws.sort_values('Start Date')

        print("Merging data...")
        merged_df = pd.merge_asof(
            df_minutal, df_aws,
            left_on='Date', right_on='Start Date',
            by='Device', direction='backward'
        )

        # Keep only rows within event interval
        merged_df = merged_df[
            (merged_df['Date'] >= merged_df['Start Date']) &
            (merged_df['Date'] <= merged_df['End Date'])
        ]

        # Filter categories
        categories = ['State', 'Warning', 'Alarm']
        filtered_df = merged_df[merged_df['Category'].isin(categories)]

        if filtered_df.empty:
            print("No valid data for selected parameter.")
            return

        print("Calculating max temperature per device and category...")
        stats = filtered_df.groupby(['Device', 'Category'])[PARAMETER].max().unstack('Category').fillna(0)

        devices = stats.index.tolist()
        x = np.arange(len(devices))
        width = 0.6

        # Black background figure
        fig, ax = plt.subplots(figsize=(18, 8))
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')
        plt.style.use('dark_background')

        # Updated popping colors
        colors = {'State': '#00FFFF', 'Warning': '#FFA500', 'Alarm': '#FF2A2A'}
        alpha_val = 0.6  # semi-transparent

        # Plot each category on same x-position to allow overlap
        for cat in categories:
            if cat in stats.columns:
                values = stats[cat].values
                ax.bar(
                    x,
                    values,
                    width,
                    label=cat,
                    color=colors[cat],
                    alpha=alpha_val,
                    edgecolor='black'
                )

        # Axes and labels
        ax.set_xticks(x)
        ax.set_xticklabels(devices, rotation=45, ha='right', color='white')
        ax.set_ylabel('Temperature (°C)', color='black', fontsize=12)
        ax.set_xlabel('Devices', color='black', fontsize=12)
        ax.set_title(f'Temperature Ranges per Device (Overlapping) — {PARAMETER}', color='blue', fontsize=16, fontweight='bold')
        ax.grid(True, linestyle=':', alpha=0.3)
        ax.spines['bottom'].set_color('black')
        ax.spines['left'].set_color('black')
        ax.tick_params(colors='black')

        legend = ax.legend(facecolor='white', edgecolor='black')
        for text in legend.get_texts():
            text.set_color('black')

        plt.tight_layout()
        plt.show()
        print("Overlapping stacked plot complete.")

    if __name__ == "__main__":
        plot_overlapping_temperature_bar()
    return


if __name__ == "__main__":
    app.run()
