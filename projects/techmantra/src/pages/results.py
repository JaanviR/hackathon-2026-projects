import streamlit as st
import json
import pandas as pd
from db.db import save_diagnostic_report, get_recent_sessions

# --- NEW INTEGRATION IMPORTS ---
from integrations.notifications import send_summary
from integrations.calendar_api import book_appointment

# def show():
#     patient_id = st.session_state.get('patient_id')

#     # --- FIX: AUTO-LOAD PREVIOUS RECORD IF STATE IS EMPTY ---
#     if not st.session_state.get('diagnosis'):
#         if patient_id:
#             recent = get_recent_sessions(patient_id, limit=1)
#             if recent:
#                 # Silently load the latest record into the session state
#                 entry = recent[0]
#                 st.session_state.diagnosis = json.loads(entry['diagnosis'])
#                 st.session_state.session_id = entry['id']
#                 st.session_state.severity = entry['risk_tier']
#                 st.session_state.current_symptoms = entry['symptoms']
#             else:
#                 st.warning("Please run the symptom checker first.")
#                 if st.button("Go Back"):
#                     st.session_state.current_page = "Symptoms"
#                     st.rerun()
#                 return
#         else:
#             st.error("Please log in to view results.")
#             return

#     # 1. Get diagnosis data (either fresh from AI or auto-loaded from DB)
#     diag = st.session_state.diagnosis
#     risk = diag.get('risk_tier', 'LOW').upper()
#     session_id = st.session_state.get('session_id')
#     user_profile = st.session_state.get('user_profile', {})

#     # 2. Display Urgent Banner
#     if risk == "HIGH":
#         st.error("🚨 **EMERGENCY: Please seek immediate medical attention.**")
#     elif risk == "MEDIUM":
#         st.warning("⚠️ **MEDIUM: Follow-up with a healthcare provider soon.**")
#     else:
#         st.success("✅ **LOW RISK: Manage symptoms at home and monitor.**")

#     st.title("📋 Diagnostic Report")

#     # --- NEW: TRIGGER AUTOMATION INTEGRATIONS ---
#     # We use session state flags to ensure these only run once per report generation
    
#     # A. Send Email Notification (Always)
#     if not st.session_state.get('email_sent'):
#         with st.spinner("📧 Notifying your doctor via email..."):
#             email_success = send_summary(user_profile, diag, risk)
#             if email_success:
#                 st.session_state['email_sent'] = True
#                 st.toast("Doctor has been notified of this report.")

#     # B. Book Calendar Appointment (Only for MEDIUM risk)
#     if risk == "MEDIUM" and not st.session_state.get('appointment_booked'):
#         physician = user_profile.get("physician", {})
#         doctor_email = physician.get("email")
        
#         if doctor_email:
#             with st.spinner("📅 Booking follow-up appointment..."):
#                 appt_result = book_appointment(
#                     doctor_email=doctor_email,
#                     patient_email=user_profile.get("email"),
#                     patient_name=user_profile.get("name", "Patient"),
#                     risk_summary=f"MEDIUM Risk: {diag.get('summary', '')[:50]}..."
#                 )
#                 if appt_result:
#                     st.session_state['appointment_booked'] = True
#                     st.success(f"Appointment scheduled on Google Calendar with Dr. {physician.get('name', 'Provider')}")

#     # --- STEP 4: FHIR HANDSHAKE ---
#     if patient_id and session_id:
#         with st.spinner("Generating FHIR R4 Record..."):
#             fhir_data = save_diagnostic_report(patient_id, session_id, diag)
            
#         with st.expander("📂 View FHIR R4 JSON (Interoperability)", expanded=False):
#             st.json(fhir_data)

#     # 3. Display AI Analysis
#     st.subheader("Summary")
#     st.write(diag.get('summary', 'Analysis provided by MedGemma.'))

#     col1, col2 = st.columns(2)
#     with col1:
#         st.markdown("### 🧬 Potential Conditions")
#         for cond in diag.get('top_conditions', []):
#             st.markdown(f"- **{cond['name']}** ({int(cond['probability']*100)}%)")
            
#     with col2:
#         st.markdown("### 💊 Recommended Remedies")
#         for rem in diag.get('remedies', []):
#             st.markdown(f"- {rem}")

#     # --- RECENT MEDICAL HISTORY SECTION ---
#     st.divider()
#     st.subheader("📜 Your Recent Medical History")
    
#     if patient_id:
#         recent_data = get_recent_sessions(patient_id, limit=3) 
#         if recent_data:
#             for i, entry in enumerate(recent_data):
#                 try:
#                     past_diag = json.loads(entry['diagnosis'])
#                     date_val = entry['created_at'][:10]
                    
#                     with st.expander(f"Visit Date: {date_val} | Risk: {entry['risk_tier']}"):
#                         st.write(f"**Symptoms:** {entry['symptoms']}")
#                         st.info(f"**Main Condition:** {past_diag.get('top_conditions', [{}])[0].get('name', 'N/A')}")
                        
#                         if st.button(f"Reload This Report", key=f"reload_res_{i}"):
#                             # Reset flags so automation can re-run for a different report if desired
#                             st.session_state.email_sent = False
#                             st.session_state.appointment_booked = False
#                             st.session_state.diagnosis = past_diag
#                             st.session_state.session_id = entry['id']
#                             st.rerun()
#                 except Exception: 
#                     continue
#         else:
#             st.info("No previous reports found.")

