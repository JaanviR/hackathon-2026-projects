# MediTriage — Evaluation Report
### CareDevi AI Innovation Hackathon 2026
**Generated:** 2026-04-26 07:59:17
**Model:** alibayram/medgemma via Ollama
**Pipeline:** medspaCy NER → LangChain RAG (ChromaDB) → MedGemma → Triage Engine

---

## Accuracy Summary

| Metric | Value |
|---|---|
| Total Test Cases | 20 |
| Correct Risk Tier | 18 |
| Pipeline Errors | 0 |
| **Overall Accuracy** | **90.0%** |

### Accuracy by Risk Tier

| Risk Tier | Test Cases | Correct | Accuracy |
|---|---|---|---|
| 🚨 HIGH | 5 | 5 | 100.0% |
| ⚠️ MEDIUM | 8 | 6 | 75.0% |
| ✅ LOW | 7 | 7 | 100.0% |

---

## Detailed Results

| # | Patient | Symptom Input | Expected | Got | Match | Top Condition | Confidence |
|---|---|---|---|---|---|---|---|
| 1 | Male, 58, hypertension, no allergies | I have sudden severe chest pain radiating to my left arm, I ... | 🚨 HIGH | 🚨 HIGH | ✅ | Cardiac chest pain (heart-related — EMERGENCY) (0.95%) | 95% |
| 2 | Female, 25, no conditions, no allergies | I have a sudden severe headache, high fever of 103, my neck ... | 🚨 HIGH | 🚨 HIGH | ✅ | Meningitis (0.95%) | 95% |
| 3 | Male, 40, no conditions, no allergies | I cannot breathe properly, my throat feels like it is closin... | 🚨 HIGH | 🚨 HIGH | ✅ | Severe sore throat with breathing difficulty and facial swelling (0.95%) | 95% |
| 4 | Female, 67, diabetes, aspirin allergy | I passed out earlier and now I feel confused and dizzy, my s... | 🚨 HIGH | 🚨 HIGH | ✅ | Dizziness (0.9%) | 80% |
| 5 | Male, 30, no conditions, no allergies | I am having a seizure, my whole body is shaking and I cannot... | 🚨 HIGH | 🚨 HIGH | ✅ | Seizure (0.95%) | 85% |
| 6 | Female, 34, no conditions, penicillin allergy | I have had ear pain for 3 days, mild fever of 100.5, and my ... | ⚠️ MEDIUM | ⚠️ MEDIUM | ✅ | Sore Throat (0.8%) | 75% |
| 7 | Male, 45, no conditions, no allergies | I have a high fever of 102, chills, body aches, and I have b... | ⚠️ MEDIUM | ⚠️ MEDIUM | ✅ | Sore Throat (0.75%) | 75% |
| 8 | Female, 52, diabetes, no allergies | I have a painful burning sensation when I urinate, lower abd... | ⚠️ MEDIUM | ✅ LOW | ❌ | Indigestion (0.8%) | 75% |
| 9 | Male, 22, asthma, no allergies | My asthma inhaler is not working, I am wheezing badly and ha... | ⚠️ MEDIUM | ⚠️ MEDIUM | ✅ | Asthma exacerbation (0.85%) | 85% |
| 10 | Female, 29, no conditions, no allergies | I have had a severe sore throat for 5 days with white patche... | ⚠️ MEDIUM | ⚠️ MEDIUM | ✅ | Sore Throat (0.95%) | 85% |
| 11 | Male, 32, no conditions, no allergies | I have a runny nose, sneezing, mild sore throat, and a sligh... | ✅ LOW | ✅ LOW | ✅ | Common Cold (0.95%) | 95% |
| 12 | Female, 28, seasonal allergies, no allergies to medication | My eyes are itchy and watery, I keep sneezing, and my nose i... | ✅ LOW | ✅ LOW | ✅ | Hay Fever (0.95%) | 95% |
| 13 | Male, 38, no conditions, no allergies | I have indigestion and heartburn after eating a large spicy ... | ✅ LOW | ✅ LOW | ✅ | Indigestion (0.95%) | 90% |
| 14 | Female, 24, no conditions, no allergies | I have a mild tension headache at the front of my head. No f... | ✅ LOW | ✅ LOW | ✅ | headache (0.95%) | 80% |
| 15 | Male, 50, no conditions, no allergies | I have mild lower back pain after lifting boxes yesterday. N... | ✅ LOW | ✅ LOW | ✅ | Muscle or ligament strain (0.9%) | 90% |
| 16 | Female, 35, diabetes, penicillin allergy | I have a fever and headache but no stiff neck, no chest pain... | ✅ LOW | ✅ LOW | ✅ | Fever (0.8%) | 75% |
| 17 | Male, 42, no conditions, no allergies | I am worried about meningitis because my friend has it but I... | ✅ LOW | ✅ LOW | ✅ | headache (0.75%) | 75% |
| 18 | Female, 60, hypertension, no allergies | I feel dizzy when I stand up quickly and I felt faint once t... | ⚠️ MEDIUM | ⚠️ MEDIUM | ✅ | Lightheadedness (0.8%) | 75% |
| 19 | Male, 19, no conditions, no allergies | aaa my stomch hrts rly bad | ⚠️ MEDIUM | ✅ LOW | ❌ | Indigestion (0.75%) | 75% |
| 20 | Female, 45, no conditions, no allergies | I have had nausea and vomiting for 24 hours and I cannot kee... | ⚠️ MEDIUM | ⚠️ MEDIUM | ✅ | Dehydration (0.85%) | 85% |

