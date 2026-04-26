# demo/evaluation.py
# Purpose: Runs a set of predefined patient symptom inputs through the
# full MediTriage pipeline and records the results in a table.
# This file serves as an evaluation report showing:
# - What the app diagnoses for various symptom descriptions
# - Whether the risk tier matches the expected clinical outcome
# - How consistent the pipeline is across different inputs
#
# Run this file to regenerate the evaluation report:
#   python demo/evaluation.py
#
# Output: demo/evaluation_results.md

import sys
import os
import json
from datetime import datetime

# Add src/ to path so we can import our pipeline modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.ner import extract_entities
from core.preprocessing import preprocess
from core.rag import get_rag_context
from core.llm import run_inference
from core.triage import triage

# ── TEST CASES ────────────────────────────────────────────────────────
# Each test case represents a realistic patient scenario.
# expected_risk is what a clinician would expect — used to measure accuracy.
# Covers: HIGH emergencies, MEDIUM doctor-needed, LOW home care, edge cases

TEST_CASES = [
    # ── HIGH RISK CASES ───────────────────────────────────────────────
    {
        "id": 1,
        "patient": "Male, 58, hypertension, no allergies",
        "profile": {"age": 58, "conditions": "Hypertension", "allergies": "None"},
        "input": "I have sudden severe chest pain radiating to my left arm, I am sweating and feel short of breath",
        "expected_risk": "HIGH",
        "clinical_note": "Classic heart attack presentation"
    },
    {
        "id": 2,
        "patient": "Female, 25, no conditions, no allergies",
        "profile": {"age": 25, "conditions": "None", "allergies": "None"},
        "input": "I have a sudden severe headache, high fever of 103, my neck is very stiff and I am sensitive to light",
        "expected_risk": "HIGH",
        "clinical_note": "Classic bacterial meningitis triad"
    },
    {
        "id": 3,
        "patient": "Male, 40, no conditions, no allergies",
        "profile": {"age": 40, "conditions": "None", "allergies": "None"},
        "input": "I cannot breathe properly, my throat feels like it is closing and my face is swelling up",
        "expected_risk": "HIGH",
        "clinical_note": "Anaphylaxis — airway emergency"
    },
    {
        "id": 4,
        "patient": "Female, 67, diabetes, aspirin allergy",
        "profile": {"age": 67, "conditions": "Type 2 Diabetes", "allergies": "Aspirin"},
        "input": "I passed out earlier and now I feel confused and dizzy, my speech feels strange",
        "expected_risk": "HIGH",
        "clinical_note": "Possible stroke — FAST symptoms"
    },
    {
        "id": 5,
        "patient": "Male, 30, no conditions, no allergies",
        "profile": {"age": 30, "conditions": "None", "allergies": "None"},
        "input": "I am having a seizure, my whole body is shaking and I cannot control it",
        "expected_risk": "HIGH",
        "clinical_note": "Active seizure — neurological emergency"
    },

    # ── MEDIUM RISK CASES ─────────────────────────────────────────────
    {
        "id": 6,
        "patient": "Female, 34, no conditions, penicillin allergy",
        "profile": {"age": 34, "conditions": "None", "allergies": "Penicillin"},
        "input": "I have had ear pain for 3 days, mild fever of 100.5, and my hearing feels muffled in my right ear",
        "expected_risk": "MEDIUM",
        "clinical_note": "Ear infection — needs antibiotics"
    },
    {
        "id": 7,
        "patient": "Male, 45, no conditions, no allergies",
        "profile": {"age": 45, "conditions": "None", "allergies": "None"},
        "input": "I have a high fever of 102, chills, body aches, and I have been coughing for 4 days with yellow mucus",
        "expected_risk": "MEDIUM",
        "clinical_note": "Possible bacterial respiratory infection"
    },
    {
        "id": 8,
        "patient": "Female, 52, diabetes, no allergies",
        "profile": {"age": 52, "conditions": "Type 2 Diabetes", "allergies": "None"},
        "input": "I have a painful burning sensation when I urinate, lower abdominal pain, and a low fever for 2 days",
        "expected_risk": "MEDIUM",
        "clinical_note": "UTI — diabetes increases complication risk"
    },
    {
        "id": 9,
        "patient": "Male, 22, asthma, no allergies",
        "profile": {"age": 22, "conditions": "Asthma", "allergies": "None"},
        "input": "My asthma inhaler is not working, I am wheezing badly and having trouble breathing after exercise",
        "expected_risk": "MEDIUM",
        "clinical_note": "Asthma exacerbation — needs medical evaluation"
    },
    {
        "id": 10,
        "patient": "Female, 29, no conditions, no allergies",
        "profile": {"age": 29, "conditions": "None", "allergies": "None"},
        "input": "I have had a severe sore throat for 5 days with white patches on my tonsils and fever of 101",
        "expected_risk": "MEDIUM",
        "clinical_note": "Likely strep throat — needs antibiotics"
    },

    # ── LOW RISK CASES ────────────────────────────────────────────────
    {
        "id": 11,
        "patient": "Male, 32, no conditions, no allergies",
        "profile": {"age": 32, "conditions": "None", "allergies": "None"},
        "input": "I have a runny nose, sneezing, mild sore throat, and a slight cough for 2 days. No fever.",
        "expected_risk": "LOW",
        "clinical_note": "Common cold — home care appropriate"
    },
    {
        "id": 12,
        "patient": "Female, 28, seasonal allergies, no allergies to medication",
        "profile": {"age": 28, "conditions": "Seasonal Allergies", "allergies": "None"},
        "input": "My eyes are itchy and watery, I keep sneezing, and my nose is runny. No fever.",
        "expected_risk": "LOW",
        "clinical_note": "Seasonal allergies — antihistamine appropriate"
    },
    {
        "id": 13,
        "patient": "Male, 38, no conditions, no allergies",
        "profile": {"age": 38, "conditions": "None", "allergies": "None"},
        "input": "I have indigestion and heartburn after eating a large spicy meal. No chest pain or fever.",
        "expected_risk": "LOW",
        "clinical_note": "Indigestion — antacid appropriate"
    },
    {
        "id": 14,
        "patient": "Female, 24, no conditions, no allergies",
        "profile": {"age": 24, "conditions": "None", "allergies": "None"},
        "input": "I have a mild tension headache at the front of my head. No fever, no stiff neck, no vision changes.",
        "expected_risk": "LOW",
        "clinical_note": "Tension headache — home care appropriate"
    },
    {
        "id": 15,
        "patient": "Male, 50, no conditions, no allergies",
        "profile": {"age": 50, "conditions": "None", "allergies": "None"},
        "input": "I have mild lower back pain after lifting boxes yesterday. No numbness, no bladder issues.",
        "expected_risk": "LOW",
        "clinical_note": "Musculoskeletal back pain — rest and ice appropriate"
    },

    # ── EDGE CASES ────────────────────────────────────────────────────
    {
        "id": 16,
        "patient": "Female, 35, diabetes, penicillin allergy",
        "profile": {"age": 35, "conditions": "Type 2 Diabetes", "allergies": "Penicillin"},
        "input": "I have a fever and headache but no stiff neck, no chest pain, no difficulty breathing",
        "expected_risk": "LOW",
        "clinical_note": "Negation test — should NOT escalate despite fever+headache"
    },
    {
        "id": 17,
        "patient": "Male, 42, no conditions, no allergies",
        "profile": {"age": 42, "conditions": "None", "allergies": "None"},
        "input": "I am worried about meningitis because my friend has it but I just have a slight headache and no other symptoms",
        "expected_risk": "LOW",
        "clinical_note": "Anxiety mention test — should not over-escalate"
    },
    {
        "id": 18,
        "patient": "Female, 60, hypertension, no allergies",
        "profile": {"age": 60, "conditions": "Hypertension", "allergies": "None"},
        "input": "I feel dizzy when I stand up quickly and I felt faint once this morning but I am fine now",
        "expected_risk": "MEDIUM",
        "clinical_note": "Orthostatic hypotension in hypertensive patient — warrants evaluation"
    },
    {
        "id": 19,
        "patient": "Male, 19, no conditions, no allergies",
        "profile": {"age": 19, "conditions": "None", "allergies": "None"},
        "input": "aaa my stomch hrts rly bad",
        "expected_risk": "MEDIUM",
        "clinical_note": "Typo/informal input test — pipeline should still function"
    },
    {
        "id": 20,
        "patient": "Female, 45, no conditions, no allergies",
        "profile": {"age": 45, "conditions": "None", "allergies": "None"},
        "input": "I have had nausea and vomiting for 24 hours and I cannot keep any water down. I feel very weak.",
        "expected_risk": "MEDIUM",
        "clinical_note": "Dehydration risk — needs medical evaluation"
    },
]

