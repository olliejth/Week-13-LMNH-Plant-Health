"""Extracts long term stored plant health csv files from an AWS S3 bucket."""

import pandas as pd
import altair as alt

from longterm_extract import extract_s3_files


def concat_csvs(files: list[str]) -> pd.DataFrame:
    """Concatenates local csv files by name into a single pandas dataframe."""

    df_list = []
    for file in files:
        df = pd.read_csv(file)
        df_list.append(df)

    return pd.concat(df_list)


def get_times_watered(df: pd.DataFrame) -> alt.Chart:
    """
    Gets the average number of times each plant is watered per day.
    Returns a bar chart of the results.
    """

    watered_df = df.groupby("plant_id").mean().reset_index()

    title = alt.TitleParams(
        'Average daily water count per plant', anchor='middle')
    bar_chart = alt.Chart(watered_df, title=title).mark_bar().encode(
        x="plant_id:N",
        y="water_count:Q").configure_bar(
        color='red'
    )

    return bar_chart


def get_max_temp_per_plant(df: pd.DataFrame) -> alt.Chart:

    max_temp_df = df.groupby("plant_id").max().reset_index()

    title = alt.TitleParams(
        'Max T experienced by each plant', anchor='middle')
    max_temp_bar = alt.Chart(max_temp_df, title=title).mark_bar().encode(
        x="plant_id:N",
        y="max_T:Q").configure_bar(
        color='red'
    )

    return max_temp_bar


def get_min_moisture_per_plant(df: pd.DataFrame) -> alt.Chart:

    min_moist_df = df.groupby("plant_id").min().reset_index()

    title = alt.TitleParams(
        'Min M experienced by each plant', anchor='middle')
    min_moist_bar = alt.Chart(min_moist_df, title=title).mark_bar().encode(
        x="plant_id:N",
        y="min_M:Q").configure_bar(
        color='red'
    )

    return min_moist_bar


if __name__ == "__main__":

    s3_files = extract_s3_files()

    my_df = concat_csvs(s3_files)

    print(my_df.head())
