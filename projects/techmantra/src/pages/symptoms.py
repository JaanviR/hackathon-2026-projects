import streamlit as st
from streamlit_mic_recorder import speech_to_text

def show():
    # 1. Initialize Transcript State (Exactly like your working project)
    if "transcript" not in st.session_state:
        st.session_state.transcript = ""

    user_profile = st.session_state.get('user_profile', {})
    user_name = user_profile.get('name', 'Patient')
    
    st.title("🌡️ Symptom Checker")
    st.markdown(f"Hello **{user_name}**, please describe what you are experiencing.")

    with st.container(border=True):
        st.subheader("Current Distress")
        
        # 2. Voice Input Section (Your specific working implementation)
        st.write("🎤 **Record Symptoms:**")
        captured_speech = speech_to_text(
            language='en', 
            start_prompt="Click to Record", 
            stop_prompt="Stop & Transcribe", 
            key='biomistral_mic' # Using your specific key
        )

        # The logic that fixed it before: if speech is caught, save and force rerun
        if captured_speech and captured_speech != st.session_state.transcript:
            st.session_state.transcript = captured_speech
            st.rerun()

        # 3. Text Confirmation Area
        # The 'value' is locked to the session_state transcript
        user_input = st.text_area(
            "Describe your symptoms in detail:",
            value=st.session_state.transcript,
            height=150,
            placeholder="Type or use the mic to describe symptoms..."
        )
        # Sync manual typing back to the transcript state
        st.session_state.transcript = user_input

        # 4. Vital Triage Data (Your existing sliders)
        col1, col2 = st.columns(2)
        with col1:
            severity = st.select_slider(
                "Pain Severity",
                options=["Mild", "Moderate", "Severe", "Unbearable"]
            )
        with col2:
            duration = st.selectbox(
                "How long has this been happening?",
                ["Just started", "A few hours", "1-2 days", "More than a week"]
            )

    # 5. Action Button
    if st.button("Analyze with AI", type="primary", use_container_width=True):
        raw_text = st.session_state.transcript.strip()
        
        if not raw_text:
            st.warning("Please provide symptoms to analyze.")
        else:
            # Check for valid input before passing to AI
            has_vowels = any(c in "aeiouAEIOU" for c in raw_text)
            if len(raw_text) < 5 or not has_vowels:
                 st.error("⚠️ Please provide a clearer description of your symptoms.")
            else:
                st.session_state.current_symptoms = raw_text
                st.success("Symptoms saved! Ready for BioMistral analysis.")

    # 6. Reset Option
    if st.button("🔄 Clear All Input"):
        st.session_state.transcript = ""
        st.rerun()