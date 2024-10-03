"""Loads visualisations to constantly running dashboard."""

import pandas as pd
import streamlit as st

from extract_dashboard import extract_readings
from transform_dashboard import create_botanist_pie, create_temperature_bar, create_moisture_bar, create_temperature_line

if __name__ == "__main__":

    plants_df = extract_readings()

    botanist_plants_pie = create_botanist_pie(plants_df)
    temp_bar_chart = create_temperature_bar(plants_df)
    temp_line_chart = create_temperature_line(plants_df)
    moist_bar_chart = create_moisture_bar(plants_df)

    plant_ids = plants_df["plant_id"].unique().tolist()
    st.sidebar.markdown("# Sidebar")
    st.sidebar.multiselect("Trucks", options=plant_ids)

    st.altair_chart(botanist_plants_pie, use_container_width=True)
    st.altair_chart(temp_bar_chart, use_container_width=True)
    st.altair_chart(temp_line_chart, use_container_width=True)
    st.altair_chart(moist_bar_chart, use_container_width=True)


# cols = st.columns(2)
#    with cols[0]:
#         st.altair_chart(total_transactions, use_container_width=True)
#         st.altair_chart(avg_transactions, use_container_width=True)

#    with cols[1]:
#         st.altair_chart(transactions_over_time, use_container_width=True)
#         st.altair_chart(weekday_transactions, use_container_width=True)
