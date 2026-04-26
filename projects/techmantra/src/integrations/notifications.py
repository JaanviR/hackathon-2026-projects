# import sendgrid
# from sendgrid.helpers.mail import Mail
# from twilio.rest import Client
# import os

# def send_summary(user_profile, diagnosis, risk):
#     doctor_email = user_profile["extension"][4]["valueString"].split("|")[2].strip()

#     # Email via SendGrid
#     sg = sendgrid.SendGridAPIClient(api_key=os.getenv("SENDGRID_API_KEY"))
#     message = Mail(
#         from_email="triage@yourapp.com",
#         to_emails=doctor_email,
#         subject=f"Patient Triage Summary — Risk: {risk}",
#         plain_text_content=f"""
# Patient: {user_profile['name'][0]['text']}
# Risk Level: {risk}
# Top Conditions: {diagnosis['top_conditions']}
# Confidence: {diagnosis['confidence_score']}
# Summary: {diagnosis['summary']}
# Sources: {diagnosis['sources']}
# Disclaimer: AI-generated. Not a substitute for clinical judgment.
#         """
#     )
#     sg.send(message)