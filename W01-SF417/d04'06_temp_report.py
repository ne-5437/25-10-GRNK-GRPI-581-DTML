import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import numpy as np

    def create_detailed_temperature_report():

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        pd.set_option('display.float_format', '{:,.2f}'.format) 

        param_cols = [
            'Trafo 2 winding temperature max 10M (ºC)',
            'Trafo 3 winding temperature max 10M (ºC)',
            'Bearing D.E. Temperature max 10M (ºC)',
            'Bearing N.D.E. Temperature max 10M (ºC)',
            'Gearbox bearing temperature max 10M (ºC)',
            'Gearbox oil temperature max 10M (ºC)',
            'Generator windings temperature 1 max 10M (ºC)',
            'Generator windings temperature 2 max 10M (ºC)',
            'Generator windings temperature 3 max 10M (ºC)',
            'Generator’s sliprings temperature max 10M (ºC)',
            'Nacelle temperature average 10M (ºC)',
            'Trafo 1 winding temperature max 10M (ºC)'
        ]

        try:
            print("Loading X-Minutal.csv...")
            df_minutal = pd.read_csv("X-Minutal.csv", delimiter=';')

            print("\n--- Raw Data Check (Before Cleaning) ---")
            raw_trafo2_temp = pd.to_numeric(df_minutal['Trafo 2 winding temperature max 10M (ºC)'], errors='coerce')
            print(f"Raw 'Trafo 2' Min (as read from file): {raw_trafo2_temp.min()}")
            print(f"Raw 'Trafo 2' Max (as read from file): {raw_trafo2_temp.max()}")

            df_minutal['Date'] = pd.to_datetime(
                df_minutal['Date'], 
                format='%d/%m/%Y %H:%M:%S.%f', 
                errors='coerce'
            )

            param_cols_found = []
            for col in param_cols:
                if col in df_minutal.columns:
                    param_cols_found.append(col)

            print("\nCleaning temperature data: Treating values <= 0 as invalid (NaN)...")
            for col in param_cols_found:
                df_minutal[col] = pd.to_numeric(df_minutal[col], errors='coerce')
                df_minutal[col] = df_minutal[col].apply(lambda x: x if x > 0 else np.nan)

            print("\n--- Overall Cleaned Data Check (like a simple Excel sort) ---")
            clean_trafo2_temp = df_minutal['Trafo 2 winding temperature max 10M (ºC)'].dropna()
            print(f"Overall Cleaned 'Trafo 2' Min (all devices, all times): {clean_trafo2_temp.min()}")
            print(f"Overall Cleaned 'Trafo 2' Max (all devices, all times): {clean_trafo2_temp.max()}")

            print("\nLoading Full AWS.csv...")
            df_aws = pd.read_csv("Full AWS.csv", delimiter=';')

            df_aws['Start Date'] = pd.to_datetime(
                df_aws['Start Date'], 
                format='%d/%m/%Y %H:%M:%S.%f', 
                errors='coerce'
            )
            df_aws['End Date'] = pd.to_datetime(
                df_aws['End Date'], 
                format='%d/%m/%Y %H:%M:%S.%f', 
                errors='coerce'
            )

            df_minutal = df_minutal.dropna(subset=['Date', 'Device'] + param_cols_found)
            df_aws = df_aws.dropna(subset=['Start Date', 'End Date', 'Device', 'Category'])

            df_minutal_sorted = df_minutal.sort_values('Date')
            df_aws_sorted = df_aws.sort_values('Start Date')

            print("Merging dataframes on time intervals...")
            merged_df = pd.merge_asof(
                df_minutal_sorted,
                df_aws_sorted,
                left_on='Date',
                right_on='Start Date',
                by='Device',
                direction='backward'
            )

            valid_merged_df = merged_df[
                (merged_df['Date'] >= merged_df['Start Date']) & 
                (merged_df['Date'] <= merged_df['End Date'])
            ]

            valid_merged_df = valid_merged_df.dropna(subset=['Start Date', 'Category'])

            print(f"Found {len(valid_merged_df)} valid 10-minute records with corresponding events.")

            categories_of_interest = ['State', 'Warning', 'Alarm']
            filtered_df = valid_merged_df[valid_merged_df['Category'].isin(categories_of_interest)]

            if filtered_df.empty:
                print("\nNo data found matching 'State', 'Warning', or 'Alarm' after merging.")
                return

            print("Calculating new Min/Max statistics, grouped by *Device* and *Category*...")

            final_stats = filtered_df.groupby(['Device', 'Category'])[param_cols_found].agg(['min', 'max'])

            if not final_stats.empty:
                final_stats.to_csv("detailed_device_temperature_ranges.csv")
                print("\nDetailed report saved to 'detailed_device_temperature_ranges.csv'")

                print("\n--- Detailed Temperature Operation Ranges (Min/Max) by Device and Category ---")

                devices = final_stats.index.get_level_values('Device').unique()

                for device in devices:
                    print(f"\n\n--- Device: {device} ---")

                    device_data = final_stats.loc[device].T

                    cols_order = [col for col in ['State', 'Warning', 'Alarm'] if col in device_data.columns]
                    print(device_data[cols_order])

            else:
                print("No matching data found to create a report.")


        except FileNotFoundError as e:
            print(f"\nERROR: File not found. Make sure '{e.filename}' is in the same directory.")
        except Exception as e:
            print(f"\nAn error occurred: {e}")

    if __name__ == "__main__":
        create_detailed_temperature_report()
    return


if __name__ == "__main__":
    app.run()
