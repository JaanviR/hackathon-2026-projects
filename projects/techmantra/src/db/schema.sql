-- db/schema.sql  —  base: Adding only patient data in tables
-- Add sessions table for storing session data

CREATE TABLE IF NOT EXISTS patients (
    id           TEXT PRIMARY KEY,
    name         TEXT NOT NULL,
    age          INTEGER,
    sex          TEXT,
    height_cm    REAL,
    weight_kg    REAL,
    place        TEXT,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS allergies (
    id         TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL REFERENCES patients(id),
    allergen   TEXT NOT NULL,
    severity   TEXT DEFAULT 'unknown'
);

CREATE TABLE IF NOT EXISTS known_conditions (
    id             TEXT PRIMARY KEY,
    patient_id     TEXT NOT NULL REFERENCES patients(id),
    condition_name TEXT NOT NULL,
    icd10_code     TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS physician_details (
    id            TEXT PRIMARY KEY,
    patient_id    TEXT NOT NULL REFERENCES patients(id),
    doctor_name   TEXT NOT NULL,
    hospital_name TEXT,
    email         TEXT
);

-- Add this to schema.sql
CREATE TABLE IF NOT EXISTS sessions (
    id           TEXT PRIMARY KEY,
    patient_id   TEXT NOT NULL REFERENCES patients(id),
    symptoms_raw       TEXT,
    symptoms_structured TEXT,
    rag_context        TEXT,
    llm_output         TEXT,
    risk_level         TEXT,
    priority           INTEGER DEFAULT 3,
    fhir_report        TEXT,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);