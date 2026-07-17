import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Linguistic Humanizer", page_icon="🧬")
st.title("Linguistic Disruption Humanizer")

api_key = st.text_input("Enter Google API Key:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # We are using 'gemini-pro' and 'gemini-flash' 
        # Sometimes removing 'models/' and the version numbers helps bypass the 404
        model_options = [
            "gemini-1.5-flash", 
            "gemini-pro",
            "models/gemini-1.5-flash",
            "models/gemini-pro"
        ]
        
        working_model_name = None
        for m_name in model_options:
            try:
                model = genai.GenerativeModel(model_name=m_name)
                # Test call
                model.generate_content("Hi", generation_config={"max_output_tokens": 1})
                working_model_name = m_name
                break
            except:
                continue

        if not working_model_name:
            st.error("❌ Still getting 404.")
            st.warning("🚨 **MANDATORY STEP:** You must use a VPN set to **USA**.")
            st.info("Your current IP address is in a region (EU/UK) where Google blocks the 'GenerateContent' method for these models. Once your VPN is on, refresh this page.")
        else:
            st.success(f"✅ Connected via: {working_model_name}")
            
            text_input = st.text_area("Paste AI text here:", height=300)

            if st.button("Humanize Text"):
                if text_input:
                    # Best instructions based on your research
                    prompt = f"Rewrite this text to have high perplexity and burstiness. Use varied sentence lengths and natural human contractions. Avoid AI words like 'delve' or 'tapestry'. Text: {text_input}"
                    response = model.generate_content(prompt)
                    st.write(response.text)
                else:
                    st.warning("Please paste text.")

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Paste your API key to begin.")
