import json 
import streamlit as st
import pandas as pd
from mplsoccer import VerticalPitch

# App Title and Description
st.title('Euros 2024 Shot Map')
st.markdown("""
Welcome to the **Euros 2024 Shot Map** app! This interactive tool allows you to explore shot data from the UEFA Euro 2024 tournament. 
You can filter the data by team and player to visualize their shot locations, expected goals (xG), and outcomes (goals or misses).
""")

# Load Data
df = pd.read_csv('https://raw.githubusercontent.com/mckayjohns/youtube-videos/refs/heads/main/streamlit/euros_2024_shot_map.csv')
df = df[df['type'] == 'Shot'].reset_index(drop=True)
df['location'] = df['location'].apply(json.loads)

# Sidebar for Filters
st.sidebar.header('Filters')
team = st.sidebar.selectbox('Select a Team', df['team'].sort_values().unique(), index=None)
player = st.sidebar.selectbox('Select a Player', df[df['team'] == team]['player'].sort_values().unique(), index=None) if team else None

# Function to Filter Data
def filter_data(df, team, player):
    if team:
        df = df[df['team'] == team]
    if player:
        df = df[df['player'] == player]
    return df

filtered_df = filter_data(df, team, player)

# Plot Shots
pitch = VerticalPitch(pitch_type='statsbomb', half=True)
fig, ax = pitch.draw(figsize=(10, 10))

def plot_shots(df, ax, pitch):
    for x in df.to_dict(orient='records'):
        pitch.scatter(
            x=float(x['location'][0]),
            y=float(x['location'][1]),
            ax=ax,
            s=1000 * x['shot_statsbomb_xg'],
            color="red" if x['shot_outcome'] == 'Goal' else 'white',
            edgecolors='black',
            alpha=1 if x['shot_outcome'] == 'Goal' else 0.5,
            zorder=2 if x['shot_outcome'] == 'Goal' else 1
        )

if not filtered_df.empty:
    plot_shots(filtered_df, ax, pitch)
    st.pyplot(fig)
else:
    st.write("No data available for the selected filters.")

# Display Key Metrics
if team and player:
    st.subheader(f'Performance Summary for {player} ({team})')
    total_shots = df[(df['team'] == team) & (df['player'] == player)].shape[0]
    total_goals = df[(df['team'] == team) & (df['player'] == player) & (df['shot_outcome'] == 'Goal')].shape[0]
    st.metric(label="Total Shots", value=total_shots)
    st.metric(label="Total Goals", value=total_goals)
    if total_shots > 0:
        st.metric(label="Conversion Rate", value=f"{(total_goals / total_shots * 100):.1f}%")
else:
    st.write("Please select a team and player to see their performance metrics.")

# Additional Information
st.sidebar.markdown("""
### How to Use This App
1. **Select a Team**: Choose a team from the dropdown menu.
2. **Select a Player**: Once a team is selected, choose a player from that team.
3. **Explore Data**: The shot map and performance metrics will update based on your selections.

### Data Source
The data used in this app is sourced from [McKay Johns' GitHub repository](https://github.com/mckayjohns/youtube-videos).
""")
