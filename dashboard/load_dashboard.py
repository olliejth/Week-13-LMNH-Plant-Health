"""Loads visualisations to constantly running dashboard."""

import streamlit as st

from extract_dashboard import extract_readings
from transform_dashboard import create_botanist_pie, create_temperature_bar
from transform_dashboard import create_moisture_bar, create_temperature_line
from longterm_extract import extract_s3_files
from longterm_transform import (concat_csvs, get_times_watered,
                                get_max_temp_per_plant, get_min_moisture_per_plant)

if __name__ == "__main__":

    # SHORT TERM VISUALISATIONS

    plants_df = extract_readings()

    st.sidebar.markdown("# Sidebar")
    plant_ids = plants_df["plant_id"].unique().tolist()
    selected_plants = st.sidebar.multiselect("Plant IDs", options=plant_ids)

    if len(selected_plants) > 0:
        plants_df = plants_df[plants_df["plant_id"].isin(selected_plants)]

    botanist_plants_pie = create_botanist_pie(plants_df)
    temp_bar_chart = create_temperature_bar(plants_df)
    temp_line_chart = create_temperature_line(plants_df)
    moist_bar_chart = create_moisture_bar(plants_df)

    st.altair_chart(botanist_plants_pie, use_container_width=True)
    st.altair_chart(temp_bar_chart, use_container_width=True)
    st.altair_chart(temp_line_chart, use_container_width=True)
    st.altair_chart(moist_bar_chart, use_container_width=True)

    # LONG TERM VISUALISATIONS:

    longterm_df = concat_csvs(extract_s3_files())

    water_count_bar = get_times_watered(longterm_df)
    max_temp_bar = get_max_temp_per_plant(longterm_df)
    min_moist_br = get_min_moisture_per_plant(longterm_df)

    st.altair_chart(water_count_bar, use_container_width=True)
    st.altair_chart(max_temp_bar, use_container_width=True)
    st.altair_chart(min_moist_br, use_container_width=True)
