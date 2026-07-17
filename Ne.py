import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Humanizer", page_icon="✍️")
st.title("My Mobile Humanizer")

# Input for API Key
api_key = st.text_input("Paste Google API Key here:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    text_input = st.text_area("Paste AI text here:", height=200)

    if st.button("Humanize Now"):
        if text_input:
            # The "Humanizing" instructions
            prompt = f"""Rewrite the following text to sound like a natural human wrote it. 
            - Vary sentence lengths significantly.
            - Use a conversational but professional tone.
            - Avoid words like 'delve', 'tapestry', 'comprehensive', 'unlock'.
            - Use contractions (don't, it's, we're).
            - Text to rewrite: {text_input}"""
            
            response = model.generate_content(prompt)
            st.success("Humanized Output:")
            st.write(response.text)
        else:
            st.error("Please paste some text first!")
else:
    st.warning("Please enter your API Key from Google AI Studio to begin.")
