import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Linguistic Humanizer PRO", page_icon="🧬")
st.title("Linguistic Disruption Humanizer")

api_key = st.text_input("Enter Google API Key:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # 1. Ask Google: "What models is this SPECIFIC key allowed to use?"
        models = genai.list_models()
        # Filter for models that actually support writing text
        available_model_names = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
        
        if not available_model_names:
            st.error("No models found for this key. Check your VPN and API settings.")
        else:
            # 2. Let YOU pick the model from a list of what actually exists for you
            st.success(f"Found {len(available_model_names)} working models!")
            selected_model = st.selectbox("Select a model (Try '1.5-flash' first):", available_model_names)
            
            # The "Algorithm" Settings (From your research)
            model = genai.GenerativeModel(
                model_name=selected_model,
                generation_config={
                    "temperature": 1.0,  # Maximize Perplexity (Surprise)
                    "top_p": 0.95,
                    "max_output_tokens": 2048,
                }
            )
            
            text_input = st.text_area("Paste AI-generated text here:", height=300)

            if st.button("Humanize Now"):
                if text_input:
                    # Your scientific prompt for Perplexity and Burstiness
                    prompt = f"""
                    Rewrite this text to bypass AI detectors.
                    - HIGH PERPLEXITY: Use unexpected word choices. Avoid 'delve', 'tapestry', 'pivotal'.
                    - HIGH BURSTINESS: Mix very short (3-5 words) and very long (25-40 words) sentences.
                    - CONTRACTIONS: Use 'don't', 'it's', 'can't'.
                    - STYLE: Conversational human tone.
                    TEXT: {text_input}
                    """
                    
                    with st.spinner('Disrupting statistical patterns...'):
                        response = model.generate_content(prompt)
                        st.subheader("Humanized Output:")
                        st.write(response.text)
                else:
                    st.warning("Please paste some text.")
                
    except Exception as e:
        st.error(f"Connection Error: {e}")
        st.info("Ensure your USA VPN is active. Some models only appear when on a USA IP.")
else:
    st.info("Paste your API Key and keep your USA VPN active.")