#     st.divider()
#     if st.button("🏠 Return to Dashboard"):
#         st.session_state.diagnosis = None 
#         # Reset automation flags for the next session
#         st.session_state.email_sent = False
#         st.session_state.appointment_booked = False
#         st.session_state.current_page = "Symptoms"
#         st.rerun()
def show():
    patient_id = st.session_state.get('patient_id')
    scroll_to = st.session_state.pop("scroll_to", None)  # 👈 read scroll target

    # --- AUTO-LOAD PREVIOUS RECORD IF STATE IS EMPTY ---
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

    # ── RISK BANNER ───────────────────────────────────────────────────
    if risk == "HIGH":
        st.markdown("""
            <div style="background:#ff000020; border:2px solid #ff0000;
                 border-radius:12px; padding:24px; text-align:center; margin:16px 0;">
                <h2 style="color:#cc0000; margin:0;">🚨 EMERGENCY</h2>
                <p style="color:#cc0000; font-size:18px; margin:8px 0;">
                    Your symptoms require <strong>immediate medical attention.</strong>
                </p>
            </div>
        """, unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.link_button("📞 Call 911 Now", "tel:911",
                           use_container_width=True, type="primary")
        with col2:
            st.link_button("🗺️ Find Nearest ER",
                           "https://www.google.com/maps/search/emergency+room+near+me",
                           use_container_width=True)

    elif risk == "MEDIUM":
        st.markdown("""
            <div style="background:#fff3cd; border:2px solid #ffc107;
                 border-radius:12px; padding:24px; text-align:center; margin:16px 0;">
                <h2 style="color:#856404; margin:0;">⚠️ MEDICAL ATTENTION NEEDED</h2>
                <p style="color:#856404; font-size:16px; margin:8px 0;">
                    You should see a doctor within <strong>24 hours.</strong>
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="background:#d4edda; border:2px solid #28a745;
                 border-radius:12px; padding:24px; text-align:center; margin:16px 0;">
                <h2 style="color:#155724; margin:0;">✅ LOW RISK</h2>
                <p style="color:#155724; font-size:16px; margin:8px 0;">
                    Your symptoms can be managed at home.
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.title("📋 Diagnostic Report")

    # ── INTEGRATIONS ──────────────────────────────────────────────────
    if not st.session_state.get('email_sent'):
        with st.spinner("📧 Notifying your doctor via email..."):
            email_success = send_summary(user_profile, diag, risk)
            if email_success:
                st.session_state['email_sent'] = True
                st.toast("Doctor has been notified of this report.")

    # ── APPOINTMENT ANCHOR + AUTO-BOOK ────────────────────────────────
    st.markdown('<div id="appointment"></div>', unsafe_allow_html=True)  # 👈 scroll anchor

    if risk == "MEDIUM" and not st.session_state.get('appointment_booked'):
        physician = user_profile.get("physician", {})
        doctor_email = physician.get("email")
        if doctor_email:
            with st.spinner("📅 Booking follow-up appointment..."):
                appt_result = book_appointment(
                    doctor_email=doctor_email,
                    patient_email=user_profile.get("email"),
                    patient_name=user_profile.get("name", "Patient"),
                    risk_summary=f"MEDIUM Risk: {diag.get('summary', '')[:50]}..."
                )
                if appt_result:
                    st.session_state['appointment_booked'] = True
                    st.success(f"📅 Appointment scheduled with Dr. {physician.get('name', 'Provider')}")

    # ── FHIR ──────────────────────────────────────────────────────────
    if patient_id and session_id:
        with st.spinner("Generating FHIR R4 Record..."):
            fhir_data = save_diagnostic_report(patient_id, session_id, diag)
        with st.expander("📂 View FHIR R4 JSON (Interoperability)", expanded=False):
            st.json(fhir_data)

    # ── SUMMARY ───────────────────────────────────────────────────────
    st.subheader("Summary")
    st.write(diag.get('summary', 'Analysis provided by MedGemma.'))

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🧬 Potential Conditions")
        for cond in diag.get('top_conditions', []):
            st.markdown(f"- **{cond['name']}** ({int(cond['probability']*100)}%)")

    # ── REMEDIES ANCHOR ───────────────────────────────────────────────
    with col2:
        st.markdown('<div id="remedies"></div>', unsafe_allow_html=True)  # 👈 scroll anchor
        st.markdown("### 💊 Recommended Remedies")
        for rem in diag.get('remedies', []):
            st.markdown(f"- {rem}")

    # ── AUTO SCROLL ───────────────────────────────────────────────────
    if scroll_to:
        st.markdown(f"""
            <script>
                window.addEventListener('load', function() {{
                    const el = document.getElementById('{scroll_to}');
                    if (el) el.scrollIntoView({{behavior: 'smooth'}});
                }});
            </script>
        """, unsafe_allow_html=True)

    # ── RECENT HISTORY ────────────────────────────────────────────────
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

    # ── FULL REPORT (all tiers) ───────────────────────────────────
        st.markdown("---")
        if st.button("📋 Proceed to Full Medical Report ➡️", use_container_width=True):
            st.session_state["current_page"] = "Results"
            st.rerun()

        # 👈 add this
        if st.button("🔄 Start New Analysis", use_container_width=True):
            st.session_state.diagnosis = None
            st.session_state.transcript = ""
            st.session_state.email_sent = False
            st.session_state.appointment_booked = False
            st.rerun()