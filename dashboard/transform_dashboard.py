"""Script containing the functions to create altair visualisations for streamlit dashboard."""

import pandas as pd
import altair as alt
from datetime import datetime, timedelta


def create_botanist_pie(df: pd.DataFrame) -> alt.Chart:
    """Creates pie chart of botanists as a proportion of how many plants they monitor."""

    grouped_df = df.groupby(df["botanist_id"]).count().reset_index()

    title = alt.TitleParams('Botanist plant count', anchor='middle')
    botanist_pie_chart = alt.Chart(grouped_df, title=title).mark_arc().encode(
        theta="plant_id:Q",
        color="botanist_id:N"
    )

    return botanist_pie_chart


def create_temperature_bar(df: pd.DataFrame):
    """Creates bar chart of plants against their most recently recorded temperature."""

    df['at'] = pd.to_datetime(df['at'])

    recent_df = df.loc[df.groupby('plant_id')['at'].idxmax()]

    title = alt.TitleParams('Plant temperature', anchor='middle')
    temp_bar_chart = alt.Chart(recent_df, title=title).mark_bar().encode(
        x='plant_id:N',
        y='temperature:Q'
    )

    return temp_bar_chart


def create_temperature_line(df: pd.DataFrame):
    """Creates bar chart of plants against their most recently recorded temperature."""

    df['at'] = pd.to_datetime(df['at'])

    three_hours_ago = pd.Timestamp.now() - pd.Timedelta(hours=3)

    # Filter the DataFrame to only include readings from the past hour
    df_filtered = df[df['at'] >= three_hours_ago]

    title = alt.TitleParams('Plant temperature over time', anchor='middle')
    temp_line_chart = alt.Chart(df_filtered, title=title).mark_line().encode(
        x='at:T',  # 'at' column for time on x-axis
        y='temperature:Q',  # 'temperature' column for y-axis (quantitative)
        color='plant_id:N'  # Different color for each plant_id
    )

    return temp_line_chart


def create_moisture_bar(df: pd.DataFrame):
    """Creates bar chart of plants against their most recently recorded temperature."""

    df['at'] = pd.to_datetime(df['at'])

    recent_df = df.loc[df.groupby('plant_id')['at'].idxmax()]

    title = alt.TitleParams('Plant moisture', anchor='middle')
    moist_bar_chart = alt.Chart(recent_df, title=title).mark_bar().encode(
        x='plant_id:N',
        y='soil_moisture:Q'
    )

    return moist_bar_chart
