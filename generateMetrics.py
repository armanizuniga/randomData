import dataFrame
import os
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar


def generate_monthly_metrics(start_date=None):
    """
        Generate 12 months of data starting from the specified date
        and save each month's data to the macOS desktop

        Parameters:
        start_date (str): Starting date in format 'YYYY-MM-DD', defaults to current date

        Returns:
        list: List of all generated DataFrames
        """
    # If no start date is provided, use current date
    if start_date is None:
        current_date = datetime.now()
        # Go back to the first day of the current month
        start_date = current_date.replace(day=1)
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').replace(day=1)

    # Get macOS desktop path
    desktop_path = os.path.expanduser("~/Desktop")

    # Store all dataframes
    all_dfs = []

    # Generate data for 12 months
    for i in range(12):
        # Calculate month date properly using date utility package
        current_month_date = start_date + relativedelta(months=i)

        # Set date to the last day of the month
        last_day = calendar.monthrange(current_month_date.year, current_month_date.month)[1]
        end_of_month = current_month_date.replace(day=last_day)

        month_name = current_month_date.strftime("%B")
        year = current_month_date.strftime("%Y")

        print(f"Generating data for {month_name} {year}...")

        # Generate monthly data
        df = dataFrame.create_data(period="monthly")

        # Add month and year columns to the DataFrame
        df["Report_Date"] = end_of_month.strftime("%Y-%m-%d")
        df["Month"] = month_name
        df["Year"] = year

        # Reorder columns to put date columns first
        date_columns = ["Report_Date", "Month", "Year"]
        other_columns = [col for col in df.columns if col not in date_columns]
        df = df[date_columns + other_columns]

        # Save the DataFrame as CSV for easier data processing later
        csv_file_path = os.path.join(desktop_path, f"Monthly_Metrics_{month_name}_{year}.csv")
        df.to_csv(csv_file_path, index=False)
        print(f"Data saved to {desktop_path}")

        # Store DataFrame in our list
        all_dfs.append(df)

        # Optionally create a combined yearly dataset
    yearly_df = pd.concat(all_dfs)
    yearly_file_path = os.path.join(desktop_path, f"Yearly_Metrics.csv")
    yearly_df.to_csv(yearly_file_path, index=False)

    print(f"Complete yearly dataset saved to {yearly_file_path}")

    return all_dfs


def generate_weekly_data(start_date=None, num_weeks=52):
    """
    Generate weekly data for a year starting from the specified date
    and save each week's data to the macOS desktop

    Parameters:
    start_date (str): Starting date in format 'YYYY-MM-DD', defaults to current date
    num_weeks (int): Number of weeks to generate, defaults to 52 (approximately a year)

    Returns:
    list: List of all generated DataFrames
    """
    # If no start date is provided, use current date
    if start_date is None:
        current_date = datetime.now()
        # Go back to the start of the current week (Monday)
        start_date = current_date - timedelta(days=current_date.weekday())
    else:
        temp_date = datetime.strptime(start_date, '%Y-%m-%d')
        # Adjust to start of week (Monday)
        start_date = temp_date - timedelta(days=temp_date.weekday())

    # Get macOS desktop path
    desktop_path = os.path.expanduser("~/Desktop")

    # Store all dataframes
    all_dfs = []

    # Generate data for specified number of weeks
    for i in range(num_weeks):
        # Calculate week start and end dates
        week_start = start_date + timedelta(weeks=i)
        week_end = week_start + timedelta(days=6)  # End of week (Sunday)

        # Format dates for display
        week_start_str = week_start.strftime("%Y-%m-%d")
        week_end_str = week_end.strftime("%Y-%m-%d")
        month_name = week_end.strftime("%B")
        year = week_end.strftime("%Y")
        week_number = week_start.strftime("%U")  # Week number (00-53)

        print(f"Generating data for Week {week_number} ({week_start_str} to {week_end_str})...")

        # Generate weekly data
        df = dataFrame.create_data(period="weekly")

        # Add date columns to the DataFrame
        df["Report_Date"] = week_end_str
        df["Week_Start"] = week_start_str
        df["Week_End"] = week_end_str
        df["Week_Number"] = f"Week {week_number}"
        df["Month"] = month_name
        df["Year"] = year

        # Reorder columns to put date columns first
        date_columns = ["Report_Date", "Week_Number", "Week_Start", "Week_End", "Month", "Year"]
        other_columns = [col for col in df.columns if col not in date_columns]
        df = df[date_columns + other_columns]

        # Also save as CSV for easier data processing later
        # csv_file_path = os.path.join(desktop_path, f"Weekly_Metrics_W{week_number}_{year}.csv")
        # df.to_csv(csv_file_path, index=False)
        # print(f"Data saved to {desktop_path}")

        # Store DataFrame in our list
        all_dfs.append(df)

    # Create a combined dataset of all weeks
    all_weeks_df = pd.concat(all_dfs)
    all_weeks_file_path = os.path.join(desktop_path, f"All_Weekly_Metrics.csv")
    all_weeks_df.to_csv(all_weeks_file_path, index=False)

    print(f"Complete dataset of all weeks saved to {all_weeks_file_path}")

    return all_dfs


# Usage Monthly:
# test = generate_monthly_metrics()  # Uses current date as starting point
# test = generate_yearly_data("2024-01-01")  # Starts from January 2024
# Usage Weekly:
# test = generate_weekly_data()