---

## NER Pipeline Performance

Shows what medspaCy extracted from each input — confirms clinical NER is working correctly.

| # | Input (short) | Symptoms Extracted | Negations Detected | NER Severity | RAG Chunks |
|---|---|---|---|---|---|
| 1 | I have sudden severe chest pain radiating to my le... | chest pain | none | HIGH | 5 |
| 2 | I have a sudden severe headache, high fever of 103... | headache, fever | none | LOW | 5 |
| 3 | I cannot breathe properly, my throat feels like it... | cannot breathe | none | HIGH | 5 |
| 4 | I passed out earlier and now I feel confused and d... | passed out, dizzy | none | HIGH | 5 |
| 5 | I am having a seizure, my whole body is shaking an... | seizure | none | HIGH | 5 |
| 6 | I have had ear pain for 3 days, mild fever of 100.... | pain, fever | none | LOW | 5 |
| 7 | I have a high fever of 102, chills, body aches, an... | fever, coughing | none | LOW | 5 |
| 8 | I have a painful burning sensation when I urinate,... | pain, fever | none | LOW | 5 |
| 9 | My asthma inhaler is not working, I am wheezing ba... | none | none | LOW | 5 |
| 10 | I have had a severe sore throat for 5 days with wh... | sore throat, fever | none | LOW | 5 |
| 11 | I have a runny nose, sneezing, mild sore throat, a... | sore throat, cough | fever | LOW | 5 |
| 12 | My eyes are itchy and watery, I keep sneezing, and... | none | fever | LOW | 5 |
| 13 | I have indigestion and heartburn after eating a la... | none | chest pain, fever | LOW | 5 |
| 14 | I have a mild tension headache at the front of my ... | headache | fever, stiff neck | LOW | 5 |
| 15 | I have mild lower back pain after lifting boxes ye... | pain | none | LOW | 5 |
| 16 | I have a fever and headache but no stiff neck, no ... | fever, headache | stiff neck, chest pain, difficulty breathing | LOW | 5 |
| 17 | I am worried about meningitis because my friend ha... | meningitis, headache | none | HIGH | 5 |
| 18 | I feel dizzy when I stand up quickly and I felt fa... | dizzy | none | LOW | 5 |
| 19 | aaa my stomch hrts rly bad | none | none | LOW | 5 |
| 20 | I have had nausea and vomiting for 24 hours and I ... | nausea | none | LOW | 5 |

---

## Case-by-Case Breakdown

### Case 1 ✅ — HIGH Risk
**Patient:** Male, 58, hypertension, no allergies
**Clinical Note:** Classic heart attack presentation
**Input:** I have sudden severe chest pain radiating to my left arm, I am sweating and feel short of breath

