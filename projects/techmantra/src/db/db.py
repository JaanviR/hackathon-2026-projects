"""
db/db.py  —  base: This performs patient related opretions CRUD using SQLite
Run directly to test:  python db.py
"""

import json
import sqlite3
import uuid
from pathlib import Path

# Use .resolve() to get the absolute, real path on your Mac
DB_PATH     = Path(__file__).resolve().parent / "triage.db"
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """Create tables from schema.sql. Safe to call multiple times."""
    conn = get_connection()
    with open(SCHEMA_PATH) as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print(f"[db] Tables created at {DB_PATH}")


# ── Patient ────────────────────────────────────────────────────

def save_patient(name: str, age: int, sex: str,
                 height_cm: float, weight_kg: float, place: str) -> str:
    patient_id = str(uuid.uuid4())
    conn = get_connection()
    conn.execute(
        "INSERT INTO patients (id, name, age, sex, height_cm, weight_kg, place) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (patient_id, name, age, sex, height_cm, weight_kg, place)
    )
    conn.commit()
    conn.close()
    return patient_id


def get_patient(patient_id: str) -> dict | None:
    conn = get_connection()
    row = conn.execute("SELECT * FROM patients WHERE id = ?", (patient_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


# ── Allergies ──────────────────────────────────────────────────

def save_allergy(patient_id: str, allergen: str, severity: str = "unknown") -> str:
    allergy_id = str(uuid.uuid4())
    conn = get_connection()
    conn.execute(
        "INSERT INTO allergies (id, patient_id, allergen, severity) VALUES (?, ?, ?, ?)",
        (allergy_id, patient_id, allergen, severity)
    )
    conn.commit()
    conn.close()
    return allergy_id


# ── Known conditions ───────────────────────────────────────────

def save_known_condition(patient_id: str, condition_name: str,
                          icd10_code: str = "") -> str:
    cond_id = str(uuid.uuid4())
    conn = get_connection()
    conn.execute(
        "INSERT INTO known_conditions (id, patient_id, condition_name, icd10_code) "
        "VALUES (?, ?, ?, ?)",
        (cond_id, patient_id, condition_name, icd10_code)
    )
    conn.commit()
    conn.close()
    return cond_id


# ── Physician ──────────────────────────────────────────────────

def save_physician(patient_id: str, doctor_name: str,
                   hospital_name: str, email: str) -> str:
    phys_id = str(uuid.uuid4())
    conn = get_connection()
    conn.execute(
        "INSERT INTO physician_details (id, patient_id, doctor_name, hospital_name, email) "
        "VALUES (?, ?, ?, ?, ?)",
        (phys_id, patient_id, doctor_name, hospital_name, email)
    )
    conn.commit()
    conn.close()
    return phys_id


# ── Full context (used by preprocessing layer) ─────────────────

def get_patient_full_context(patient_id: str) -> dict:
    conn = get_connection()
    patient    = conn.execute("SELECT * FROM patients WHERE id = ?", (patient_id,)).fetchone()
    allergies  = conn.execute("SELECT allergen, severity FROM allergies WHERE patient_id = ?", (patient_id,)).fetchall()
    conditions = conn.execute("SELECT condition_name, icd10_code FROM known_conditions WHERE patient_id = ?", (patient_id,)).fetchall()
    physician  = conn.execute("SELECT * FROM physician_details WHERE patient_id = ?", (patient_id,)).fetchone()
    conn.close()
    return {
        "patient":          dict(patient)    if patient   else {},
        "allergies":        [dict(r) for r in allergies],
        "known_conditions": [dict(r) for r in conditions],
        "physician":        dict(physician)  if physician else {}
    }


# ── FHIR Export ────────────────────────────────────────────────

def get_patient_as_fhir(patient_id: str) -> dict:
    """
    Converts patient SQLite data → FHIR R4 Bundle JSON.
    Call this when saving DiagnosticReport or sending summary to doctor.
    """
    ctx = get_patient_full_context(patient_id)
    p   = ctx["patient"]

    fhir_patient = {
        "resourceType": "Patient",
        "id": patient_id,
        "name": [{
            "use": "official",
            "text": p.get("name", ""),
            "family": p.get("name", "").split()[-1] if p.get("name") else "",
            "given":  [p.get("name", "").split()[0]] if p.get("name") else []
        }],
        "gender": p.get("sex", "unknown").lower(),
        "birthDate": _age_to_birthdate(p.get("age")),
        "address": [{"text": p.get("place", "")}],
        "extension": [
            {
                "url": "http://example.org/height",
                "valueQuantity": {
                    "value": p.get("height_cm"),
                    "unit": "cm",
                    "system": "http://unitsofmeasure.org",
                    "code": "cm"
                }
            },
            {
                "url": "http://example.org/weight",
                "valueQuantity": {
                    "value": p.get("weight_kg"),
                    "unit": "kg",
                    "system": "http://unitsofmeasure.org",
                    "code": "kg"
                }
            }
        ]
    }

    fhir_allergies = []
    for allergy in ctx["allergies"]:
        fhir_allergies.append({
            "resourceType": "AllergyIntolerance",
            "id": str(uuid.uuid4()),
            "patient": {"reference": f"Patient/{patient_id}"},
            "code": {"text": allergy["allergen"]},
            "criticality": _map_severity(allergy["severity"]),
            "clinicalStatus": {
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical",
                    "code": "active"
                }]
            }
        })

    fhir_conditions = []
    for cond in ctx["known_conditions"]:
        fhir_conditions.append({
            "resourceType": "Condition",
            "id": str(uuid.uuid4()),
            "subject": {"reference": f"Patient/{patient_id}"},
            "code": {
                "coding": [{
                    "system": "http://hl7.org/fhir/sid/icd-10",
                    "code":   cond.get("icd10_code", ""),
                    "display": cond["condition_name"]
                }],
                "text": cond["condition_name"]
            },
            "clinicalStatus": {
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                    "code": "active"
                }]
            }
        })

    return {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": (
            [{"resource": fhir_patient}] +
            [{"resource": a} for a in fhir_allergies] +
            [{"resource": c} for c in fhir_conditions]
        )
    }


