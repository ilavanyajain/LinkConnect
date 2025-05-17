# app.py
import streamlit as st
from linkedin_bot import LinkedInBot
from filters import filter_profiles
import pandas as pd

st.set_page_config(page_title="LinkedIn Connection Manager", layout="centered")

st.title("LinkedIn Connection Manager")
email = st.text_input("LinkedIn Email")
password = st.text_input("LinkedIn Password", type="password")

if st.button("Fetch Pending Requests"):
    with st.spinner("Logging in & Fetching..."):
        bot = LinkedInBot(email, password)
        profiles = bot.get_pending_requests()
        st.session_state['profiles'] = profiles
        st.success(f"Fetched {len(profiles)} pending requests.")

if 'profiles' in st.session_state:
    profiles = st.session_state['profiles']
    st.write("**Set Filter Criteria:**")
    headline_keywords = st.text_input("Headline keywords (comma-separated)").split(",")
    min_mutual = st.number_input("Minimum mutual connections", min_value=0, value=0)
    if st.button("Filter & Show Matches"):
        filtered = filter_profiles(profiles, [kw.strip() for kw in headline_keywords if kw], min_mutual)
        df = pd.DataFrame(filtered)
        st.dataframe(df)
        if st.button("Accept All Shown"):
            names = [p['name'] for p in filtered]
            bot = LinkedInBot(email, password)
            bot.accept_request(names)
            st.success("Accepted selected connection requests!")