| Field | Value |
|---|---|
| Expected Risk | 🚨 HIGH |
| Actual Risk | 🚨 HIGH |
| Top Condition | Cardiac chest pain (heart-related — EMERGENCY) (0.95%) |
| Confidence Score | 95% |
| Symptoms Extracted | chest pain |
| Negations Detected | none |
| NER Severity | HIGH |
| RAG Chunks Retrieved | 5 |
| AI Summary | The patient is experiencing sudden, severe chest pain radiating to the left arm, accompanied by shortness of breath and sweating. This is a medical em... |

### Case 2 ✅ — HIGH Risk
**Patient:** Female, 25, no conditions, no allergies
**Clinical Note:** Classic bacterial meningitis triad
**Input:** I have a sudden severe headache, high fever of 103, my neck is very stiff and I am sensitive to light

| Field | Value |
|---|---|
| Expected Risk | 🚨 HIGH |
| Actual Risk | 🚨 HIGH |
| Top Condition | Meningitis (0.95%) |
| Confidence Score | 95% |
| Symptoms Extracted | headache, fever |
| Negations Detected | none |
| NER Severity | LOW |
| RAG Chunks Retrieved | 5 |
| AI Summary | The patient is experiencing a severe headache, high fever, and stiff neck, along with sensitivity to light. This presentation is highly concerning for... |

### Case 3 ✅ — HIGH Risk
**Patient:** Male, 40, no conditions, no allergies
**Clinical Note:** Anaphylaxis — airway emergency
**Input:** I cannot breathe properly, my throat feels like it is closing and my face is swelling up

| Field | Value |
|---|---|
| Expected Risk | 🚨 HIGH |
| Actual Risk | 🚨 HIGH |
| Top Condition | Severe sore throat with breathing difficulty and facial swelling (0.95%) |
| Confidence Score | 95% |
| Symptoms Extracted | cannot breathe |
| Negations Detected | none |
| NER Severity | HIGH |
| RAG Chunks Retrieved | 5 |
| AI Summary | The patient is experiencing a severe sore throat with difficulty breathing and facial swelling. This is a medical emergency and requires immediate att... |

### Case 4 ✅ — HIGH Risk
**Patient:** Female, 67, diabetes, aspirin allergy
**Clinical Note:** Possible stroke — FAST symptoms
**Input:** I passed out earlier and now I feel confused and dizzy, my speech feels strange

| Field | Value |
|---|---|
| Expected Risk | 🚨 HIGH |
| Actual Risk | 🚨 HIGH |
| Top Condition | Dizziness (0.9%) |
| Confidence Score | 80% |
| Symptoms Extracted | passed out, dizzy |
| Negations Detected | none |
| NER Severity | HIGH |
| RAG Chunks Retrieved | 5 |
| AI Summary | The patient is experiencing dizziness, confusion, and a feeling of passing out. These symptoms, especially when severe or accompanied by other concern... |

### Case 5 ✅ — HIGH Risk
**Patient:** Male, 30, no conditions, no allergies
**Clinical Note:** Active seizure — neurological emergency
**Input:** I am having a seizure, my whole body is shaking and I cannot control it

| Field | Value |
|---|---|
| Expected Risk | 🚨 HIGH |
| Actual Risk | 🚨 HIGH |
| Top Condition | Seizure (0.95%) |
| Confidence Score | 85% |
| Symptoms Extracted | seizure |
| Negations Detected | none |
| NER Severity | HIGH |
| RAG Chunks Retrieved | 5 |
| AI Summary | The patient is experiencing a seizure and has a severe headache, stiff neck, and sensitivity to light and noise. These symptoms, along with the seizur... |

### Case 6 ✅ — MEDIUM Risk
**Patient:** Female, 34, no conditions, penicillin allergy
**Clinical Note:** Ear infection — needs antibiotics
**Input:** I have had ear pain for 3 days, mild fever of 100.5, and my hearing feels muffled in my right ear

