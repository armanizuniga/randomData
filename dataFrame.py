import pandas as pd
import randomName
import numpy as np


def create_data():
    # Create DataFrame with a column "Name"
    df = pd.DataFrame({"Name": randomName.generate_names()})

    # Define job distribution
    jobs = ["Genius"] * 10 + ["Technical Expert"] * 10 + ["Technical Specialist"] * 20
    np.random.shuffle(jobs)  # Randomize the order
    df["Jobs"] = jobs
    df["Type"] = ["FT"] * 17 + ["PT"] * 23
    df = df[["Jobs", "Type", "Name"]]  # Reorder columnes
    # Display the DataFrame
    print(df)


create_data()
