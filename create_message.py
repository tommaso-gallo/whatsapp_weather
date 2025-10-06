import pandas as pd
from datetime import datetime, timezone

def describe_preciptations(hourly_df):
    """
    Takes a dataframe with columns:
        - 'date' (datetime)
        - 'precipitation' (mm/hour)
    Returns a string with a natural language weather summary.
    """

    # Ensure correct timezone and sort
    df = hourly_df.copy().sort_values('date')

    # Identify hours with measurable rain
    rain_df = df[df['precipitation'] > 0.1].copy()  # ignore tiny noise

    # Compute average intensity over the rainy hours
    avg_rain = rain_df['precipitation'].mean()

    if rain_df.empty:
        return None, None

    # Categorise rain intensity
    if avg_rain < 2:
        intensity = "light"
    elif avg_rain < 6:
        intensity = "moderate"
    else:
        intensity = "heavy"

    # Extract hour and define time periods
    rain_df['hour'] = rain_df['date'].dt.hour

    # Treat early-morning hours (0–5) as belonging to the "next day"
    rain_df.loc[rain_df['hour'] < 6, 'hour'] += 24

    # Define periods from 6am to next day's 6am
    bins = [6, 12, 18, 24, 30]
    labels = ["morning", "afternoon", "evening", "night"]

    rain_df['period'] = pd.cut(
        rain_df['hour'], bins=bins, labels=labels, right=False, include_lowest=True
    )

    # Determine when it rains the most
    dominant_period = (
        rain_df.groupby('period', observed=True)['precipitation']
        .sum()
        .idxmax()
    )

    return intensity, dominant_period

def assemble_message(hourly_df, daily_df):
    max_T = int(daily_df["temperature_2m_max"][0])
    min_T = int(daily_df["temperature_2m_min"][0])
    message_parts = [f"The temperature will range from {min_T}°C to {max_T}°C."]

    maxpp = daily_df["precipitation_probability_max"][0]

    if maxpp == 0:
        average_cloud_cover = hourly_df["cloud_cover"].mean()

        if average_cloud_cover < 33:
            message_parts.append("Today will be sunny!!")
        elif average_cloud_cover < 67:
            message_parts.append("There will be no rain today, but it will be partially cloudy")
        else:
            message_parts.append("There will be no rain today, but it will be cloudy")
    elif maxpp < 33:
        message_parts.append("It is unlikely it will rain today.")
    elif maxpp < 67:
        message_parts.append("It will probably rain today.")
        intensity, dominant_period = describe_preciptations(hourly_df)
        message_parts.append(f"Precipitations will be {intensity}, mostly during the {dominant_period}")
    else:
        message_parts.append("It is highly likely it will rain today.")
        intensity, dominant_period = describe_preciptations(hourly_df)
        message_parts.append(f"Precipitations will be {intensity}, mostly during the {dominant_period}")

    return "\n".join(message_parts)





