"""Loads visualisations to constantly running dashboard."""

import pandas as pd
import streamlit as st

from extract_dashboard import extract_readings
from transform_dashboard import create_botanist_pie, create_temperature_bar
from transform_dashboard import create_moisture_bar, create_temperature_line

if __name__ == "__main__":

    plants_df = extract_readings()

    st.sidebar.markdown("# Sidebar")
    plant_ids = plants_df["plant_id"].unique().tolist()
    selected_plants = st.sidebar.multiselect("Plant IDs", options=plant_ids)

    botanist_plants_pie = create_botanist_pie(plants_df)
    temp_bar_chart = create_temperature_bar(plants_df, selected_plants)
    temp_line_chart = create_temperature_line(plants_df, selected_plants)
    moist_bar_chart = create_moisture_bar(plants_df, selected_plants)

    st.altair_chart(botanist_plants_pie, use_container_width=True)
    st.altair_chart(temp_bar_chart, use_container_width=True)
    st.altair_chart(temp_line_chart, use_container_width=True)
    st.altair_chart(moist_bar_chart, use_container_width=True)
