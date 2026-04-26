import streamlit as st
import json
import pandas as pd
from datetime import datetime
from db.db import save_diagnostic_report, get_recent_sessions

# --- NEW INTEGRATION IMPORTS ---
from integrations.notifications import send_summary
from integrations.calendar_api import book_appointment

def show():
    patient_id = st.session_state.get('patient_id')

    # --- FIX: AUTO-LOAD PREVIOUS RECORD IF STATE IS EMPTY ---
    if not st.session_state.get('diagnosis'):
        if patient_id:
            recent = get_recent_sessions(patient_id, limit=1)
            if recent:
                entry = recent[0]
                st.session_state.diagnosis = json.loads(entry['diagnosis'])
                st.session_state.session_id = entry['id']
                st.session_state.severity = entry['risk_tier']
                st.session_state.current_symptoms = entry['symptoms']
            else:
                st.warning("Please run the symptom checker first.")
                if st.button("Go Back"):
                    st.session_state.current_page = "Symptoms"
                    st.rerun()
                return
        else:
            st.error("Please log in to view results.")
            return

    diag = st.session_state.diagnosis
    risk = diag.get('risk_tier', 'LOW').upper()
    session_id = st.session_state.get('session_id')
    user_profile = st.session_state.get('user_profile', {})

    # 1. Display Risk Banners
    if risk == "HIGH":
        st.error("🚨 **EMERGENCY: Please seek immediate medical attention.**")
    elif risk == "MEDIUM":
        st.warning("⚠️ **MEDIUM RISK: Professional follow-up is recommended.**")
    else:
        st.success("✅ **LOW RISK: Manage symptoms at home and monitor.**")

    st.title("📋 Diagnostic Report")

    # --- UPDATED: TRIGGER AUTOMATION INTEGRATIONS ---
    
    # A. Send Email Notification
    if not st.session_state.get('email_sent'):
        with st.spinner("📧 Sending clinical summary to your provider..."):
            email_success = send_summary(user_profile, diag, risk)
            if email_success:
                st.session_state['email_sent'] = True
                st.toast("Summary sent to your doctor.")

    # B. Interactive Appointment Booking (Only for MEDIUM risk)
    if risk == "MEDIUM":
        st.divider()
        st.subheader("📅 Schedule Follow-up Appointment")
        
        if not st.session_state.get('appointment_booked'):
            from db.db import get_patient_full_context, save_appointment
            from integrations.calendar_api import get_doctor_availability, book_appointment
            
            # --- DEFINE ALL VARIABLES FIRST ---
            ctx = get_patient_full_context(patient_id)
            physician_data = ctx.get("physician", {})
            
            doctor_email = physician_data.get("email")
            patient_email = user_profile.get("email")
            patient_name = user_profile.get("name", "Patient")

            if doctor_email:
                # 1. Fetch available slots
                if 'available_slots' not in st.session_state:
                    with st.spinner("Checking doctor availability..."):
                        st.session_state.available_slots = get_doctor_availability(doctor_email)

                if st.session_state.available_slots:
                    st.write(f"Dr. {physician_data.get('doctor_name')} is free at the following times:")
                    
                    # 2. Patient selects a slot
                    selected_slot = st.selectbox(
                        "Pick a time that works for you:",
                        options=st.session_state.available_slots,
                        format_func=lambda x: datetime.fromisoformat(x).strftime("%A, %b %d at %I:%M %p")
                    )
                    
                    if st.button("Confirm Appointment", type="primary"):
                        # Double check we have the patient email before calling the API
                        if not patient_email:
                            st.error("Your email is missing from your profile. Please re-login.")
                        else:
                            with st.spinner("Booking..."):
                                result = book_appointment(
                                    doctor_email=doctor_email,
                                    patient_email=patient_email,
                                    patient_name=patient_name,
                                    start_time_iso=selected_slot,
                                    risk_summary=f"MEDIUM Risk - {diag.get('summary', '')[:30]}"
                                )
                                if result:
                                    # Save to local DB so doctor can see it in their dashboard
                                    save_appointment(
                                        patient_id=patient_id,
                                        doctor_email=doctor_email,
                                        appointment_time=selected_slot,
                                        summary=diag.get('summary', '')
                                    )
                                    st.session_state.appointment_booked = True
                                    st.success("Appointment Confirmed!")
                                    st.rerun()
                else:
                    st.warning("No open slots found for the next 3 days.")
            else:
                st.error("No doctor email found in profile.")
        else:
            st.success("✅ Your appointment is scheduled and reflected on both calendars.")
        st.divider()

    # --- STEP 4: FHIR HANDSHAKE ---
    if patient_id and session_id:
        with st.spinner("Generating FHIR R4 Record..."):
            fhir_data = save_diagnostic_report(patient_id, session_id, diag)
            
        with st.expander("📂 View FHIR R4 JSON (Interoperability)", expanded=False):
            st.json(fhir_data)

    # 3. Display AI Analysis
    st.subheader("Summary")
    st.write(diag.get('summary', 'Analysis provided by MedGemma.'))

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🧬 Potential Conditions")
        for cond in diag.get('top_conditions', []):
            st.markdown(f"- **{cond['name']}** ({int(cond['probability']*100)}%)")
            
    with col2:
        st.markdown("### 💊 Recommended Remedies")
        for rem in diag.get('remedies', []):
            st.markdown(f"- {rem}")

    # --- RECENT MEDICAL HISTORY SECTION ---
    st.divider()
    st.subheader("📜 Your Recent Medical History")
    
    if patient_id:
        recent_data = get_recent_sessions(patient_id, limit=3) 
        if recent_data:
            for i, entry in enumerate(recent_data):
                try:
                    past_diag = json.loads(entry['diagnosis'])
                    date_val = entry['created_at'][:10]
                    
                    with st.expander(f"Visit Date: {date_val} | Risk: {entry['risk_tier']}"):
                        st.write(f"**Symptoms:** {entry['symptoms']}")
                        st.info(f"**Main Condition:** {past_diag.get('top_conditions', [{}])[0].get('name', 'N/A')}")
                        
                        if st.button(f"Reload This Report", key=f"reload_res_{i}"):
                            st.session_state.email_sent = False
                            st.session_state.appointment_booked = False
                            st.session_state.diagnosis = past_diag
                            st.session_state.session_id = entry['id']
                            st.rerun()
                except Exception: 
                    continue
        else:
            st.info("No previous reports found.")

    st.divider()
    if st.button("🏠 Return to Dashboard"):
        st.session_state.diagnosis = None 
        st.session_state.email_sent = False
        st.session_state.appointment_booked = False
        st.session_state.current_page = "Symptoms"
        st.rerun()