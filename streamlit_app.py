import streamlit as st
from plot import ggscatter
import pandas as pd
import nfl_data_py as nfl

# Set page config
st.set_page_config(page_title="Air Yards vs Yards After Catch", page_icon=":football:", theme="light")

#Import data

pbp = nfl.import_pbp_data([2023])
pbp = pd.DataFrame(pbp)

# Define the list of teams (replace with actual team list)
teams_list = pbp['posteam'].unique().tolist()

st.title('Air Yards vs Yards After Catch, play-by-play NFL Team Comparison')

# Team selectors
team1 = st.selectbox('Select Team 1:', teams_list)
team2 = st.selectbox('Select Team 2:', teams_list)

# Button to generate plot
if st.button('Compare Teams'):
    # Filter the data for the selected teams
    filtered_data = pbp[pbp['posteam'].isin([team1, team2])]
    
    # Generate the scatter plot
    fig = ggscatter('air_yards', 'yards_after_catch', filtered_data, hue='posteam', reference='Fit')

    # Display the plot
    st.pyplot(fig)
