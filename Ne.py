import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Linguistic Humanizer PRO", page_icon="🧬")
st.title("Linguistic Disruption Humanizer")
st.markdown("---")

api_key = st.text_input("Enter Google API Key:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # 1. We added 'models/' prefix - this is the most common reason for rejection
        # 2. We added the 'gemini-1.5-flash' (standard) and 'gemini-1.0-pro' (backup)
        model_options = [
            "models/gemini-1.5-flash", 
            "models/gemini-1.5-pro", 
            "models/gemini-1.0-pro"
        ]
        
        working_model_name = None
        error_log = []

        # Logic to find which model your specific key is allowed to use
        for m_name in model_options:
            try:
                test_model = genai.GenerativeModel(model_name=m_name)
                # Quick check call
                test_model.generate_content("Hi", generation_config={"max_output_tokens": 1})
                working_model_name = m_name
                break
            except Exception as e:
                error_log.append(f"{m_name}: {str(e)}")
                continue
        
        if not working_model_name:
            st.error("❌ Google is still rejecting the connection.")
            with st.expander("Show Technical Diagnosis"):
                for err in error_log:
                    st.write(err)
            st.info("💡 **PRO TIP:** If you are in the EU/UK, Google often blocks these keys. **Turn on a VPN (set to USA)**, refresh this page, and try again.")
        else:
            st.success(f"✅ Connected! Using: {working_model_name}")
            
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
                    
                    LINGUISTIC RULES:
                    1. MAXIMIZE PERPLEXITY: Avoid predictable word choices. Remove AI words like 'delve' or 'tapestry'.
                    2. MAXIMIZE BURSTINESS: Mix very short sentences with very long ones.
                    3. USE CONTRACTIONS: Use 'don't', 'it's', 'can't'.
                    4. NO FORMAL TRANSITIONS: Avoid 'Moreover', 'Furthermore', 'In conclusion'.
                    
                    TEXT: {text_input}
                    """
                    
                    with st.spinner('Disrupting patterns...'):
                        response = model.generate_content(prompt)
                        st.write(response.text)
                else:
                    st.warning("Please paste some text.")
                
    except Exception as e:
        st.error(f"Setup Error: {e}")
else:
    st.info("Please enter your API Key.")
