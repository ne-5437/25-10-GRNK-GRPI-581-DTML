import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    PARAMETER = 'Trafo 2 winding temperature max 10M (ºC)'

    # Categories and highly visible colors
    CATEGORIES = [
        'State',
        'Warning',
        'Alarm',
        '517 Generator DE bearing high temperature warning'
    ]

    COLORS = {
        'State': '#00FFFF',    # Cyan
        'Warning': '#FFA500',  # Orange
        'Alarm': '#FF2A2A',    # Red
        '517 Generator DE bearing high temperature warning': '#3FEF3F'  # Parrot Green
    }

    def plot_separate_category_floating_bars():
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

        # Filter AWS to only the categories in CATEGORIES
        df_aws = df_aws[df_aws['Category'].isin(CATEGORIES)]
        if df_aws.empty:
            print("No events found for the selected categories.")
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
            print("No overlapping minutal data found for the selected events.")
            return

        # Compute min and max per device per category
        stats = merged_df.groupby(['Device', 'Category'])[PARAMETER].agg(['min','max']).reset_index()
        devices = stats['Device'].unique()
        x = np.arange(len(devices))
        width = 0.15  # narrower bars so multiple categories fit

        # Plot
        fig, ax = plt.subplots(figsize=(22, 10))  # expanded figure
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')
        plt.style.use('dark_background')

        alpha_val = 0.6

        # Determine global min and max for y-axis
        global_min = stats['min'].min()
        global_max = stats['max'].max()
        y_min = max(0, global_min - 2)  # start a bit below the min
        y_max = global_max + 2  # extend above the max

        # Plot each category separately
        for idx, cat in enumerate(CATEGORIES):
            cat_data = stats[stats['Category'] == cat]
            bottoms = []
            heights = []
            for device in devices:
                row = cat_data[cat_data['Device'] == device]
                if not row.empty:
                    bottoms.append(float(row['min']))
                    heights.append(float(row['max'] - row['min']))
                else:
                    bottoms.append(0)
                    heights.append(0)
            ax.bar(
                x + idx*width - (len(CATEGORIES)/2)*width,  # shift bars for visibility
                heights,
                width,
                bottom=bottoms,
                color=COLORS[cat],
                alpha=alpha_val,
                edgecolor='black',
                label=cat
            )

        # Axes and labels
        ax.set_xticks(x)
        ax.set_xticklabels(devices, rotation=45, ha='right', color='black')
        ax.set_ylabel('Temperature (°C)', color='black', fontsize=12)
        ax.set_xlabel('Devices', color='black', fontsize=12)
        ax.set_title(f'Floating Min-Max Temperature Bars per Category — {PARAMETER}', color='blue', fontsize=16, fontweight='bold')
        ax.grid(True, linestyle=':', alpha=0.3)
        ax.spines['bottom'].set_color('black')
        ax.spines['left'].set_color('black')
        ax.tick_params(colors='black')

        # Apply new y-axis range
        ax.set_ylim(y_min, y_max)

        legend = ax.legend(facecolor='white', edgecolor='black')
        for text in legend.get_texts():
            text.set_color('black')

        plt.tight_layout()
        plt.show()
        print("Expanded floating min-max plot complete.")

    if __name__ == "__main__":
        plot_separate_category_floating_bars()
    return


if __name__ == "__main__":
    app.run()
