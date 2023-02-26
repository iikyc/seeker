import pandas as pd
import streamlit as st
import re
from datetime import datetime

# Page config
st.set_page_config(layout="wide")


## START TEST

# Open the dpkg.log file and read its contents
with open(f'{st.session_state.path}/logs/last.txt', 'r') as f:
    contents = f.read()

# Split the contents into lines
lines = contents.split('\n')

# Create an empty list to store the data
lastlog_data = []

# Loop through the lines and extract the data
for line in lines:
    try:
        time = re.findall("(?<=[0-9]\s)[0-9]{2}:[0-9]{2}", line)[0]
        date_raw = re.findall("(?<=\s)[a-zA-Z]{3}\s+[0-9]{1,2}", line)[0]
        date_obj = datetime.strptime(date_raw, "%b %d")
        date = date_obj.strftime("2023-%m-%d")
        event = line.split()[0] + " " + " ".join(line.split()[-2:])
        type = "users"
        lastlog_data.append([date, time, event, type])
    except:
        continue

users_df = pd.DataFrame(lastlog_data, columns=['date', "time", "event", "type"])

## END TEST
# Open the dpkg.log file and read its contents
with open(f'{st.session_state.path}/logs/dpkg_log.txt', 'r') as f:
    contents = f.read()

# Split the contents into lines
lines = contents.split('\n')

# Create an empty list to store the data
dpkg_data = []

# Loop through the lines and extract the data
for line in lines:
    if line.startswith('2023'):
        parts = line.split()
        date = parts[0]
        time = parts[1]
        event = parts[2] + parts[3] + parts[4]
        type = "dpkg.log"
        dpkg_data.append([date, time, event, type])

# Create a Pandas dataframe from the data
dpkglog_df = pd.DataFrame(dpkg_data, columns=['date', "time", "event", "type"])

# Open the auth.log file and read its contents
with open(f'{st.session_state.path}/logs/auth_log.txt', 'r') as f:
    contents = f.read()

# Split the contents into lines
lines = contents.split('\n')

# Create an empty list to store the data
auth_data = []

time_regex = "[0-9]{2}:[0-9]{2}:[0-9]{2}"

# Loop through the lines and extract the data
for line in lines:
    try:
        date_obj = datetime.strptime(line[:6], "%b %d")
        date = date_obj.strftime("2023-%m-%d")
    except:
        continue
    try:
        time = re.findall(time_regex, line)[0]
    except:
        continue
    event = line[26:]
    type = "auth.log"
    auth_data.append([date, time, event, type])

# Create a Pandas dataframe from the data
authlog_df = pd.DataFrame(auth_data, columns=["date", "time", "event", "type"])
total_df = authlog_df.append(dpkglog_df, ignore_index=True)
total_df = total_df.append(users_df, ignore_index=True)

# Chart placeholder element
timeline_chart = st.empty()

# Search bar
st.subheader("Search")
search_query = st.text_input("")
# Downloads total_df as a .csv file
st.download_button("Download", total_df.to_csv(index=False).encode('utf-8'), "seeker_timline.csv", "text/csv", key='download-csv')

# Columns
col1, col2 = st.columns(2)

# Left column
with col1:
    st.subheader("Options")
    st.selectbox("Chart Type", ["Bar Chart", "Line Chart"])
    source_selection = st.selectbox("Source", ["All", "auth.log", "dpkg.log", "users"])
    
    if source_selection == "All":
        with timeline_chart:
            st.bar_chart(total_df.groupby(['date']).size())
    if source_selection == "auth.log":
        with timeline_chart:
            auth_df = total_df.loc[total_df['type'] == "auth.log"]
            st.bar_chart(auth_df.groupby(['date']).size())
    if source_selection == "dpkg.log":
        with timeline_chart:
            dpkg_df = total_df.loc[total_df['type'] == "dpkg.log"]
            st.bar_chart(dpkg_df.groupby(['date']).size())

# Right column
with col2:
    events_dataframe = st.empty()
    if source_selection == "All":
        with events_dataframe:
            st.dataframe(total_df, width=None, height=None)
        if search_query:
            search_results_df = total_df.loc[total_df['event'].str.contains(search_query, case=False)]
            with events_dataframe:
                st.dataframe(search_results_df)
    if source_selection == "auth.log":
        with events_dataframe:
            auth_df = total_df.loc[total_df['type'] == "auth.log"]
            st.dataframe(auth_df, width=None, height=None)
        if search_query:
            search_results_df = auth_df.loc[auth_df['event'].str.contains(search_query, case=False)]
            with events_dataframe:
                st.dataframe(search_results_df)
    if source_selection == "dpkg.log":
        with events_dataframe:
            dpkg_df = total_df.loc[total_df['type'] == "dpkg.log"]
            st.dataframe(dpkg_df, width=None, height=None)
        if search_query:
            search_results_df = dpkg_df.loc[dpkg_df['event'].str.contains(search_query, case=False)]
            with events_dataframe:
                st.dataframe(search_results_df)
