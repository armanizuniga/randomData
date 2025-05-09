import numpy as np
import random

zone_weights = {
    'Genius': {
        'Mobile Support Hours': 5,
        'Mac Support Hours': 6,
        'iPhone Repair Hours': 3,
        'Mac Repair Hours': 3,
        'Repair Pickup': 1,
        'Daily Download': 1,
        'Guided': 0.5,
        'Connection': 0.5
    },
    'Technical Expert': {
        'Mobile Support Hours': 8,
        'iPhone Repair Hours': 4,
        'Repair Pickup': 2,
        'GB On Point': 2,
        'Daily Download': 1,
        'Guided': 0.5,
        'Connection': 0.5
    },
    'Technical Specialist': {
        'Mobile Support Hours': 8,
        'Repair Pickup': 2,
        'GB On Point': 2,
        'Daily Download': 1,
        'Guided': 0.5,
        'Connection': 0.5
    }
}

zone_caps = {
    'Connection': 4,
    'Guided': 4,
    'Daily Download': 8,
    'GB On Point': 13,
    'Repair Pickup': 14
}


def distribute_hours(df):
    zone_columns = [
        'Mobile Support Hours', 'Mac Support Hours', 'iPhone Repair Hours', 'Mac Repair Hours',
        'Repair Pickup', 'GB On Point', 'Daily Download', 'Guided', 'Connection'
    ]

    # Initialize zone columns
    for col in zone_columns:
        df[col] = 0

    for idx, row in df.iterrows():
        role = row['Jobs']
        total_hours = row['Total Hours']
        weights = zone_weights.get(role, {})

        zones = list(weights.keys())
        probs = np.array(list(weights.values()), dtype=float)
        probs /= probs.sum()

        # Track assigned hours
        remaining = total_hours
        zone_hours = dict.fromkeys(zone_columns, 0)

        # === Guarantee minimums ===
        if role in ['Technical Expert', 'Technical Specialist']:
            zone_hours['Mobile Support Hours'] = 1
            remaining -= 1

        elif role == 'Genius':
            # Reserve 1 hour for Mobile or Mac support
            # Prioritize Mobile if both are in weights
            if 'Mobile Support Hours' in weights:
                zone_hours['Mobile Support Hours'] = 1
            else:
                zone_hours['Mac Support Hours'] = 1
            remaining -= 1

        # === Begin distribution ===
        attempt_limit = 500
        attempts = 0

        while remaining > 0 and attempts < attempt_limit:
            chosen = np.random.choice(zones, p=probs)
            max_assignable = min(4, remaining)

            cap = zone_caps.get(chosen, float('inf'))
            already_assigned = zone_hours[chosen]
            available_for_zone = cap - already_assigned

            if available_for_zone > 0:
                allocation = min(random.randint(1, 4), available_for_zone, max_assignable)
                zone_hours[chosen] += allocation
                remaining -= allocation

            attempts += 1

        for col in zone_columns:
            df.at[idx, col] = zone_hours[col]

    return df
