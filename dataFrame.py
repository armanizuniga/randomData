import pandas as pd
import randomName
import numpy as np
import random
import hour_distribution_engine


# Function to generate job roles and types then appends to the existing dataFrame
def generate_jobs(df):
    # Define job roles and full-time/part-time distribution
    jobs = ["Genius"] * 10 + ["Technical Expert"] * 10 + ["Technical Specialist"] * 20
    job_type = ["FT"] * 17 + ["PT"] * 23

    # Randomize the order
    np.random.shuffle(jobs)
    np.random.shuffle(job_type)

    # Add new columns to the existing dataFrame
    df["Jobs"] = jobs
    df["Type"] = job_type


# Function to generate the total amount of hours worked for part-time and full-time employees
def generate_total_hours(df):
    def generate_hours(row):
        if row["Type"] == "FT":
            return random.randint(130, 150)
        elif row["Type"] == "PT":
            return random.randint(60, 110)
        else:
            return 0

    # Applies above function to the Type columns and generates a new column to add to the existing dataFrame
    df["Total Hours"] = df.apply(generate_hours, axis=1)


# Main function that generates randomized test dataFrame
def create_data():
    # Create DataFrame with a column "Name"
    df = pd.DataFrame({"Name": randomName.generate_names()})
    generate_jobs(df)
    generate_total_hours(df)
    df = hour_distribution_engine.distribute_hours(df)

    # Display the DataFrame and reorder columns for organization
    df = df[["Jobs", "Type", "Name", "Mobile Support Hours", "Mac Support Hours", "iPhone Repair Hours",
             "Mac Repair Hours", "Repair Pickup", "GB On Point", "Daily Download", "Guided", "Connection",
             "Total Hours"]]
    df = df.sort_values(by=["Jobs", "Name"])

    with open("output.txt", "w") as f:
        f.write(df.to_string(index=False))



create_data()