def save_diagnostic_report(patient_id: str, session_id: str,
                             llm_output: dict) -> dict:
    """
    Converts AI triage output → FHIR DiagnosticReport.
    Call this after LLM responds (Layer 3 output).
    NOTE: the sessions table UPDATE is disabled until sessions table is added in Stage 2.
    """
    top_conditions = llm_output.get("doctor_output", {}).get("differential_diagnosis", [])
    risk           = llm_output.get("patient_output", {}).get("risk_level", "LOW")

    report = {
        "resourceType": "DiagnosticReport",
        "id": session_id,
        "status": "preliminary",
        "subject": {"reference": f"Patient/{patient_id}"},
        "issued": _now_iso(),
        "conclusion": llm_output.get("doctor_output", {}).get("chief_complaint", ""),
        "conclusionCode": [
            {
                "coding": [{
                    "system": "http://hl7.org/fhir/sid/icd-10",
                    "code":   c.get("icd10", ""),
                    "display": c.get("condition", "")
                }],
                "text": c.get("condition", "")
            }
            for c in top_conditions
        ],
        "extension": [
            {"url": "http://example.org/risk-tier",   "valueString": risk},
            {"url": "http://example.org/disclaimer",  "valueString": "This output was generated by an AI system and is not a substitute for clinical judgment."}
        ]
    }

    # TODO Stage 2: uncomment once sessions table is added to schema.sql
    # conn = get_connection()
    # conn.execute("UPDATE sessions SET fhir_report = ? WHERE id = ?", (json.dumps(report), session_id))
    # conn.commit()
    # conn.close()

    return report


# ── Helpers ────────────────────────────────────────────────────

def _age_to_birthdate(age: int) -> str:
    """Approximate birth year from age for FHIR birthDate field."""
    if not age:
        return ""
    from datetime import datetime
    return f"{datetime.now().year - int(age)}-01-01"


def _now_iso() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


def _map_severity(severity: str) -> str:
    """Maps your severity strings to FHIR criticality codes."""
    mapping = {
        "severe":   "high",
        "moderate": "low",
        "mild":     "low",
        "unknown":  "unable-to-assess"
    }
    return mapping.get((severity or "").lower(), "unable-to-assess")


# ── Quick test ─────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()

    pid = save_patient("Jane Doe", 35, "female", 162.0, 65.0, "Austin, TX")
    print(f"Created patient: {pid}")

    save_allergy(pid, "penicillin", "severe")
    save_known_condition(pid, "Type 2 Diabetes", "E11")
    save_physician(pid, "Dr. Smith", "Austin General", "dr.smith@example.com")

    ctx = get_patient_full_context(pid)
    print(json.dumps(ctx, indent=2))

    bundle = get_patient_as_fhir(pid)
    print("\n[test] FHIR Bundle:")
    print(json.dumps(bundle, indent=2))
