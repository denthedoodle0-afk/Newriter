import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Linguistic Humanizer PRO", page_icon="🧬")
st.title("Linguistic Disruption Humanizer")
st.markdown("---")

api_key = st.text_input("Enter Google API Key:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        generation_config = {
            "temperature": 1.0, 
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        }

        # CHANGED TO PRO-LATEST FOR BETTER COMPATIBILITY
        model = genai.GenerativeModel(
            model_name="models/gemini-1.5-pro-latest",
            generation_config=generation_config
        )

        text_input = st.text_area("Paste AI-generated text here:", height=300)

        if st.button("Apply Linguistic Disruption"):
            if text_input:
                prompt = f"""
                TASK: Rewrite the following text to bypass deep-learning classifiers.
                
                CORE STATISTICAL DISRUPTIONS:
                1. MAXIMIZE PERPLEXITY: Avoid 'high-probability' word sequences. Remove all AI fingerprints: 'delve', 'tapestry', 'pivotal', 'underscore', 'multifaceted', 'robust'.
                2. MAXIMIZE BURSTINESS: Create extreme variance in sentence length. Use a '4-word punchy sentence' followed by a '30-word complex sentence'.
                3. DISRUPT UNIFORMITY: Use human contractions (it's, don't). Break the subject-verb rhythm.
                4. REMOVE 'POLISHED' SIGNAL: Transition using logic, NOT labels like 'Furthermore' or 'Moreover'.
                5. PERSONA: Write like a tired human expert. Prioritize clarity and voice over perfection.

                INPUT TEXT:
                {text_input}
                """
                
                with st.spinner('Calculating Perplexity Shifts...'):
                    response = model.generate_content(prompt)
                    st.success("Humanized Output:")
                    st.write(response.text)
            else:
                st.warning("Please paste some text first.")
                
    except Exception as e:
        # This will tell us exactly what is wrong if it fails again
        st.error(f"Error: {e}")
else:
    st.info("Please enter your API Key to unlock.")