# ── RUN PIPELINE ──────────────────────────────────────────────────────

def run_test_case(case):
    """
    Runs one test case through the full pipeline.
    Returns a result dict with all outputs.
    """
    print(f"  Running case {case['id']}: {case['input'][:50]}...")

    try:
        # Step 1 — NER
        entities = extract_entities(case["input"])

        # Step 2 — Preprocessing
        payload = preprocess(case["input"], entities, case["profile"])

        # Step 3 — RAG retrieval
        context = get_rag_context(case["input"], top_k=5)

        # Step 4 — LLM inference
        diagnosis = run_inference(payload, context)

        # Step 5 — Triage
        risk_tier = triage(
            diagnosis.get("confidence_score", 0),
            payload.get("severity", "low"),
            payload.get("duration", "a few days"),        # add this
            diagnosis.get("top_conditions", [{}])[0].get("name", "unknown")  # add this
        )

        # Check if result matches expected
        matched = risk_tier.upper() == case["expected_risk"].upper()

        return {
            "id": case["id"],
            "patient": case["patient"],
            "input": case["input"],
            "expected_risk": case["expected_risk"],
            "actual_risk": risk_tier.upper(),
            "matched": matched,
            "top_condition": diagnosis.get("top_conditions", [{}])[0].get("name", "Unknown"),
            "probability": diagnosis.get("top_conditions", [{}])[0].get("probability", 0),
            "confidence_score": diagnosis.get("confidence_score", 0),
            "symptoms_extracted": entities.get("symptoms", []),
            "negations_detected": entities.get("negations", []),
            "ner_severity": entities.get("severity", "low"),
            "rag_chunks": len(context.get("docs", [])),
            "summary": diagnosis.get("summary", "")[:150] + "...",
            "clinical_note": case["clinical_note"],
            "error": None
        }

    except Exception as e:
        # If pipeline fails for any reason record the error
        return {
            "id": case["id"],
            "patient": case["patient"],
            "input": case["input"],
            "expected_risk": case["expected_risk"],
            "actual_risk": "ERROR",
            "matched": False,
            "top_condition": "Pipeline Error",
            "probability": 0,
            "confidence_score": 0,
            "symptoms_extracted": [],
            "negations_detected": [],
            "ner_severity": "unknown",
            "rag_chunks": 0,
            "summary": "",
            "clinical_note": case["clinical_note"],
            "error": str(e)
        }


