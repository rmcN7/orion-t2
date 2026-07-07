import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.title("Orion Fleet Watchlist Dashboard")
st.write("Aircraft from watchlist countries (Russia, Belarus, Syria) currently in the Turkey/Black Sea/Crimea region.")

url = "https://raw.githubusercontent.com/rmcN7/orion-t2/main/outputs/watchlist_flagged.csv"
df = pd.read_csv(url)

m = folium.Map(location=[df["latitude"].mean(), df["longitude"].mean()], zoom_start=6)

# --- REPLACE your old for-loop with this new version ---
for _, row in df.iterrows():
    color = "red" if row["stale_position"] else "green"
    if row["stale_position"]:
        reason = f"Position may be outdated — last real update was {int(row['position_age_seconds'])} seconds before this snapshot."
    else:
        reason = "Position is current as of this snapshot."
    popup_text = f"{row['callsign']} ({row['origin_country']})<br>{reason}"
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=6,
        color=color,
        fill=True,
        popup=popup_text,
    ).add_to(m)
# --- end replacement ---

st_folium(m, width=700, height=500)
