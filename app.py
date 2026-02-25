import streamlit as st
import yaml

st.title("EU AI Act Risk Classifier (Demo)")

use_case = st.text_area("Describe your AI use case")

annex_domains = st.multiselect(
    "Select affected domains",
    ["Employment", "Education", "Healthcare", 
     "Credit scoring", "Law enforcement",
     "Critical infrastructure", "Migration",
     "Justice"]
)

impact = st.checkbox("Does it significantly affect individual rights?")

if st.button("Classify"):

    if "social scoring" in use_case.lower():
        st.error("Unacceptable Risk")
    elif annex_domains and impact:
        st.warning("High Risk")
    elif "chatbot" in use_case.lower():
        st.info("Limited Risk")
    else:
        st.success("Minimal Risk")
