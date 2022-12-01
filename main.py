import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import json

poverty_rate_data_path = Path("C:/Users/stapi/Python Pro Bootcamp Data Science Projects/poverty_by_state.csv")
graduation_rate_data_path = Path("C:/Users/stapi/Python Pro Bootcamp Data Science Projects/graduation_by_state.csv")
poverty_graduation_rate_data_path = Path("C:/Users/stapi/Python Pro Bootcamp Data Science "
                                         "Projects/poverty_and_graduation.csv")
state_race_data_path = Path("C:/Users/stapi/Python Pro Bootcamp Data Science Projects/state_race_group.csv")
geojson_data_path = Path("C:/Users/stapi/Python Pro Bootcamp Data Science Projects/gz_2010_us_040_00_500k.json")
state_fatalities_data_path = Path("C:/Users/stapi/Python Pro Bootcamp Data Science Projects/state_fatalities.csv")

poverty_by_state = pd.read_csv(poverty_rate_data_path)
graduation_by_state = pd.read_csv(graduation_rate_data_path)
poverty_and_graduation_comparison = pd.read_csv(poverty_graduation_rate_data_path)
state_race_group = pd.read_csv(state_race_data_path)
df_states_fatalities = pd.read_csv(state_fatalities_data_path)

with open(geojson_data_path) as response:
    states_geojson = json.load(response)

fig_state_poverty = px.bar(poverty_by_state,
                           x="Geographic Area",
                           y="poverty_rate",
                           color="Geographic Area",
                           title="Poverty Rate by State",
                           width=1000, height=550,
                           labels={"Geographic Area": "State", "poverty_rate": "Poverty Rate %"},
                           template="plotly_dark")

fig_state_graduation = px.bar(graduation_by_state,
                              x="Geographic Area",
                              y="percent_completed_hs",
                              color="Geographic Area",
                              title="Graduation Rate by State",
                              width=1000, height=550,
                              labels={"Geographic Area": "State", "percent_completed_hs": "Graduation Rate %"},
                              template="plotly_dark")

fig_poverty_and_graduation = px.line(poverty_and_graduation_comparison,
                                     x="Geographic Area",
                                     y=["poverty_rate", "percent_completed_hs"],
                                     title="Relationship between poverty and Graduation",
                                     width=1000, height=600,
                                     template="plotly_dark",
                                     labels={"Geographic Area": "State",
                                             "value": "Poverty and Graduation %",
                                             "variable": "Poverty - Graduation"})

race_columns = ['share_white', 'share_black', 'share_native_american', 'share_asian', 'share_hispanic']

fig_state_by_race = px.bar(state_race_group,
                           x="Geographic area",
                           y=race_columns,
                           width=1000,
                           height=600,
                           barmode="group",
                           title="Racial Makeup Per State",
                           labels={"Geographic area": "State", "value": "Race Group %", "variable": "Race Share"},
                           template="plotly_dark")

fig_c = px.choropleth(df_states_fatalities,
                      geojson=states_geojson,
                      locations="State_names",
                      color="state",
                      scope="usa",
                      featureidkey="properties.NAME",
                      color_continuous_scale=px.colors.sequential.Reds,
                      title="Fatalities By State",
                      hover_data=["race"],
                      height=600,
                      width=1000)

fig_c.add_scattergeo(geojson=states_geojson,
                     locations=df_states_fatalities["State_names"],
                     text=df_states_fatalities["state"],
                     mode='text',
                     featureidkey="properties.NAME")

st.set_page_config(page_title="Plotly Charts Test", layout="wide")
st.header('USA police Fatality shooting analysis')
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    st.plotly_chart(fig_state_poverty, use_container_width=True)

with col2:
    st.plotly_chart(fig_state_graduation, use_container_width=True)

with col3:
    st.plotly_chart(fig_poverty_and_graduation, use_container_width=True)

with col4:
    st.plotly_chart(fig_state_by_race, use_container_width=True)

with st.container():
    st.plotly_chart(fig_c, use_container_width=True)
