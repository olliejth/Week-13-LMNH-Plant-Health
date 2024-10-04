"""Script containing the functions to create altair visualisations for a streamlit dashboard."""

from os import environ as ENV

from dotenv import load_dotenv
import pandas as pd
import altair as alt

from extract_dashboard import get_db_connection


load_dotenv()


def get_botanist_mapping() -> dict:
    """Creates dictionary of botanist names and ids."""

    with get_db_connection() as conn:

        schema_name = ENV['SCHEMA_NAME']

        query = f'''
        SELECT botanist_id, first_name, last_name FROM {schema_name}.botanist
        '''

        df = pd.read_sql(query, conn)

        id_to_name = dict(
            zip(df['botanist_id'], df['first_name'] + ' ' + df['last_name']))

        return id_to_name


def create_botanist_pie(df: pd.DataFrame) -> alt.Chart:
    """Creates pie chart of botanists as a proportion of how many plants they monitor."""

    grouped_df = df.groupby(df["botanist_id"]).count().reset_index()

    botanist_mapping = get_botanist_mapping()
    grouped_df["botanist_name"] = grouped_df["botanist_id"].map(
        botanist_mapping)

    title = alt.TitleParams('Recordings taken per botanist', anchor='middle')
    botanist_pie_chart = alt.Chart(grouped_df, title=title).mark_arc().encode(
        theta="plant_id:Q",
        color="botanist_name:N",
        tooltip=[alt.Tooltip(field="botanist_name", title="Botanist Name"),
                 alt.Tooltip(field="plant_id", title="Readings")]
    )

    return botanist_pie_chart


def create_temperature_bar(df: pd.DataFrame) -> alt.Chart:
    """Creates bar chart of plants against their most recently recorded temperature."""

    df['at'] = pd.to_datetime(df['at'])

    df["high_temperature"] = df["temperature"] >= 50

    recent_df = df.loc[df.groupby('plant_id')['at'].idxmax()]

    title = alt.TitleParams('Plant temperature', anchor='middle')
    temp_bar_chart = alt.Chart(recent_df, title=title).mark_bar().encode(
        x='plant_id:N',
        y='temperature:Q',
        color=alt.Color('high_temperature',
                        scale=alt.Scale(
                            domain=[False, True],
                            range=["#84c9ff", "red"]))
    )

    return temp_bar_chart


def create_temperature_line(df: pd.DataFrame) -> alt.Chart:
    """Creates line chart of plants' temperature over time."""

    df['at'] = pd.to_datetime(df['at']).dt.round('min')

    two_hours_ago = df['at'].max() - pd.Timedelta(hours=2)

    df_filtered = df[df['at'] >= two_hours_ago]

    title = alt.TitleParams(
        'Plant temperature fluctuation over time', anchor='middle')
    temp_line_chart = alt.Chart(df_filtered, title=title).mark_line().encode(
        x='at:T',
        y=alt.Y('temperature:Q').scale(zero=False),
        color='plant_id:N'
    )

    return temp_line_chart


def create_moisture_bar(df: pd.DataFrame) -> alt.Chart:
    """Creates bar chart of plants against their most recently recorded moisture."""

    df['at'] = pd.to_datetime(df['at'])

    df["low_moisture"] = df["soil_moisture"] <= 10

    recent_df = df.loc[df.groupby('plant_id')['at'].idxmax()]

    title = alt.TitleParams('Plant moisture', anchor='middle')
    moist_bar_chart = alt.Chart(recent_df, title=title).mark_bar().encode(
        x='plant_id:N',
        y='soil_moisture:Q',
        color=alt.Color('low_moisture',
                        scale=alt.Scale(
                            domain=[False, True],
                            range=["#84c9ff", "red"]))
    )

    return moist_bar_chart
