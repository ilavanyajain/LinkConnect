import subprocess
try:
    subprocess.run(["playwright", "install", "chromium"], check=True)
except Exception as e:
    print("Playwright browser install failed:", e)

import streamlit as st
from linkedin_bot import LinkedInBot
import pandas as pd
import re

def safe_mutual_count(mc):
    try:
        numbers = re.findall(r'(\d+)', mc)
        return int(numbers[-1]) if numbers else 0
    except:
        return 0

def filter_profiles(profiles, headline_keywords=[], min_mutual=0):
    result = []
    for p in profiles:
        headline = p.get('headline', '').lower()
        if (not headline_keywords or any(kw.strip().lower() in headline for kw in headline_keywords if kw.strip())) and safe_mutual_count(p['mutual_connections']) >= min_mutual:
            result.append(p)
    return result

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
    st.write("Fetched profiles (raw):")
    st.dataframe(profiles)
    st.write("**Set Filter Criteria:**")
    headline_keywords = st.text_input("Headline keywords (comma-separated)").split(",")
    min_mutual = st.number_input("Minimum mutual connections", min_value=0, value=0)
    if st.button("Filter & Show Matches"):
        keywords = [kw.strip() for kw in headline_keywords if kw.strip()]
        filtered = filter_profiles(profiles, keywords, min_mutual)
        df = pd.DataFrame(filtered)
        # Create clickable LinkedIn profile links (Streamlit native HTML rendering)
        if not df.empty:
            # Streamlit's dataframe doesn't support clickable links; use HTML table
            def make_link(row):
                url = row['profile_url']
                name = row['name']
                return f'<a href="{url}" target="_blank">{name}</a>'
            df['name'] = df.apply(make_link, axis=1)
            st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
        else:
            st.write("No matches found.")
        if st.button("Accept All Shown"):
            urls = [p['profile_url'] for p in filtered]
            st.write("Debug - URLs to accept:", urls)  # Debug line
            bot = LinkedInBot(email, password)
            accepted_count = bot.accept_request(urls)
            st.success(f"Successfully accepted {accepted_count} out of {len(urls)} connection requests!")