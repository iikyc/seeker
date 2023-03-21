# Under Development
import streamlit as st
import re
import pandas as pd
##
# Page setup
st.title("Networking Information")

##
# Regular expressions
interface_names_regexp = "^[a-z0-9]+(?=:)"
#interface_names_regexp = "(?<=\n)lo"
ipv4_address_regexp = "(?<=inet\s)[0-9\.]+"
ipv6_address_regexp = "(?<=inet6\s)[0-9a-z:]+"
received_packets_regexp = "(?<=RX\spackets\s)[0-9]+"
transmitted_packets_regexp = "(?<=TX\spackets\s)[0-9]+"
df = pd.DataFrame(columns = ["Received Packets", "Transmitted Packets"])

try:
    ##
    # Reading interfaces.txt
    packages_file = open(f"{st.session_state.path}/system/interfaces.txt", "r")
    package_details = packages_file.read()

    # Searching with RegEx
    interface = re.findall(interface_names_regexp, package_details)
    ipv4address = re.findall(ipv4_address_regexp, package_details)
    ipv6address = re.findall(ipv6_address_regexp, package_details)
    received_packets = re.findall(received_packets_regexp, package_details)
    transmitted_packets = re.findall(transmitted_packets_regexp, package_details)
    ##
    # Outputting the data
    st.subheader(f"Interface: {interface[0]}")
    st.info(f"IPv4 Address: {ipv4address[0]}  \nIPv6 Address: {ipv6address[0]}  "
            f"\nTotal packets received: {received_packets[0]}  \nTotal packets transmitted: {transmitted_packets[0]}")

except FileNotFoundError:
    st.error("No data source specified")