def calculate_accuracy(results):
    """
    Calculates overall and per-tier accuracy from results.
    """
    total = len(results)
    correct = sum(1 for r in results if r["matched"])
    errors = sum(1 for r in results if r["error"])

    # Per-tier breakdown
    tiers = ["HIGH", "MEDIUM", "LOW"]
    tier_stats = {}
    for tier in tiers:
        tier_cases = [r for r in results if r["expected_risk"] == tier]
        tier_correct = [r for r in tier_cases if r["matched"]]
        tier_stats[tier] = {
            "total": len(tier_cases),
            "correct": len(tier_correct),
            "accuracy": round(len(tier_correct) / len(tier_cases) * 100, 1) if tier_cases else 0
        }

    return {
        "total": total,
        "correct": correct,
        "errors": errors,
        "overall_accuracy": round(correct / total * 100, 1),
        "tier_stats": tier_stats
    }


def generate_markdown(results, accuracy, run_time):
    """
    Generates a clean markdown evaluation report.
    """
    correct_icon = lambda r: "✅" if r["matched"] else "❌"
    risk_emoji = {"HIGH": "🚨", "MEDIUM": "⚠️", "LOW": "✅", "ERROR": "💥"}

    lines = []

    # Header
    lines.append("# MediTriage — Evaluation Report")
    lines.append(f"### CareDevi AI Innovation Hackathon 2026")
    lines.append(f"**Generated:** {run_time}")
    lines.append(f"**Model:** alibayram/medgemma via Ollama")
    lines.append(f"**Pipeline:** medspaCy NER → LangChain RAG (ChromaDB) → MedGemma → Triage Engine")
    lines.append("")

    # Accuracy summary
    lines.append("---")
    lines.append("")
    lines.append("## Accuracy Summary")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|---|---|")
    lines.append(f"| Total Test Cases | {accuracy['total']} |")
    lines.append(f"| Correct Risk Tier | {accuracy['correct']} |")
    lines.append(f"| Pipeline Errors | {accuracy['errors']} |")
    lines.append(f"| **Overall Accuracy** | **{accuracy['overall_accuracy']}%** |")
    lines.append("")

    # Per-tier accuracy
    lines.append("### Accuracy by Risk Tier")
    lines.append("")
    lines.append("| Risk Tier | Test Cases | Correct | Accuracy |")
    lines.append("|---|---|---|---|")
    for tier, stats in accuracy["tier_stats"].items():
        emoji = risk_emoji.get(tier, "")
        lines.append(
            f"| {emoji} {tier} | {stats['total']} | {stats['correct']} | {stats['accuracy']}% |"
        )
    lines.append("")

    # Full results table
    lines.append("---")
    lines.append("")
    lines.append("## Detailed Results")
    lines.append("")
    lines.append("| # | Patient | Symptom Input | Expected | Got | Match | Top Condition | Confidence |")
    lines.append("|---|---|---|---|---|---|---|---|")

    for r in results:
        input_short = r["input"][:60] + "..." if len(r["input"]) > 60 else r["input"]
        match_icon = correct_icon(r)
        expected_display = f"{risk_emoji.get(r['expected_risk'], '')} {r['expected_risk']}"
        actual_display = f"{risk_emoji.get(r['actual_risk'], '')} {r['actual_risk']}"

        lines.append(
            f"| {r['id']} "
            f"| {r['patient']} "
            f"| {input_short} "
            f"| {expected_display} "
            f"| {actual_display} "
            f"| {match_icon} "
            f"| {r['top_condition']} ({r['probability']}%) "
            f"| {r['confidence_score']:.0%} |"
        )

    lines.append("")

    # NER performance section
    lines.append("---")
    lines.append("")
    lines.append("## NER Pipeline Performance")
    lines.append("")
    lines.append("Shows what medspaCy extracted from each input — confirms clinical NER is working correctly.")
    lines.append("")
    lines.append("| # | Input (short) | Symptoms Extracted | Negations Detected | NER Severity | RAG Chunks |")
    lines.append("|---|---|---|---|---|---|")

    for r in results:
        input_short = r["input"][:50] + "..." if len(r["input"]) > 50 else r["input"]
        symptoms = ", ".join(r["symptoms_extracted"][:3]) if r["symptoms_extracted"] else "none"
        negations = ", ".join(r["negations_detected"]) if r["negations_detected"] else "none"
        lines.append(
            f"| {r['id']} "
            f"| {input_short} "
            f"| {symptoms} "
            f"| {negations} "
            f"| {r['ner_severity'].upper()} "
            f"| {r['rag_chunks']} |"
        )

    lines.append("")

    # Detailed case breakdowns
    lines.append("---")
    lines.append("")
    lines.append("## Case-by-Case Breakdown")
    lines.append("")

    for r in results:
        match_icon = correct_icon(r)
        lines.append(f"### Case {r['id']} {match_icon} — {r['expected_risk']} Risk")
        lines.append(f"**Patient:** {r['patient']}")
        lines.append(f"**Clinical Note:** {r['clinical_note']}")
        lines.append(f"**Input:** {r['input']}")
        lines.append("")
        lines.append(f"| Field | Value |")
        lines.append(f"|---|---|")
        lines.append(f"| Expected Risk | {risk_emoji.get(r['expected_risk'], '')} {r['expected_risk']} |")
        lines.append(f"| Actual Risk | {risk_emoji.get(r['actual_risk'], '')} {r['actual_risk']} |")
        lines.append(f"| Top Condition | {r['top_condition']} ({r['probability']}%) |")
        lines.append(f"| Confidence Score | {r['confidence_score']:.0%} |")
        lines.append(f"| Symptoms Extracted | {', '.join(r['symptoms_extracted']) if r['symptoms_extracted'] else 'none'} |")
        lines.append(f"| Negations Detected | {', '.join(r['negations_detected']) if r['negations_detected'] else 'none'} |")
        lines.append(f"| NER Severity | {r['ner_severity'].upper()} |")
        lines.append(f"| RAG Chunks Retrieved | {r['rag_chunks']} |")
        lines.append(f"| AI Summary | {r['summary']} |")
        if r["error"]:
            lines.append(f"| Error | {r['error']} |")
        lines.append("")

    # Methodology note
    lines.append("---")
    lines.append("")
    lines.append("## Methodology")
    lines.append("")
    lines.append(
        "Each test case runs through the complete MediTriage pipeline: "
        "medspaCy clinical NER → preprocessing → LangChain RAG retrieval from ChromaDB "
        "(indexed from MedlinePlus and CDC sources) → MedGemma LLM inference via Ollama → "
        "risk triage engine."
    )
    lines.append("")
    lines.append(
        "Expected risk tiers were assigned based on standard clinical triage guidelines. "
        "HIGH = emergency requiring immediate care or 911. "
        "MEDIUM = requires physician evaluation within 24 hours. "
        "LOW = manageable with home care and self-monitoring."
    )
    lines.append("")
    lines.append(
        "This evaluation is not a clinical validation study. "
        "It demonstrates the pipeline's reasoning capability across diverse symptom presentations. "
        "MediTriage is a triage routing tool — not a diagnostic device — "
        "and requires clinical oversight before any real-world deployment."
    )
    lines.append("")
    lines.append("---")
    lines.append("*Generated by MediTriage evaluation pipeline — CareDevi Hackathon 2026*")

    return "\n".join(lines)


