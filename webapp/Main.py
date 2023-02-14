import re
import streamlit as st

##
# Page setup
st.set_page_config(
    page_title="Seeker Dashboard",
    layout="wide"
)
st.title("Seeker Dashboard")

##
# Save path to data directory in a session variable
try:
    st.session_state.path = st.sidebar.text_input("Data directory", value=st.session_state.path)
except:
    st.session_state.path = st.sidebar.text_input("Data directory")

##
# Regular expressions
os_name_regexp = "(?<=NAME=\")[\w\W]+(?=\")"
os_version_regexp = "(?<=VERSION=\")[\w\W]+(?=\")"
all_users_regexp = "^[a-zA-Z0-9]+"
login_users_regexp = "(^[a-zA-Z0-9]+).*\/bin\/bash$"
nologin_users_regexp = "(^[a-zA-Z0-9]+).*[^\/bin\/bash]$"

##
# Open the data directory and it's files
if st.session_state.path:
    st.sidebar.success("Path set to: " + st.session_state.path)
    # Print execution log of Seeker
    with open(f"{st.session_state.path}/log.txt") as log_file:
        for line in log_file:
            st.info(line)
    ##
    # Read system information files
    f = open(f"{st.session_state.path}/system/system_information.txt", "r")
    os_file = open(f"{st.session_state.path}/system/operating_system.txt", "r")
    os_details = os_file.readlines()
    # Print system information
    with st.expander("System Information"):
        st.write(f"Operating System: {re.search(os_name_regexp, os_details[0]).group(0)}")
        st.write(f"Operating System Version: {re.search(os_version_regexp, os_details[1]).group(0)}")
        st.write(f"Data collected as: {f.readline()}")
        st.write(f"Hostname: {f.readline()}")
        st.write(f"Timezone: {f.readline()}")
        st.write(f"Uptime: ")
    # Print users
    with st.expander("Users"):
        option = st.selectbox('Shell',("All Users", 'Login', "No Login"))
        with open(f"{st.session_state.path}/system/users.txt") as users_file:
            # Filtering users based on shell
            for line in users_file:
                if option == "All Users" and re.match(all_users_regexp, line):
                    st.write(f"{re.findall(all_users_regexp, line)[0]}")

                if option == "Login" and re.match(login_users_regexp, line):
                    st.write(f"{re.findall(login_users_regexp, line)[0]}")

                if option == "No Login" and re.match(nologin_users_regexp, line):
                    st.write(f"{re.findall(nologin_users_regexp, line)[0]}")

else:
    st.sidebar.warning("No path specified")

