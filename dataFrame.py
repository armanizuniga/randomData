import pandas as pd
import randomName
import numpy as np


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


def create_data():
    # Create DataFrame with a column "Name"
    df = pd.DataFrame({"Name": randomName.generate_names()})
    generate_jobs(df)
    # Display the DataFrame
    # Reorder columns for organization
    df = df[["Jobs", "Type", "Name"]]
    print(df)


create_data()
