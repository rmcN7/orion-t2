import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.title("Orion Fleet Watchlist Dashboard")
st.write("Aircraft from watchlist countries (Russia, Belarus, Syria) currently in the Turkey/Black Sea/Crimea region.")

url = "https://raw.githubusercontent.com/rmcN7/orion-t2/main/outputs/watchlist_flagged.csv"
df = pd.read_csv(url)

m = folium.Map(location=[df["latitude"].mean(), df["longitude"].mean()], zoom_start=6)

for _, row in df.iterrows():
    color = "red" if row["stale_position"] else "green"
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=6,
        color=color,
        fill=True,
        popup=f"{row['callsign']} ({row['origin_country']})",
    ).add_to(m)

st_folium(m, width=700, height=500)
