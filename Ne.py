import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Linguistic Humanizer", page_icon="🧬")
st.title("Linguistic Disruption Humanizer")

api_key = st.text_input("Enter Google API Key:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # 1. Get the list of ALL models Google says you can use
        all_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # 2. SMART FILTER: Skip the broken "2.5-flash" and find a working one
        # We prefer 1.5-flash (fast) or 1.5-pro (smart)
        target_model = None
        for m in all_models:
            if "gemini-1.5-flash" in m:
                target_model = m
                break
        
        if not target_model:
            for m in all_models:
                if "gemini-1.5-pro" in m:
                    target_model = m
                    break
        
        # Fallback: If 1.5 isn't there, take the first one that ISN'T the broken 2.5
        if not target_model:
            target_model = next((m for m in all_models if "2.5" not in m), all_models[0])

        st.success(f"✅ Connected to Working Model: {target_model}")
        
        model = genai.GenerativeModel(model_name=target_model)
        
        text_input = st.text_area("Paste AI-generated text here:", height=300)

        if st.button("Humanize Text"):
            if text_input:
                # Using your research: Maximize Perplexity and Burstiness
                prompt = f"""
                Rewrite the following text to bypass AI detectors.
                - Use 'Linguistic Disruption': Vary sentence length drastically.
                - Use 'Token Randomization': Avoid predictable AI words (delve, tapestry, multifaceted).
                - Use natural human contractions (don't, it's).
                - Adopt a conversational but professional tone.
                TEXT: {text_input}
                """
                
                with st.spinner('Disrupting statistical patterns...'):
                    # Setting Temperature to 1.0 to increase Perplexity (Surprise)
                    response = model.generate_content(
                        prompt, 
                        generation_config={"temperature": 1.0}
                    )
                    st.subheader("Humanized Output:")
                    st.write(response.text)
            else:
                st.warning("Please paste some text.")
                
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("Check if your USA VPN is still active.")
else:
    st.info("Paste your API Key and keep your USA VPN active.")