# ── MAIN ──────────────────────────────────────────────────────────────
if __name__ == "__main__":

    print("=" * 60)
    print("MediTriage — Evaluation Runner")
    print("=" * 60)
    print(f"Running {len(TEST_CASES)} test cases through full pipeline...")
    print("Make sure Ollama is running: ollama serve")
    print("=" * 60)

    run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    results = []

    for case in TEST_CASES:
        result = run_test_case(case)
        results.append(result)

        # Print live result so you can see progress
        icon = "✅" if result["matched"] else "❌"
        print(
            f"  {icon} Case {result['id']:02d} | "
            f"Expected: {result['expected_risk']:8} | "
            f"Got: {result['actual_risk']:8} | "
            f"{result['top_condition'][:30]}"
        )

    # Calculate accuracy
    accuracy = calculate_accuracy(results)

    print("")
    print("=" * 60)
    print(f"OVERALL ACCURACY: {accuracy['overall_accuracy']}%  "
          f"({accuracy['correct']}/{accuracy['total']} correct)")
    print("=" * 60)
    for tier, stats in accuracy["tier_stats"].items():
        print(f"  {tier:8} accuracy: {stats['accuracy']}%  ({stats['correct']}/{stats['total']})")

    # Generate and save markdown report
    markdown = generate_markdown(results, accuracy, run_time)

    output_path = os.path.join(os.path.dirname(__file__), "evaluation_results.md")
    with open(output_path, "w") as f:
        f.write(markdown)

    # Also save raw JSON results for reference
    json_path = os.path.join(os.path.dirname(__file__), "evaluation_results.json")
    with open(json_path, "w") as f:
        json.dump({
            "run_time": run_time,
            "accuracy": accuracy,
            "results": results
        }, f, indent=2)

    print("")
    print(f"Report saved to: {output_path}")
    print(f"Raw JSON saved to: {json_path}")
    print("")
    print("Add evaluation_results.md to your repo before submission.")