| Field | Value |
|---|---|
| Expected Risk | ⚠️ MEDIUM |
| Actual Risk | ⚠️ MEDIUM |
| Top Condition | Sore Throat (0.8%) |
| Confidence Score | 75% |
| Symptoms Extracted | pain, fever |
| Negations Detected | none |
| NER Severity | LOW |
| RAG Chunks Retrieved | 5 |
| AI Summary | The patient reports ear pain and a mild fever. While these symptoms are common and often resolve on their own, it's important to monitor them closely.... |

### Case 7 ✅ — MEDIUM Risk
**Patient:** Male, 45, no conditions, no allergies
**Clinical Note:** Possible bacterial respiratory infection
**Input:** I have a high fever of 102, chills, body aches, and I have been coughing for 4 days with yellow mucus

| Field | Value |
|---|---|
| Expected Risk | ⚠️ MEDIUM |
| Actual Risk | ⚠️ MEDIUM |
| Top Condition | Sore Throat (0.75%) |
| Confidence Score | 75% |
| Symptoms Extracted | fever, coughing |
| Negations Detected | none |
| NER Severity | LOW |
| RAG Chunks Retrieved | 5 |
| AI Summary | The patient reports a high fever, chills, body aches, and a cough with yellow mucus. The symptoms have lasted for 4 days. Based on the symptoms, a sor... |

### Case 8 ❌ — MEDIUM Risk
**Patient:** Female, 52, diabetes, no allergies
**Clinical Note:** UTI — diabetes increases complication risk
**Input:** I have a painful burning sensation when I urinate, lower abdominal pain, and a low fever for 2 days

| Field | Value |
|---|---|
| Expected Risk | ⚠️ MEDIUM |
| Actual Risk | ✅ LOW |
| Top Condition | Indigestion (0.8%) |
| Confidence Score | 75% |
| Symptoms Extracted | pain, fever |
| Negations Detected | none |
| NER Severity | LOW |
| RAG Chunks Retrieved | 5 |
| AI Summary | The patient is experiencing a painful burning sensation when urinating, lower abdominal pain, and a low fever for 2 days. These symptoms could be rela... |

### Case 9 ✅ — MEDIUM Risk
**Patient:** Male, 22, asthma, no allergies
**Clinical Note:** Asthma exacerbation — needs medical evaluation
**Input:** My asthma inhaler is not working, I am wheezing badly and having trouble breathing after exercise

| Field | Value |
|---|---|
| Expected Risk | ⚠️ MEDIUM |
| Actual Risk | ⚠️ MEDIUM |
| Top Condition | Asthma exacerbation (0.85%) |
| Confidence Score | 85% |
| Symptoms Extracted | none |
| Negations Detected | none |
| NER Severity | LOW |
| RAG Chunks Retrieved | 5 |
| AI Summary | The patient is experiencing an asthma exacerbation, indicated by wheezing and difficulty breathing after exercise. The patient's asthma inhaler is not... |

### Case 10 ✅ — MEDIUM Risk
**Patient:** Female, 29, no conditions, no allergies
**Clinical Note:** Likely strep throat — needs antibiotics
**Input:** I have had a severe sore throat for 5 days with white patches on my tonsils and fever of 101

| Field | Value |
|---|---|
| Expected Risk | ⚠️ MEDIUM |
| Actual Risk | ⚠️ MEDIUM |
| Top Condition | Sore Throat (0.95%) |
| Confidence Score | 85% |
| Symptoms Extracted | sore throat, fever |
| Negations Detected | none |
| NER Severity | LOW |
| RAG Chunks Retrieved | 5 |
| AI Summary | The patient reports a sore throat lasting 5 days with white patches on the tonsils and a fever of 101°F. The patient does not have any known allergies... |

### Case 11 ✅ — LOW Risk
**Patient:** Male, 32, no conditions, no allergies
**Clinical Note:** Common cold — home care appropriate
**Input:** I have a runny nose, sneezing, mild sore throat, and a slight cough for 2 days. No fever.

