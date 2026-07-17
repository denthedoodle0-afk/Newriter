import streamlit as st
import google.generativeai as genai

# UI and Page Configuration
st.set_page_config(page_title="Linguistic Humanizer PRO", page_icon="🧬")
st.title("Linguistic Disruption Humanizer")
st.markdown("---")
st.caption("Engineered to bypass statistical classifiers (Turnitin AIR-1, GPTZero, Copyleaks).")

# API Key Input
api_key = st.text_input("Enter Google API Key:", type="password")

if api_key:
    try:
        # Configure the AI engine
        genai.configure(api_key=api_key)
        
        # ALGORITHM SETTINGS:
        # Temperature 1.0 maximizes Perplexity (predictability disruption).
        # Top_p and Top_k settings force wider token distribution.
        generation_config = {
            "temperature": 1.0, 
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        }

        # FIXED: Added 'models/' prefix to solve google.api_core.exceptions.NotFound
        model = genai.GenerativeModel(
            model_name="models/gemini-1.5-flash",
            generation_config=generation_config
        )

        # Input Area
        text_input = st.text_area("Paste AI-generated text here:", height=300, placeholder="Enter text to disrupt...")

        if st.button("Apply Linguistic Disruption"):
            if text_input:
                # Optimized prompt based on Perplexity/Burstiness research
                prompt = f"""
                TASK: Rewrite the following text to bypass deep-learning classifiers.
                
                CORE STATISTICAL DISRUPTIONS:
                1. MAXIMIZE PERPLEXITY: Purposely avoid 'high-probability' token sequences. Use contextually rare but natural synonyms. Remove all AI fingerprints: 'delve', 'tapestry', 'pivotal', 'underscore', 'multifaceted', 'robust', 'leverage'.
                
                2. MAXIMIZE BURSTINESS: Create extreme variance in sentence length. Break the even cadence of AI. Use a '4-word punchy sentence' followed immediately by a '30-word complex sentence' using appositive phrases.
                
                3. DISRUPT UNIFORMITY: AI text has a consistent subject-verb rhythm. Break this. Use fragments, varied connectors, and shift the token distribution by using human contractions (it's, don't, we're).
                
                4. REMOVE 'POLISHED' SIGNAL: Detectors flag clean, organized prose. Transition using logic and flow, NOT labels. Absolutely NO 'Furthermore', 'Moreover', 'In conclusion', or 'Notably'. 
                
                5. PERSONA: Write like a highly educated human expert who is writing in a hurry. Prioritize clarity and voice over 'robotic perfection'.

                INPUT TEXT:
                {text_input}
                """
                
                with st.spinner('Calculating Perplexity Shifts...'):
                    response = model.generate_content(prompt)
                    st.success("Humanized Output:")
                    st.write(response.text)
                    st.divider()
                    st.info("Strategy: Statistical Randomness (Temp 1.0) + Forced Burstiness + Persona Shift.")
            else:
                st.warning("Please paste some text first.")
                
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Please enter your API Key to unlock the humanizer. Get a free key at aistudio.google.com")
