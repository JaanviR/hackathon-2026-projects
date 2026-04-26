# from google.oauth2.credentials import Credentials
# from googleapiclient.discovery import build
# from datetime import datetime, timedelta

# def book_appointment(doctor_email, patient_name, risk_summary):
#     creds = Credentials.from_authorized_user_file("token.json")
#     service = build("calendar", "v3", credentials=creds)

#     event = {
#         "summary": f"Urgent: {patient_name} — AI Triage ({risk_summary})",
#         "start": {"dateTime": (datetime.now() + timedelta(hours=2)).isoformat()},
#         "end":   {"dateTime": (datetime.now() + timedelta(hours=3)).isoformat()},
#         "attendees": [{"email": doctor_email}]
#     }
#     service.events().insert(calendarId="primary", body=event).execute()