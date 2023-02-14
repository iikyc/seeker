import streamlit as st
import re

##
# Page setup
st.title("Log Analysis")

##
# Regular expressions
date_regexp = "([a-zA-Z]{3}\W\W[0-9]{,2}\W[0-9]{,2})"
log_entry_time_regexp = "[0-9]{2}:[0-9]{2}:[0-9]{2}"
event_regexp = "(?<=:\s).*"

try:
    ##
    # Printing preprocessed auth_log.txt
    with st.expander("auth.log"):
        with open(f"{st.session_state.path}/logs/auth_log.txt") as authlog_file:
            for line in authlog_file:
                #st.write(re.search(date_regexp, line).group(1))
                #st.write(re.search(log_entry_time_regexp, line).group(0))
                st.write(f"{re.search(date_regexp, line).group(1)} - {re.search(log_entry_time_regexp, line).group(0)}")
                st.info(re.search(event_regexp, line).group(0))

except FileNotFoundError:
    st.error("No data source specified")