import streamlit as st
import google.generativeai as genai

# UI and Page Configuration
st.set_page_config(page_title="Linguistic Humanizer PRO", page_icon="🧬")
st.title("Linguistic Disruption Humanizer")
st.markdown("---")

# API Key Input
api_key = st.text_input("Enter Google API Key:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # 1. AUTO-LIST MODELS (To avoid 404/429 guessing games)
        models = genai.list_models()
        available_model_names = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
        
        if not available_model_names:
            st.error("No working models found for this key. Check your VPN and key permissions.")
        else:
            # Dropdown for user to pick (Default to Gemini 1.5 Flash if present)
            default_index = 0
            for i, name in enumerate(available_model_names):
                if "gemini-1.5-flash" in name:
                    default_index = i
                    break
            
            selected_model = st.selectbox("Select Model (Use 1.5-Flash for speed):", available_model_names, index=default_index)
            
            # Input Text Area
            text_input = st.text_area("Paste AI-generated text here:", height=300)

            if st.button("Humanize Now"):
                if text_input:
                    # THE FINAL ALGORITHM PROMPT (Updated to be SILENT)
                    prompt = f"""
                    SYSTEM TASK: Rewrite the following text to bypass AI detectors like GPTZero and Turnitin AIR-1. 
                    CRITICAL: PROVIDE ONLY THE REWRITTEN TEXT. DO NOT SHOW YOUR DRAFTING, REFINING, OR THOUGHT PROCESS. 
                    NO HEADERS, NO LABELS, NO EXPLANATIONS. JUST THE RESULT.

                    LINGUISTIC REQUIREMENTS:
                    1. HIGH PERPLEXITY: Use contextually unexpected word choices. Avoid AI cliches (delve, tapestry, pivotal, multifaceted, underscore).
                    2. HIGH BURSTINESS: Create extreme variance in sentence length. Mix 4-word punchy sentences with 30-word complex sentences.
                    3. NATURAL RHYTHM: Use contractions (don't, it's, we're). Use a conversational, tech-savvy human voice.
                    4. REMOVE AI TRANSITIONS: Do not use 'Furthermore', 'Moreover', or 'In conclusion'.
                    
                    INPUT TEXT TO REWRITE:
                    {text_input}
                    """
                    
                    with st.spinner('Disrupting statistical patterns...'):
                        model = genai.GenerativeModel(
                            model_name=selected_model,
                            generation_config={"temperature": 1.0}
                        )
                        response = model.generate_content(prompt)
                        
                        st.subheader("Humanized Result:")
                        st.write(response.text)
                        st.divider()
                        st.info("Tip: If the result looks too 'polished', try adding a specific persona like 'Write like a tired journalist'.")
                else:
                    st.warning("Please paste some text first.")
                
    except Exception as e:
        st.error(f"App Error: {e}")
        st.info("Ensure your USA VPN is active.")
else:
    st.info("1. Connect to USA VPN. \n2. Paste your API Key from aistudio.google.com")
