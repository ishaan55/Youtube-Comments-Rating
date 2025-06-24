import streamlit as st
import requests

st.set_page_config(page_title="YouTube Comment Rating", layout="centered")
st.title("🎬 YouTube Video Comment Rating")

url = st.text_input("Enter YouTube URL:", "")

if st.button("Rate"):
    if url.strip() == "":
        st.warning("Please enter a YouTube video URL.")
    else:
        try:
            response = requests.post("http://127.0.0.1:5000/rate", json={"url": url})
            if response.status_code == 200:
                data = response.json()
                rating = data["rating"]

                if rating > 0.75:
                    st.success(f"🌟 Excellent - Rating: {rating}")
                elif rating > 0.5:
                    st.info(f"👍 Good - Rating: {rating}")
                elif rating > 0.25:
                    st.warning(f"⚠️ Bad - Rating: {rating}")
                else:
                    st.error(f"💔 Terrible - Rating: {rating}")
            else:
                st.error("Could not get rating. Check the URL.")
        except Exception as e:
            st.error(f"Error: {e}")