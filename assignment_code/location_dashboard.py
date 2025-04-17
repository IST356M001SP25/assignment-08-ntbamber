'''
location_dashboard.py
'''
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# streamlit layout and title
st.set_page_config(layout="wide")
st.title("Parking Ticket Trends by Location")

# load ticket data for top locations
df = pd.read_csv("./cache/tickets_in_top_locations.csv")

# create dropdown of top locations
locations = df["location"].unique()
selected_location = st.selectbox("Select a location:", sorted(locations))

# filter dataset by selected location
loc_df = df[df["location"] == selected_location]

# get total tickets and total fines
total_tickets = loc_df.shape[0]
total_fines = loc_df["amount"].sum()

# show total tickets and total fines
col1, col2 = st.columns(2)
col1.metric("Total Tickets", f"{total_tickets:,}")
col2.metric("Total Fines", f"${total_fines:,.2f}")

# display day of week distribution
st.subheader("Ticket Count by Day of Week")
dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_counts = loc_df["dayofweek"].value_counts().reindex(dow_order).fillna(0)

fig1, ax1 = plt.subplots()
sns.barplot(x=day_counts.index, y=day_counts.values, ax=ax1)
ax1.set_ylabel("Tickets")
ax1.set_xlabel("Day of Week")
ax1.set_title("Tickets by Day")
st.pyplot(fig1)

# display hour of day distribution
st.subheader("Ticket Count by Hour of Day")
hour_counts = loc_df["hourofday"].value_counts().sort_index()

fig2, ax2 = plt.subplots()
sns.lineplot(x=hour_counts.index, y=hour_counts.values, ax=ax2, marker="o")
ax2.set_xlabel("Hour of Day")
ax2.set_ylabel("Tickets")
ax2.set_title("Tickets by Hour")
st.pyplot(fig2)

# show location on a map
st.subheader("Selected Location on Map")
map_df = loc_df[["lat", "lon"]].dropna().drop_duplicates()
st.map(map_df)