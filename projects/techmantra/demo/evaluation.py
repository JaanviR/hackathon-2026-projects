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

def load_test_cases():
    test_data_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'test_data', 'test_cases.json')
    with open(test_data_path, 'r') as f:
        return json.load(f)

TEST_CASES = load_test_cases()



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
        payload = preprocess(case["input"], entities, case["profile"], duration=case.get("ui_duration", "not specified"),
    ui_severity=case.get("ui_severity", None))

        # Step 3 — RAG retrieval
        context = get_rag_context(case["input"], top_k=5)

        # Step 4 — LLM inference
        diagnosis = run_inference(payload, context)

        # Step 5 — Triage
        risk_tier = triage(
            diagnosis.get("confidence_score", 0),
            payload.get("severity", "low"),
            payload.get("duration", "not specified"),
            diagnosis.get("top_conditions", [{}])[0].get("name", "unknown"),
            llm_risk_tier=diagnosis.get("risk_tier")
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