| Field | Value |
|---|---|
| Expected Risk | ✅ LOW |
| Actual Risk | ✅ LOW |
| Top Condition | Common Cold (0.95%) |
| Confidence Score | 95% |
| Symptoms Extracted | sore throat, cough |
| Negations Detected | fever |
| NER Severity | LOW |
| RAG Chunks Retrieved | 5 |
| AI Summary | The patient reports a runny nose, sneezing, mild sore throat, and a slight cough for 2 days. No fever. Based on the symptoms and the provided document... |

### Case 12 ✅ — LOW Risk
**Patient:** Female, 28, seasonal allergies, no allergies to medication
**Clinical Note:** Seasonal allergies — antihistamine appropriate
**Input:** My eyes are itchy and watery, I keep sneezing, and my nose is runny. No fever.

| Field | Value |
|---|---|
| Expected Risk | ✅ LOW |
| Actual Risk | ✅ LOW |
| Top Condition | Hay Fever (0.95%) |
| Confidence Score | 95% |
| Symptoms Extracted | none |
| Negations Detected | fever |
| NER Severity | LOW |
| RAG Chunks Retrieved | 5 |
| AI Summary | The patient is experiencing symptoms consistent with hay fever, including itchy watery eyes, sneezing, and a runny nose. No fever is reported.... |

### Case 13 ✅ — LOW Risk
**Patient:** Male, 38, no conditions, no allergies
**Clinical Note:** Indigestion — antacid appropriate
**Input:** I have indigestion and heartburn after eating a large spicy meal. No chest pain or fever.

| Field | Value |
|---|---|
| Expected Risk | ✅ LOW |
| Actual Risk | ✅ LOW |
| Top Condition | Indigestion (0.95%) |
| Confidence Score | 90% |
| Symptoms Extracted | none |
| Negations Detected | chest pain, fever |
| NER Severity | LOW |
| RAG Chunks Retrieved | 5 |
| AI Summary | The patient reports indigestion and heartburn after eating a large spicy meal. This is consistent with the symptoms of indigestion, which can be cause... |

### Case 14 ✅ — LOW Risk
**Patient:** Female, 24, no conditions, no allergies
**Clinical Note:** Tension headache — home care appropriate
**Input:** I have a mild tension headache at the front of my head. No fever, no stiff neck, no vision changes.

| Field | Value |
|---|---|
| Expected Risk | ✅ LOW |
| Actual Risk | ✅ LOW |
| Top Condition | headache (0.95%) |
| Confidence Score | 80% |
| Symptoms Extracted | headache |
| Negations Detected | fever, stiff neck |
| NER Severity | LOW |
| RAG Chunks Retrieved | 5 |
| AI Summary | The patient reports a mild headache. While the patient does not have fever or stiff neck, it is important to monitor for any worsening symptoms, espec... |

### Case 15 ✅ — LOW Risk
**Patient:** Male, 50, no conditions, no allergies
**Clinical Note:** Musculoskeletal back pain — rest and ice appropriate
**Input:** I have mild lower back pain after lifting boxes yesterday. No numbness, no bladder issues.

| Field | Value |
|---|---|
| Expected Risk | ✅ LOW |
| Actual Risk | ✅ LOW |
| Top Condition | Muscle or ligament strain (0.9%) |
| Confidence Score | 90% |
| Symptoms Extracted | pain |
| Negations Detected | none |
| NER Severity | LOW |
| RAG Chunks Retrieved | 5 |
| AI Summary | The patient reports mild lower back pain after lifting boxes yesterday. This is likely a muscle or ligament strain, which usually improves with home t... |

### Case 16 ✅ — LOW Risk
**Patient:** Female, 35, diabetes, penicillin allergy
**Clinical Note:** Negation test — should NOT escalate despite fever+headache
**Input:** I have a fever and headache but no stiff neck, no chest pain, no difficulty breathing

| Field | Value |
|---|---|
| Expected Risk | ✅ LOW |
| Actual Risk | ✅ LOW |
| Top Condition | Fever (0.8%) |
| Confidence Score | 75% |
| Symptoms Extracted | fever, headache |
| Negations Detected | stiff neck, chest pain, difficulty breathing |
| NER Severity | LOW |
| RAG Chunks Retrieved | 5 |
| AI Summary | You have a fever and headache. While these symptoms can be caused by various conditions, it's important to monitor them closely. If your symptoms wors... |

