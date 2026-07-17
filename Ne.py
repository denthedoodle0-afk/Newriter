import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Linguistic Humanizer PRO", page_icon="🧬")
st.title("Linguistic Disruption Humanizer")
st.markdown("---")

api_key = st.text_input("Enter Google API Key:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # We will try these models in order. Latest versions first.
        model_options = [
            "gemini-1.5-flash-latest", 
            "gemini-1.5-pro-latest", 
            "gemini-1.5-flash-002"
        ]
        
        # Test which one works
        working_model_name = None
        for m_name in model_options:
            try:
                test_model = genai.GenerativeModel(model_name=m_name)
                # A tiny test call to see if the model is actually available
                test_model.generate_content("Hi", generation_config={"max_output_tokens": 1})
                working_model_name = m_name
                break
            except:
                continue
        
        if not working_model_name:
            st.error("Google is rejecting all standard models for this API key. Please check if your API key is restricted or create a new one at aistudio.google.com")
        else:
            st.caption(f"✅ Connected via: {working_model_name}")
            
            generation_config = {
                "temperature": 1.0, 
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 2048,
            }

            model = genai.GenerativeModel(
                model_name=working_model_name,
                generation_config=generation_config
            )

            text_input = st.text_area("Paste AI-generated text here:", height=300)

            if st.button("Apply Linguistic Disruption"):
                if text_input:
                    prompt = f"""
                    TASK: Rewrite the following text to bypass deep-learning classifiers.
                    
                    CORE STATISTICAL DISRUPTIONS:
                    1. MAXIMIZE PERPLEXITY: Avoid 'high-probability' word sequences. Remove AI fingerprints like 'delve', 'tapestry', 'pivotal', 'underscore'.
                    2. MAXIMIZE BURSTINESS: Force sentence length variance (Extreme mix of very short and very long sentences).
                    3. DISRUPT UNIFORMITY: Use human contractions. Break the subject-verb rhythm.
                    4. REMOVE 'POLISHED' SIGNAL: Do not use formal transition words.
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
        st.error(f"Critical Error: {e}")
else:
    st.info("Enter your API Key to unlock.")
