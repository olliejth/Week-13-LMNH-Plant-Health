"""Transform the files from the short term database into a csv with all of the summary info."""

import pandas as pd


def round_numerical_columns(df: pd.DataFrame, columns: list[str], round_dp: int):
    """Round columns to specified number of dp"""

    for column in columns:
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame.")

    df[columns] = df[columns].apply(lambda x: x.round(round_dp).fillna('N/A'))
    return df


def create_summary(df: pd.DataFrame, round_dp: int = 2) -> pd.DataFrame:
    """
    Creates a dataframe containing a summary of all of the day's recordings.
    Note: standard dev formula is one for a sample, not population
    """

    output_data = df.groupby(["plant_id"])["temperature"].min(
    ).reset_index().rename(columns={"temperature": "min_T"})
    
    output_data["plant_id"] = df["plant_id"].astype(int)

    output_data["max_T"] = df.groupby(
        ["plant_id"])["temperature"].max().reset_index()["temperature"]

    output_data["min_M"] = df.groupby(["plant_id"])[
        "soil_moisture"].min().reset_index()["soil_moisture"]

    output_data["max_M"] = df.groupby(["plant_id"])[
        "soil_moisture"].max().reset_index()["soil_moisture"]

    output_data["water_count"] = df.groupby(["plant_id"])["last_watered"].agg(
        lambda x: x.tolist()).reset_index()["last_watered"].apply(
        lambda x: 0 if all(pd.isna(v) for v in x) else len(set(x)))

    output_data["std_T"] = df.groupby(
        ["plant_id"])["temperature"].std().reset_index()["temperature"]

    output_data["std_M"] = df.groupby(["plant_id"])[
        "soil_moisture"].std().reset_index()["soil_moisture"]

    output_data = output_data.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7]]

    num_cols = ["min_T", "max_T", "min_M", "max_M", "std_T", "std_M"]
    output_data = round_numerical_columns(output_data, num_cols, round_dp)

    return output_data
