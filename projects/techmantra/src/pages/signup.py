import streamlit as st
import sys
import os

# Ensure the root directory is in the path so we can find the 'db' folder
# We go up two levels because we are in src/pages and need to see src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Try/Except import to catch pathing issues immediately
try:
    from db.db import save_patient, save_allergy, save_known_condition, save_physician
except ImportError:
    st.error("Could not find the 'db' module. Make sure your folder structure is correct!")

def show():
    st.title("🏥 Patient Signup")
    st.markdown("Enter your details to initialize your clinical profile.")

    # Wrap EVERYTHING in a form to prevent the "Missing Name/Location" bug
    with st.form("registration_form", clear_on_submit=False):
        
        # SECTION 1: Bio Data
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", placeholder="John Doe")
        with col2:
            age = st.number_input("Age", 1, 120, 25)
        
        col_s, col_l = st.columns(2)
        with col_s:
            sex = st.selectbox("Sex", ["Male", "Female", "Other"])
        with col_l:
            location = st.text_input("Location/City", placeholder="e.g. Austin, TX")

        # SECTION 2: Medical Context
        st.divider()
        col3, col4 = st.columns(2)
        with col3:
            height = st.number_input("Height (cm)", value=170.0)
        with col4:
            weight = st.number_input("Weight (kg)", value=70.0)

        allergies = st.text_area("Known Allergies", placeholder="Penicillin, Nuts, etc.")
        conditions = st.text_area("Pre-existing Conditions", placeholder="Diabetes, Asthma, etc.")

        # SECTION 3: Physician Info
        st.divider()
        st.subheader("Primary Physician")
        dr_name = st.text_input("Doctor Name")
        hospital = st.text_input("Hospital Name", placeholder="General Hospital")
        dr_email = st.text_input("Doctor Email")

        # The Form Submit Button
        submit_button = st.form_submit_button("Save Profile", type="primary", use_container_width=True)

    # LOGIC: Only runs when the form button is clicked
    if submit_button:
        # Check .strip() to ignore spaces
        if not name.strip() or not location.strip():
            st.error("🚨 Error: Name and Location are required to create a record.")
        else:
            with st.spinner("Writing to secure database..."):
                try:
                    # 1. Save main patient and get the unique UUID
                    patient_id = save_patient(
                        name=name,
                        age=int(age),
                        sex=sex,
                        height_cm=float(height),
                        weight_kg=float(weight),
                        place=location
                    )

                    # 2. Save Allergies (if provided)
                    if allergies.strip():
                        save_allergy(patient_id, allergies.strip(), "Moderate")

                    # 3. Save Conditions (if provided)
                    if conditions.strip():
                        save_known_condition(patient_id, conditions.strip())

                    # 4. Save Physician Details
                    if dr_name.strip():
                        save_physician(patient_id, dr_name.strip(), hospital.strip(), dr_email.strip())

                    # 5. Update Session State
                    st.session_state.patient_id = patient_id
                    st.session_state.user_profile = {
                        "name": name,
                        "id": patient_id,
                        "location": location
                    }
                    st.session_state.is_authenticated = True

                    st.success(f"✅ Success! Patient ID: {patient_id}")
                    st.balloons()
                    
                    # Force a refresh to show the sidebar/next page
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Database Error: {e}")