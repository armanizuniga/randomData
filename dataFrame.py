import pandas as pd
import randomName
import numpy as np
import random
import hour_distribution_engine
import nps_medallia_model


# Function to generate job roles and types then appends to the existing dataFrame
def generate_jobs(df):
    total_employees = len(df)

    # Define role distribution
    num_genius = int(total_employees * 0.25)
    num_expert = int(total_employees * 0.25)
    num_specialist = total_employees - num_genius - num_expert

    # Create job roles
    jobs = (
            ["Genius"] * num_genius +
            ["Technical Expert"] * num_expert +
            ["Technical Specialist"] * num_specialist
    )
    np.random.shuffle(jobs)

    # Define type distribution
    num_ft = int(total_employees * 0.5)
    num_pt = total_employees - num_ft

    job_type = ["FT"] * num_ft + ["PT"] * num_pt
    np.random.shuffle(job_type)

    # Add columns
    df["Jobs"] = jobs
    df["Type"] = job_type

    return df


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
    return df


# Function randomly generates the amount of specific appointment taken dependent on job role
def add_sessions(df):
    df["Mac Sessions"] = 0
    df["Mobile Sessions"] = 0

    for idx, row in df.iterrows():
        role = row["Jobs"]

        if role == "Genius":
            mac_hours = row.get("Mac Support Hours", 0)
            mobile_hours = row.get("Mobile Support Hours", 0)

            # You can adjust the range of randomization if you want to increase or decrease appointments
            df.at[idx, "Mac Sessions"] = int(mac_hours * random.uniform(2.5, 3.3))
            df.at[idx, "Mobile Sessions"] = int(mobile_hours * random.uniform(2.5, 3.5))

        elif role in ["Technical Expert", "Technical Specialist"]:
            mobile_hours = row.get("Mobile Support Hours", 0)
            # You can adjust the range of randomization if you want to increase or decrease appointments
            df.at[idx, "Mobile Sessions"] = int(mobile_hours * random.uniform(2.5, 3.5))

    return df


# Function  to add another column with the sum
def add_customers_helped(df):
    df["Customers Helped"] = df["Mac Sessions"] + df["Mobile Sessions"]
    return df


# Function to calculate the average amount sessions taken per queued hour
def add_spqh(df):
    df["SPQH"] = round(df["Customers Helped"] / (df["Mac Support Hours"] + df["Mobile Support Hours"]), 2)
    return df


# Function that adds two more columns about mac duration and mobile duration
def add_duration(df):
    df["Mac Duration"] = 0
    df["Mobile Duration"] = 0

    for idx, row in df.iterrows():
        role = row["Jobs"]

        if role == "Genius":
            # You can adjust the range of randomization if you want to increase or decrease appointments
            df.at[idx, "Mac Duration"] = random.randint(11, 34)
            df.at[idx, "Mobile Duration"] = random.randint(11, 25)

        elif role in ["Technical Expert", "Technical Specialist"]:
            # You can adjust the range of randomization if you want to increase or decrease appointments
            df.at[idx, "Mobile Duration"] = random.randint(11, 25)

    return df


# Function to generate fake SUR and opportunities metric
def generate_sur_and_opportunities(df):
    opportunities_list = []
    successful_repairs_list = []
    sur_list = []

    for _, row in df.iterrows():
        iphone_hours = row.get('iPhone Repair Hours', 0)

        if iphone_hours > 0:
            repairs_per_hour = random.choice([1.0, 1.5, 2.0])
            opportunities = max(1, int(iphone_hours * repairs_per_hour))

            successful_repairs = random.randint(0, opportunities)
            sur = round((successful_repairs / opportunities) * 100, 2)
        else:
            opportunities = 0
            successful_repairs = 0
            sur = 0.0

        opportunities_list.append(opportunities)
        successful_repairs_list.append(successful_repairs)
        sur_list.append(sur)

    df['Opportunities'] = opportunities_list
    df['SUR'] = sur_list

    return df


# Function to generate random business intro metrics
def generate_business_intros(df):
    df["Business Intros"] = [random.randint(0, 10) for _ in range(len(df))]
    return df


# Main function that generates randomized test dataFrame
def create_data():
    # Create DataFrame and generate random metric values
    df = pd.DataFrame({"Name": randomName.generate_names()})
    df = generate_jobs(df)
    df = generate_total_hours(df)
    df = hour_distribution_engine.distribute_hours(df)
    df = add_sessions(df)
    df = add_customers_helped(df)
    df = add_spqh(df)
    df = add_duration(df)
    df = nps_medallia_model.generate_nps(df)
    df = generate_sur_and_opportunities(df)
    df = generate_business_intros(df)

    # Display the DataFrame and reorder columns for organization
    df = df[["Jobs", "Type", "Name", "SPQH", "Customers Helped", "Mac Duration", "Mobile Duration", "NPS", "TMS", "SUR",
             "Business Intros", "Discussed AppleCare", "Offered Trade In", "Apple Intelligence", "Survey Qty",
             "Full Survey Qty", "Opportunities", "Mac Sessions", "Mobile Sessions", "Mobile Support Hours",
             "Mac Support Hours", "iPhone Repair Hours", "Mac Repair Hours", "Repair Pickup", "GB On Point",
             "Daily Download", "Guided", "Connection", "Total Hours"]]
    # Sort based on job tiles and the name in alphabetical order
    df = df.sort_values(by=["Jobs", "Name"])
    # Output to a text file for easy reading and testing
    with open("output.txt", "w") as f:
        f.write(df.to_string(index=False))


create_data()
