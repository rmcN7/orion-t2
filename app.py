import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.title("Orion Fleet Watchlist Dashboard")
st.write("Aircraft from watchlist countries (Russia, Belarus, Syria) currently in the Turkey/Black Sea/Crimea region.")

url = "https://raw.githubusercontent.com/rmcN7/orion-t2/main/outputs/watchlist_flagged.csv"
df = pd.read_csv(url)

st.sidebar.header("Filters")
selected_countries = st.sidebar.multiselect(
    "Country",
    options=sorted(df["origin_country"].unique()),
    default=sorted(df["origin_country"].unique())
)
show_stale_only = st.sidebar.checkbox("Show only stale positions")

filtered_df = df[df["origin_country"].isin(selected_countries)]
if show_stale_only:
    filtered_df = filtered_df[filtered_df["stale_position"] == True]

if filtered_df.empty:
    st.warning("No aircraft match the selected filters. Try adjusting your selections in the sidebar.")
else:
    m = folium.Map(
        location=[filtered_df["latitude"].mean(), filtered_df["longitude"].mean()],
        zoom_start=6
    )
    for _, row in filtered_df.iterrows():
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

    st_folium(m, width=700, height=500)

    st.subheader("Flagged aircraft details")
    st.dataframe(filtered_df[["callsign", "origin_country", "latitude", "longitude", "stale_position", "position_age_seconds"]])