### Case 17 ✅ — LOW Risk
**Patient:** Male, 42, no conditions, no allergies
**Clinical Note:** Anxiety mention test — should not over-escalate
**Input:** I am worried about meningitis because my friend has it but I just have a slight headache and no other symptoms

| Field | Value |
|---|---|
| Expected Risk | ✅ LOW |
| Actual Risk | ✅ LOW |
| Top Condition | headache (0.75%) |
| Confidence Score | 75% |
| Symptoms Extracted | meningitis, headache |
| Negations Detected | none |
| NER Severity | HIGH |
| RAG Chunks Retrieved | 5 |
| AI Summary | The patient is concerned about meningitis due to a friend's illness. The patient reports only a mild headache. While the patient's symptoms are mild, ... |

### Case 18 ✅ — MEDIUM Risk
**Patient:** Female, 60, hypertension, no allergies
**Clinical Note:** Orthostatic hypotension in hypertensive patient — warrants evaluation
**Input:** I feel dizzy when I stand up quickly and I felt faint once this morning but I am fine now

| Field | Value |
|---|---|
| Expected Risk | ⚠️ MEDIUM |
| Actual Risk | ⚠️ MEDIUM |
| Top Condition | Lightheadedness (0.8%) |
| Confidence Score | 75% |
| Symptoms Extracted | dizzy |
| Negations Detected | none |
| NER Severity | LOW |
| RAG Chunks Retrieved | 5 |
| AI Summary | The patient reports feeling dizzy when standing up quickly and experiencing lightheadedness. This is likely due to orthostatic hypotension, which can ... |

### Case 19 ❌ — MEDIUM Risk
**Patient:** Male, 19, no conditions, no allergies
**Clinical Note:** Typo/informal input test — pipeline should still function
**Input:** aaa my stomch hrts rly bad

| Field | Value |
|---|---|
| Expected Risk | ⚠️ MEDIUM |
| Actual Risk | ✅ LOW |
| Top Condition | Indigestion (0.75%) |
| Confidence Score | 75% |
| Symptoms Extracted | none |
| Negations Detected | none |
| NER Severity | LOW |
| RAG Chunks Retrieved | 5 |
| AI Summary | The patient is experiencing severe indigestion, which is causing stomach pain. While indigestion is usually not serious, it is important to consult a ... |

### Case 20 ✅ — MEDIUM Risk
**Patient:** Female, 45, no conditions, no allergies
**Clinical Note:** Dehydration risk — needs medical evaluation
**Input:** I have had nausea and vomiting for 24 hours and I cannot keep any water down. I feel very weak.

| Field | Value |
|---|---|
| Expected Risk | ⚠️ MEDIUM |
| Actual Risk | ⚠️ MEDIUM |
| Top Condition | Dehydration (0.85%) |
| Confidence Score | 85% |
| Symptoms Extracted | nausea |
| Negations Detected | none |
| NER Severity | LOW |
| RAG Chunks Retrieved | 5 |
| AI Summary | The patient is experiencing nausea and vomiting for 24 hours, with inability to keep any liquids down, and feels weak. The patient has a high fever ab... |

---

## Methodology

Each test case runs through the complete MediTriage pipeline: medspaCy clinical NER → preprocessing → LangChain RAG retrieval from ChromaDB (indexed from MedlinePlus and CDC sources) → MedGemma LLM inference via Ollama → risk triage engine.

Expected risk tiers were assigned based on standard clinical triage guidelines. HIGH = emergency requiring immediate care or 911. MEDIUM = requires physician evaluation within 24 hours. LOW = manageable with home care and self-monitoring.

This evaluation is not a clinical validation study. It demonstrates the pipeline's reasoning capability across diverse symptom presentations. MediTriage is a triage routing tool — not a diagnostic device — and requires clinical oversight before any real-world deployment.

---
*Generated by MediTriage evaluation pipeline — CareDevi Hackathon 2026*