'''
map_dashboard.py
'''
import streamlit as st
import streamlit_folium as sf
import folium
import pandas as pd
import geopandas as gpd
import matplotlib.colors as mcolors
import matplotlib.cm as cm
# these constants should help you get the map to look better
# you need to figure out where to use them
CUSE = (43.0481, -76.1474)  # center of map
ZOOM = 14                   # zoom level
VMIN = 1000                 # min value for color scale
VMAX = 5000                 # max value for color scale

# set Streamlit layout and title
st.set_page_config(layout="wide")
st.title("Map of Top Parking Ticket Locations in Syracuse")

# load the mappable top locations dataset
df = pd.read_csv("./cache/top_locations_mappable.csv")

# initialize a map centered on Syracuse
m = folium.Map(location=CUSE, zoom_start=ZOOM)

# create color normalization and colormap
norm = mcolors.Normalize(vmin=VMIN, vmax=VMAX)
cmap = cm.get_cmap("viridis")

# circle radius and color by fine amount
for _, row in df.iterrows():
    color = mcolors.to_hex(cmap(norm(row["amount"])))
    folium.CircleMarker(
        location=(row["lat"], row["lon"]),
        radius=8,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.8,
        tooltip=f"{row['location']} (${row['amount']:,.0f})"
    ).add_to(m)

# display map in Streamlit
sf.st_folium(m, width=1000, height=700)