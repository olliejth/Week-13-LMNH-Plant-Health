"""Script containing the functions to create altair visualisations for streamlit dashboard."""

import pandas as pd
import altair as alt


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
