import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Linguistic Humanizer", page_icon="🧬")
st.title("Linguistic Disruption Humanizer")

# Input for API Key (Accepts AQ or AIza)
api_key = st.text_input("Paste Google API Key:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # Step 1: Try to fetch models
        try:
            models = genai.list_models()
            available_models = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
            
            if not available_models:
                st.error("❌ Key connected, but NO models found.")
                st.info("This happens if the 'Generative Language API' is disabled in your Google Cloud Console for this project.")
            else:
                # Step 2: Auto-select the best available model
                # We search for Flash, then Pro, then anything else
                target_model = next((m for m in available_models if "flash" in m), 
                               next((m for m in available_models if "pro" in m), 
                               available_models[0]))
                
                st.success(f"✅ Connected to: {target_model}")
                
                model = genai.GenerativeModel(model_name=target_model)
                
                text_input = st.text_area("Paste AI-generated text here:", height=300)

                if st.button("Humanize Text"):
                    if text_input:
                        prompt = f"Rewrite this text to sound like a human wrote it. Vary sentence length and use natural rhythm. Text: {text_input}"
                        with st.spinner('Processing...'):
                            response = model.generate_content(prompt)
                            st.write(response.text)
                    else:
                        st.warning("Please enter text.")
                        
        except Exception as e:
            st.error(f"❌ Connection Failed: {e}")
            st.info("Check if your USA VPN is active. If you are in a restricted region, Google blocks the model list.")

    except Exception as e:
        st.error(f"Setup Error: {e}")
else:
    st.info("1. Keep USA VPN ON. \n2. Paste your API Key above.")
