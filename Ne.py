import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Linguistic Humanizer", page_icon="🧬")
st.title("Linguistic Disruption Humanizer")

api_key = st.text_input("Enter Google API Key:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # FORCING THE STABLE MODEL:
        # We avoid 2.0 and 2.5 because Google set your quota for them to 0.
        # gemini-1.5-flash is the most stable free-tier model available.
        target_model = "models/gemini-1.5-flash"
        
        st.success(f"✅ Forced Connection to Stable Model: {target_model}")
        
        model = genai.GenerativeModel(
            model_name=target_model,
            generation_config={
                "temperature": 1.0, # Maximize Perplexity (Surprise)
                "top_p": 0.95,
                "max_output_tokens": 2048,
            }
        )
        
        text_input = st.text_area("Paste AI-generated text here:", height=300)

        if st.button("Humanize Text"):
            if text_input:
                # Engineering the prompt based on your Perplexity/Burstiness research
                prompt = f"""
                TASK: Rewrite the following text to bypass AI detectors.
                
                TECHNIQUE: 
                1. High Perplexity: Use uncommon word pairings and avoid predictable AI phrases.
                2. High Burstiness: Mix 5-word sentences with 30-word complex sentences.
                3. Linguistic Markers: Use contractions (it's, don't, can't) and a conversational but professional voice.
                4. Vocabulary: Eliminate words like 'delve', 'tapestry', 'multifaceted', 'pivotal'.
                
                TEXT TO REWRITE:
                {text_input}
                """
                
                with st.spinner('Applying statistical disruption...'):
                    response = model.generate_content(prompt)
                    st.subheader("Humanized Output:")
                    st.write(response.text)
            else:
                st.warning("Please paste some text.")
                
    except Exception as e:
        if "429" in str(e):
            st.error("Quota Error: Google is still limiting this API key. Try creating a NEW API key in a brand new project at aistudio.google.com while your VPN is ALREADY turned on.")
        else:
            st.error(f"Error: {e}")
else:
    st.info("Paste your API Key and keep your USA VPN active.")
