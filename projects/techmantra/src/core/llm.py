import ollama
import json
import re

MODEL_NAME = "bio-mistral"

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
    try:
        # ollama.chat() sends a message to the local Ollama server
        # model: which pulled model to use
        # messages: list of message dicts with role and content
        # options: model parameters
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {
                    # System message sets behavior rules
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    # User message contains the actual symptoms + context
                    "role": "user",
                    "content": user_message
                }
            ],
            options={
                # temperature=0 makes output more deterministic
                # Lower = more consistent, less creative
                # For medical diagnosis we want consistency
                "temperature": 0.1,
                
                # Maximum tokens in the response
                # 1000 is enough for our JSON structure
                "num_predict": 1000,
            }
        )   
        # Extract the response text from Ollama's response object
        # response["message"]["content"] contains the LLM's reply
        raw_text = response["message"]["content"].strip()
        
        # Clean up response in case LLM added markdown code blocks
        # Some models wrap JSON in ```json ... ``` despite instructions
        raw_text = clean_json_response(raw_text)
        
        # Parse JSON string into Python dict
        result = json.loads(raw_text)
        
        # Validate that required keys exist in the response
        result = validate_and_fix_response(result)
        
        return result
    
    except ollama.ResponseError as e:
        # Ollama server returned an error — usually model not found
        print(f"Ollama error: {e}")
        print(f"Make sure you ran: ollama pull {MODEL_NAME}")
        return get_fallback_response(f"Ollama model error: {e}")