import sqlite3
import streamlit as st
from selenium import webdriver
from time import sleep

options = webdriver.FirefoxOptions()
options.headless = True
driver = webdriver.Firefox(options=options)

##
# Page setup
st.title("Browser History Analysis")

##
# Sqlite statements
get_firefox_history = "SELECT * FROM moz_places"
get_firefox_urls = "SELECT url from moz_places"
get_firefox_titles = "SELECT title from moz_places"
get_chrome_history = "SELECT * FROM urls"
get_chrome_urls = "SELECT url FROM urls"
get_chrome_titles = "SELECT title FROM urls"
get_firefox_visitcount = "SELECT visit_count FROM urls"
get_max_visited_firefox = "SELECT url, MAX(visit_count) FROM moz_places"

try:
    ##
    # Fetch Firefox browser details
    firefox_connection = sqlite3.connect(f"{st.session_state.path}/browsers/firefox.sqlite")
    firefox_cursor = firefox_connection.cursor()
    # Get URLs
    firefox_cursor.execute(get_firefox_urls)
    urls = firefox_cursor.fetchall()
    # Get titles
    firefox_cursor.execute(get_firefox_titles)
    titles = firefox_cursor.fetchall()
    # Get all history
    firefox_cursor.execute(get_firefox_history)
    sites = firefox_cursor.fetchall()
    # Most visited
    firefox_cursor.execute(get_max_visited_firefox)
    maxvis = firefox_cursor.fetchall()

    # Fetch Chrome browser details
    chrome_connection = sqlite3.connect(f"{st.session_state.path}/browsers/chrome.sqlite")
    chrome_cursor = chrome_connection.cursor()
    chrome_cursor.execute(get_chrome_history)
    chrome_sites = chrome_cursor.fetchall()

    # Print Firefox history
    with st.expander("Firefox"):
        for site in sites:
            st.info(f"URL: {site[1]}")
            st.text(f"Title: {site[2]}")
            st.text(f"Visit Count: {site[4]}")
            try:
                driver.get(site[1])
                #sleep(1)
                st.image(driver.get_screenshot_as_png(), width=500)
                #driver.close()
            except:
                continue

    ##
    # Print Chrome history
    with st.expander("Chrome"):
        for chrome_site in chrome_sites:
            st.info(f"URL: {chrome_site[1]}")
            st.write(f"Title: {chrome_site[2]}")
            st.write(f"Visit Count: {chrome_site[3]}")

    # Test

    # Close the connection
    firefox_connection.close()
    chrome_connection.close()

except:
    st.error("No data source specified")


