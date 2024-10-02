"""Transform the files from the short term database into a csv with all of the summary info."""

import pandas as pd


def create_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Creates a dataframe containing a summary of all of the day's recordings."""

    output_data = df.groupby(["plant_id"])["temperature"].min(
    ).reset_index().rename(columns={"temperature": "min_T"})

    output_data["plant_id"] = df["plant_id"]

    output_data["max_T"] = df.groupby(
        ["plant_id"])["temperature"].max().reset_index()["temperature"]

    output_data["min_M"] = df.groupby(["plant_id"])[
        "soil_moisture"].min().reset_index()["soil_moisture"]

    output_data["max_M"] = df.groupby(["plant_id"])[
        "soil_moisture"].max().reset_index()["soil_moisture"]

    output_data["water_count"] = df.groupby(["plant_id"])["last_watered"].agg(
        lambda x: x.tolist()).reset_index()["last_watered"].apply(lambda x: len(set(x)))

    output_data["std_T"] = df.groupby(
        ["plant_id"])["temperature"].std().reset_index()["temperature"]

    output_data["std_M"] = df.groupby(["plant_id"])[
        "soil_moisture"].std().reset_index()["soil_moisture"]

    output_data = output_data.iloc[:, [0, 2, 1, 3, 4, 5, 6, 7]]

    return output_data
