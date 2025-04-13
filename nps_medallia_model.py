import random


# Function to mimic metrics taken from NPS website. Columns added:
# NPS, TMS, Surveys, Full Surveys, AppleCare, Trade in, Apple Intelligence
def generate_nps(df):
    tms_list = []
    nps_list = []
    survey_list = []
    full_survey_list = []

    for _ in range(len(df)):
        surveys = random.randint(0, 11)
        full_surveys = random.randint(0, min(3, surveys))
        total_responses = surveys + full_surveys

        if total_responses > 0:
            # Simulate 1–5 ratings for both TMS and NPS questions
            ratings = [random.choices(
                population=[random.randint(1, 3), 4, 5],
                weights=[0.2, 0.2, 0.6],
                k=1
            )[0] for _ in range(total_responses)]

            promoters = ratings.count(5)
            detractors = sum(1 for r in ratings if r <= 3)

            nps = round(((promoters - detractors) / total_responses) * 100)
            tms = round((sum(ratings) / total_responses) / 5 * 100)
        else:
            nps = 0.0
            tms = 0.0

        survey_list.append(surveys)
        full_survey_list.append(full_surveys)
        nps_list.append(round(nps, 2))
        tms_list.append(tms)

    df['Survey Qty'] = survey_list
    df['Full Survey Qty'] = full_survey_list
    df['TMS'] = tms_list
    df['NPS'] = nps_list

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
