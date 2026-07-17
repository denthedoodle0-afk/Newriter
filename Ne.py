import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Linguistic Humanizer PRO", page_icon="🧬")
st.title("Linguistic Disruption Humanizer")
st.markdown("---")

api_key = st.text_input("Enter Google API Key:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # --- AUTO-DETECT MODEL SECTION ---
        # This part asks Google: "Which models can I actually use?"
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Try to find 'flash' first (it's fast), then 'pro', otherwise take the first one available
        target_model = ""
        for m in available_models:
            if "1.5-flash" in m:
                target_model = m
                break
        if not target_model:
            for m in available_models:
                if "1.5-pro" in m:
                    target_model = m
                    break
        if not target_model:
            target_model = available_models[0]
            
        st.caption(f"Connected to: {target_model}")
        # ---------------------------------

        generation_config = {
            "temperature": 1.0, 
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        }

        model = genai.GenerativeModel(
            model_name=target_model,
            generation_config=generation_config
        )

        text_input = st.text_area("Paste AI-generated text here:", height=300)

        if st.button("Apply Linguistic Disruption"):
            if text_input:
                prompt = f"""
                TASK: Rewrite the following text to bypass deep-learning classifiers.
                
                CORE STATISTICAL DISRUPTIONS:
                1. MAXIMIZE PERPLEXITY: Avoid 'high-probability' word sequences. Remove AI fingerprints like 'delve', 'tapestry', 'pivotal'.
                2. MAXIMIZE BURSTINESS: Force sentence length variance (Short-Long-Short).
                3. DISRUPT UNIFORMITY: Use human contractions. Break the subject-verb rhythm.
                4. REMOVE 'POLISHED' SIGNAL: No 'Furthermore' or 'Moreover'.
                5. PERSONA: Write like a tired human expert.

                INPUT TEXT:
                {text_input}
                """
                
                with st.spinner('Disrupting statistical patterns...'):
                    response = model.generate_content(prompt)
                    st.success("Humanized Output:")
                    st.write(response.text)
            else:
                st.warning("Please paste some text first.")
                
    except Exception as e:
        st.error(f"Connection Error: {e}")
        st.info("Tip: If you are in the EU/UK, some models are restricted. This app is trying to find an alternative for you.")
else:
    st.info("Enter your API Key to unlock.")
