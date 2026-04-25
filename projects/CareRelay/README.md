# CareRelay

CareRelay is a hackathon prototype that helps a new doctor quickly understand a patient's medical history from a patient-carried medical ID card and QR code.

The demo uses synthetic Synthea FHIR R4 patient data only. It is not for clinical use.

## Current Status

Implemented:
- Flask backend skeleton
- Parsed Synthea FHIR demo patient data
- `GET /api/patient/default` returning a doctor-friendly patient snapshot, trends, conditions, medications, encounters, and timeline

In progress / planned:
- OpenFDA drug warning endpoint
- AI first-visit brief endpoint using HuggingFace
- Medical entity extraction endpoint using HuggingFace
- QR endpoint for the patient card
- React frontend for snapshot, deep dive, and ID card views

## Backend Setup

```bash
cd projects/CareRelay/src/backend
source venv/bin/activate
python app.py
```

Then test the patient endpoint:

```bash
curl http://127.0.0.1:5000/api/patient/default
```

More backend details are in [docs/backend-api.md](docs/backend-api.md).
