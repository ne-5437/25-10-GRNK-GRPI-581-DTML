import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    PARAMETER = 'Bearing D.E. Temperature max 10M (ºC)'
    CATEGORY_517 = '517 Generator DE bearing high temperature warning'
    COLOR_517 = '#3FEF3F' 

    def plot_517_only():
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

        # Filter only 517 category
        df_aws = df_aws[df_aws['Event'] == CATEGORY_517]
        if df_aws.empty:
            print("No events found for the 517 category.")
            return

        # Sort for merge_asof
        df_minutal = df_minutal.sort_values('Date')
        df_aws = df_aws.sort_values('Start Date')

        # Merge minutal with AWS
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

        if merged_df.empty:
            print("No overlapping minutal data found for the 517 events.")
            return

        # Compute min and max per device
        stats = merged_df.groupby(['Device'])[PARAMETER].agg(['min','max']).reset_index()
        devices = stats['Device'].unique()
        x = np.arange(len(devices))
        width = 0.6  # full-width bars

        # Plot
        fig, ax = plt.subplots(figsize=(22, 10))
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')
        plt.style.use('dark_background')

        alpha_val = 0.7

        bottoms = stats['min'].tolist()
        heights = (stats['max'] - stats['min']).tolist()

        ax.bar(
            x,
            heights,
            width,
            bottom=bottoms,
            color=COLOR_517,
            alpha=alpha_val,
            edgecolor='black',
            label=CATEGORY_517
        )

        # Axes and labels
        ax.set_xticks(x)
        ax.set_xticklabels(devices, rotation=45, ha='right', color='black')
        ax.set_ylabel('Temperature (°C)', color='black', fontsize=12)
        ax.set_xlabel('Devices', color='black', fontsize=12)
        ax.set_title(f'Floating Min-Max Temperature Bars — {CATEGORY_517}', color='blue', fontsize=16, fontweight='bold')

        ax.grid(True, linestyle=':', alpha=0.3)
        ax.spines['bottom'].set_color('black')
        ax.spines['left'].set_color('black')
        ax.tick_params(colors='black')

        # Set y-axis from slightly below min to slightly above max
        y_min = max(0, stats['min'].min() - 2)
        y_max = stats['max'].max() + 2
        ax.set_ylim(y_min, y_max)

        legend = ax.legend(facecolor='white', edgecolor='black')
        for text in legend.get_texts():
            text.set_color('black')

        plt.tight_layout()
        plt.show()
        print("517 floating min-max plot complete.")

    if __name__ == "__main__":
        plot_517_only()
    return mo, pd


@app.cell
def _(mo, pd):
    df_aws = pd.read_csv("Full AWS.csv", delimiter=';')
    mo.ui.table(df_aws)
    return (df_aws,)


@app.cell
def _(df_aws):
    df = df_aws.fillna(0)
    df_n = df[df['Event']=='517 Generator DE bearing high temperature warning']
    return (df_n,)


@app.cell
def _(df_n):
    df_n
    return


@app.cell
def _(df_n):
    df_n['Device'].unique()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
