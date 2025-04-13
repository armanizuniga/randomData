import random


# Function to mimic metrics taken from NPS website. Columns added:
# NPS, TMS, Surveys, Full Surveys, AppleCare, Trade in, Apple Intelligence
def generate_nps(df):
    tms_list = []
    nps_list = []
    surveys_list = []
    full_surveys_list = []

    for _ in range(len(df)):
        # Total responses
        full_surveys = random.randint(0, 3)
        surveys = random.randint(1, 11) + full_surveys
        total_responses = surveys

        # Weighted random scores (favoring 5s for TMS and lower for NPS)
        tms_weights = [0.025, 0.01, 0.01, 0.01, 0.9]  # More likely to rate employee highly
        nps_weights = [0.025, 0.05, 0.05, 0.02, 0.8]  # More varied for store experience
        tms_scores = random.choices([1, 2, 3, 4, 5], weights=tms_weights, k=total_responses)
        nps_scores = random.choices([1, 2, 3, 4, 5], weights=nps_weights, k=total_responses)

        # NPS Calculation
        nps_promoters = nps_scores.count(5)
        nps_detractors = sum(score <= 3 for score in nps_scores)
        nps = round(((nps_promoters - nps_detractors) / total_responses) * 100)

        # TMS Calculation
        tms_promoters = tms_scores.count(5)
        tms_detractors = sum(score <= 3 for score in tms_scores)
        tms = round(((tms_promoters - tms_detractors) / total_responses) * 100)

        # Store results
        surveys_list.append(surveys)
        full_surveys_list.append(full_surveys)
        nps_list.append(nps)
        tms_list.append(tms)

    # Add to DataFrame
    df['Survey Qty'] = surveys_list
    df['Full Survey Qty'] = full_surveys_list
    df['NPS'] = nps_list
    df['TMS'] = tms_list

    # Arrays to hold generated survey percentage values
    ac = []
    ti = []
    ai = []

    # Keeps percentages consistent with the amount of Full Surveys taken
    for full in df["Full Survey Qty"]:
        if full == 0:
            ac.append(0.0)
            ti.append(0.0)
            ai.append(0.0)
        else:
            options = [round((i / full) * 100) for i in range(full + 1)]
            ac.append(random.choice(options))
            ti.append(random.choice(options))
            ai.append(random.choice(options))

    df["Discussed AppleCare"] = ac
    df["Offered Trade In"] = ti
    df["Apple Intelligence"] = ai
    return df
