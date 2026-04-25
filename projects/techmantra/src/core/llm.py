prompt = f"""
RETRIEVED MEDICAL DOCUMENTS (use ONLY these for your answer):
{text}

PATIENT INFORMATION:
- Age: 
- Known pre-existing conditions: 
- Known allergies:

CLINICAL NER ANALYSIS:

FULL SYMPTOM DESCRIPTION:

IMPORTANT: Respond with ONLY a valid JSON object.
No explanation, no markdown, no code blocks. Just raw JSON.
"""