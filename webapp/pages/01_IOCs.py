import streamlit as st
import vt
import re
import yara
import os
from dotenv import load_dotenv

load_dotenv()
##
# Page setup
st.set_page_config(
    page_title="Seeker Dashboard",
    layout="wide"
)
st.title("IOC Analysis")
genre = st.sidebar.radio("Data source",("Files", "Executables", "Packages"))

##
# Regular expressions
filename_regexp = "(?<=\s)[0-9\/a-z_A-Z\.-]+(?=\n)"
hash_regexp = '[a-zA-Z0-9]+'

try:
    ##
    # File hash analysis
    if genre == "Files":
        # Page setup
        st.subheader("File Hash Analysis")
        start_file_analysis_button = st.button("Start File Analysis")
        # Start analysis
        if start_file_analysis_button:
            progress = st.info("Analyzing file hashes..")
            # Read hashes file
            hashes_file = open(f"{st.session_state.path}/files/hashes.txt", "r")
            hashes = hashes_file.readlines()
            for hash in hashes:
                # API Key
                client = vt.Client(os.getenv("VTKEY"))
                # Start API calls
                try:
                    file = client.get_object(f"/files/{re.search(hash_regexp, hash).group(0)}")
                    if file.last_analysis_stats["malicious"] > 0:
                        st.error(f"Path: {re.search(filename_regexp, hash).group(0)}")
                        st.write(f"Hash: {re.search(hash_regexp, hash).group(0)}")
                        st.write(f"Reported as malicious: {file.last_analysis_stats['malicious']} times")
                        with st.expander("Details"):
                            st.info("Aliases")
                            for alias in file.names:
                                st.write(alias)
                except:
                    pass
                client.close()
            progress.empty()
            st.success("Analysis done")

    ##
    # Pre-processed, possible IOC from executable files
    if genre == "Executables":
        # Page setup
        st.subheader("Executables")
        # Columns
        col1, col2 = st.columns(2)

        # Read IOC file
        executables_file = open(f"{st.session_state.path}/files/ioc.txt")
        files = executables_file.readlines()
        # Print out IOC file
        #for line in files:
            #if line.startswith("FILE:"):
                #st.info(line.replace("FILE:",""))
            #else:
                #st.write(line)
        with col1:
            rule = st.text_area("YARA Rule")
            run_yara = st.button("Run")
        if run_yara:
            with col2:
                executables_file = open(f"{st.session_state.path}/files/ioc.txt")
                lines = executables_file.readlines()
                yara_regex = "^[^FILE].*"
                for line in lines:
                    #st.write(re.findall(line, yara_regex))
                    pass
                # string to be checked against YARA rule
                string = "This is an example string."

                # compile YARA rule
                rules = yara.compile(source=rule)

                # apply YARA rule to the string
                matches = rules.match(data=string)

                # check if the string matches the YARA rule
                if len(matches) > 0:
                    st.error("The string matches the YARA rule.")
                else:
                    st.success("The string does not match the YARA rule.")


    ##
    # Installed packages
    if genre == "Packages":
        # Page setup
        st.subheader("Packages")
        # Read packages file
        packages_file = open(f"{st.session_state.path}/system/packages.txt", "r")
        package_details = packages_file.readlines()
        # Print packages file
        for package_detail in package_details:
            st.write(package_detail)

except FileNotFoundError:
    st.error("No data source specified")