# Backend API

This document tracks the backend API as it is built. Keep it updated when endpoint behavior or response shapes change.

## Run Locally

```bash
cd projects/CareRelay/src/backend
source venv/bin/activate
python app.py
```

The Flask server runs at:

```text
http://127.0.0.1:5000
```

## Implemented Endpoints

### GET `/api/patient/default`

Returns parsed Synthea FHIR R4 data for the demo patient.

The raw Synthea bundle is stored at:

```text
projects/CareRelay/src/data/patient.json
```

The parser converts the raw FHIR bundle into frontend-friendly sections:

- `patient`
- `snapshot`
- `conditions`
- `medications`
- `observations`
- `trends`
- `encounters`
- `timeline`
- `conditionThreads`
- `disclaimer`

Example test:

```bash
curl -s http://127.0.0.1:5000/api/patient/default -o /tmp/carerelay_patient_response.json
```

Quick summary check:

```bash
/tmp/check_carerelay_patient.sh
```

Expected summary:

```text
Patient: Emerald468 Botsford977
Age: 77
Conditions: 52
Medications: 28
Timeline: 300
Metrics: ['blood_pressure', 'egfr', 'glucose', 'hba1c', 'ldl', 'triglycerides', 'weight']
```

## Planned Endpoints

### POST `/api/brief`

Planned: generate a first-visit brief from patient data using a HuggingFace medical model.

### GET `/api/drugs/interactions`

Planned: check current medications against OpenFDA label data and return warnings.

### POST `/api/ner`

Planned: extract medical entities from clinical note text using a HuggingFace NER model.

### GET `/api/qr/<patient_id>`

Planned: return QR data for opening the patient summary.

## Frontend Notes

The React frontend should call:

```text
GET http://127.0.0.1:5000/api/patient/default
```

CORS is enabled in Flask, so local frontend calls from Vite should work while the Flask server is running.

Example JavaScript:

```js
const response = await fetch("http://127.0.0.1:5000/api/patient/default");
const data = await response.json();
console.log(data.patient.name);
console.log(data.snapshot.latestMetrics);
```

## Demo Data Note

All current data is synthetic Synthea FHIR R4 data. No real patient information or PHI is used.
