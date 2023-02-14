import streamlit as st
import pandas as pd
import re
import csv
import sqlite3
import time

##
# Page setup
st.title("Incidents Timeline")
st.sidebar.subheader("Visualization Options")
graph_data_source = st.sidebar.selectbox("Data source", ("Logs", "Web Activity"))
graph_type = st.sidebar.selectbox("Graph type", ("Bar Chart", "Line Graph"))

global df

##
# Regular expressions
date_regexp = "^[a-zA-Z]{3}\s{2}[0-9]"
time_regexp = "[0-9]{2}:[0-9]{2}:[0-9]{2}"
incident_regexp = "(?<=:\W)[a-zA-Z0-9\W]+(?=\n)"
try:
    ##
    # Incidents file
    # Transform auth_log.txt to a csv file
    with open('incidents.csv', mode='w') as incidents_file:
        auth_log_file = open(f"{st.session_state.path}/logs/auth_log.txt", "r")
        fieldnames = ['date', 'time', 'incident']
        writer = csv.DictWriter(incidents_file, fieldnames=fieldnames)
        writer.writeheader()
        for line in auth_log_file:
            writer.writerow({'date': re.search(date_regexp, line).group(0), 'time': re.search(time_regexp, line).group(0), 'incident': re.search(incident_regexp, line).group(0)})

    main_log_file = open("incidents.csv", "r")
    get_firefox_history = "SELECT * FROM moz_places"
    get_chrome_history = "SELECT * FROM urls"

    df = pd.read_csv(main_log_file)
    df = df.set_index("time")

    ##
    # Outputting the graphs
    if graph_type == "Bar Chart" and graph_data_source == "Logs":
        chart = st.bar_chart(df.groupby(['date']).count())
    if graph_type == "Line Graph" and graph_data_source == "Logs":
        chart = st.line_chart(df.groupby(['date']).count())

    left_column, right_column = st.columns(2)

    ##
    # Print the log file
    with left_column:
        st.info("Logs")
        st.write(df)

    ##
    # Print web activity
    with right_column:
        st.info("Web Activity")
        # Fetch Chrome browser details
        firefox_connection = sqlite3.connect(f"{st.session_state.path}/browsers/firefox.sqlite")
        firefox_cursor = firefox_connection.cursor()
        firefox_cursor.execute(get_firefox_history)
        firefox_sites = firefox_cursor.fetchall()

        browser_history_df = pd.DataFrame(columns=['date', 'incident'])

        # Creating a pandas dataframe from the sqlite database
        for firefox_site in firefox_sites:
            try:
                if type(firefox_site[8]) == "NoneType":
                    continue
                else:
                    browser_history_df = browser_history_df.append(
                        {'date': time.strftime('%b %d', time.localtime(firefox_site[8])), 'incident': firefox_site[1]},
                        ignore_index=True)
            except Exception as e:
                #st.write(e)
                continue
        # Close the connection
        firefox_connection.close()

        # Fetch Chrome browser details
        chrome_connection = sqlite3.connect(f"{st.session_state.path}/browsers/chrome.sqlite")
        chrome_cursor = chrome_connection.cursor()
        chrome_cursor.execute(get_chrome_history)
        chrome_sites = chrome_cursor.fetchall()

        # Appending to the previous dataframe
        for chrome_site in chrome_sites:
            browser_history_df = browser_history_df.append(
                {'date': time.strftime('%b %d', time.localtime(chrome_site[5])), 'incident': chrome_site[1]},
                ignore_index=True)

        # Close the connection
        chrome_connection.close()
        # Print the dataframe
        st.write(browser_history_df)

    ##
    # Outputting the graphs
    if graph_type == "Bar Chart" and graph_data_source == "Web Activity":
        chart = st.bar_chart(browser_history_df.groupby(['date']).count())
    if graph_type == "Line Graph" and graph_data_source == "Web Activity":
        chart = st.line_chart(browser_history_df.groupby(['date']).count())

except FileNotFoundError:
    st.error("No data source specified")