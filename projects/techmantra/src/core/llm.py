SYSTEM_PROMPT = """You are a medical triage assistant helping patients 
understand their symptoms.

STRICT RULES YOU MUST FOLLOW:
1. Answer ONLY based on the retrieved medical documents provided to you
2. If the documents don't contain enough information, respond with a JSON where confidence_score is 0.3 and risk_tier is "medium"
3. Never invent symptoms, treatments or medical facts not in the documents
4. Always include a disclaimer that this is not clinical medical advice
5. You MUST respond ONLY in valid JSON — no text before or after the JSON
6. Do not include markdown code blocks like ```json — just raw JSON

Your response must be a single valid JSON object with EXACTLY these keys:
{
  "top_conditions": [{"name": "condition name", "probability": 75}],
  "confidence_score": 0.75,
  "risk_tier": "low",
  "warnings": ["warning 1", "warning 2"],
  "remedies": ["remedy 1", "remedy 2"],
  "summary": "plain english summary for the patient",
  "sources": ["source 1", "source 2"],
  "disclaimer": "This is not a substitute for clinical judgment"
}
"""

def run_inference(payload, context):
    """
    Sends symptoms + RAG context to local Ollama model.
    payload: structured dict from preprocessing.py
    context: dict with docs and sources from rag.py (without context the model will start to hallucinate)
    Returns: parsed dict with diagnosis, risk, remedies etc.
    """
    # Join all retrieved document chunks into one block of text
    # These are the medical articles ChromaDB retrieved
    docs_text = "\n\n".join(context["docs"])
    
    # Pull source names from metadata for attribution
    source_names = [
        s.get("source", "Medical Database") 
        for s in context["sources"]
    ]
    
    # Build the full prompt that combines:
    # - Retrieved medical documents (RAG context)
    # - Patient profile information
    # - Reported symptoms
    user_message = f"""
        RETRIEVED MEDICAL DOCUMENTS (use ONLY these for your answer):
        {docs_text}

        PATIENT INFORMATION:
        - Age: {payload['patient_age']}
        - Known pre-existing conditions: {payload['known_conditions']}
        - Known allergies: {payload['known_allergies']}
        - Symptoms patient does NOT have: {payload['negations']}

        REPORTED SYMPTOMS:
        {payload['raw_symptoms']}

        EXTRACTED SYMPTOM ENTITIES:
        {', '.join(payload['extracted_symptoms'])}

        Available sources: {', '.join(source_names)}

        IMPORTANT: Respond with ONLY a valid JSON object. 
        No explanation, no markdown, no code blocks. Just raw JSON.
        """