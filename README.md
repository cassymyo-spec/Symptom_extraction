# V-Vet Symptom Extraction Service

A small Python API that extracts structured livestock health findings from farmers' natural-language messages.

Built with FastAPI, Python, Pydantic and Groq LLM.

## 1. Overview

Farmers often describe animal health problems using their own words, including local language expressions and combinations of Shona and English.

This service uses a Large Language Model (LLM) to identify relevant symptoms and convert them into structured findings.

It exposes one endpoint:

`POST /extract`

The service also applies deterministic escalation rules using Python rather than relying on the LLM to make escalation decisions.

## 2. Technology Stack

- Python
- FastAPI
- Groq API
- GPT-OSS 20B
- Pydantic
- Pytest
- HTTPX

## 3. Project Structure

```
v-vet/
│
├── app/
│   ├── main.py
│   ├── api/
│   │   └── routes.py
│   ├── services/
│   │   ├── llm_service.py
│   │   └── extraction_service.py
│   ├── schemas/
│   │   └── symptom.py
│   └── core/
│       └── config.py
│
├── tests/
│   └── test_extraction.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 4. Setup and Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd v-vet
```

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
```

A Groq API key is required to perform actual symptom extraction.

## 5. Running the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

## 6. API Usage

### Endpoint

`POST /extract`

### Request

```json
{
  "message": "My cow has not been eating since yesterday and she is breathing very fast."
}
```

### Example Response

```json
{
  "findings": [
    {
      "sign_id": "reduced_appetite",
      "value": "yes",
      "quote": "has not been eating since yesterday"
    },
    {
      "sign_id": "rapid_breathing",
      "value": "yes",
      "quote": "breathing very fast"
    }
  ],
  "escalate": false,
  "reason": "No escalation signs were identified."
}
```

## 7. Design Decisions

### LLM-based extraction

Groq is used to process farmers' natural-language messages and identify symptoms.

The model is instructed to:

- Extract only explicitly mentioned signs.
- Recognise English and Shona-English expressions.
- Return supporting quotes from the original message.
- Use `yes`, `no` or `not_sure`.
- Avoid diagnosing diseases.

### Data validation

Pydantic models and enumerations restrict the response to the nine approved sign IDs and three permitted finding values.

This prevents unsupported sign identifiers and invalid values from entering the response.

### Deterministic escalation

Escalation is handled entirely in Python.

The service escalates when any of the following signs has a value of `yes` or `not_sure`:

- `froth_nose_mouth`
- `unable_to_stand`
- `cloudy_eye`

This separates symptom extraction from escalation decisions and ensures the rules remain predictable.

### Evidence-based findings

Each finding includes a supporting quote from the farmer's message.

This makes it easier to review why a particular symptom was extracted.

## 8. Testing

Tests are implemented using Pytest and FastAPI's TestClient.

The Groq service is mocked during testing, meaning the tests do not require:

- An internet connection.
- A Groq API key.
- Actual LLM requests.

Run tests:

```bash
pytest -v
```

The tests cover:

- Reduced appetite and rapid breathing.
- Froth from the nose and inability to stand.
- Uncertain cloudy eyes.
- Swelling.
- Ticks without escalation.
- Red urine and reduced appetite.
- Empty message validation.

The tests verify API behaviour and deterministic escalation logic. They do not measure the actual LLM's extraction accuracy.

## 9. Measuring Extraction Accuracy

I would develop a manually reviewed dataset containing real or representative livestock health messages.

Each message would have veterinarian- or domain-expert-annotated findings.

I would evaluate:

- **Precision:** How often extracted symptoms are correct.
- **Recall:** How often symptoms mentioned in messages are successfully identified.
- **F1 Score:** A balance between precision and recall.

I would also measure:

- Correct classification of `yes`, `no` and `not_sure`.
- Accuracy of supporting quotes.
- Correct escalation decisions.
- Performance on Shona-English messages.
- Invalid or unsupported symptom extraction.

Special attention would be given to false negatives involving escalation signs.

## 10. Future Improvements

With more development time, I would:

1. Build a larger multilingual livestock symptom dataset.
2. Improve extraction accuracy using structured LLM outputs.
3. Add more comprehensive tests for negation and ambiguous expressions.
4. Introduce request logging and monitoring.
5. Add retry handling and timeouts for LLM requests.
6. Evaluate different models for accuracy, latency and cost.
7. Work with veterinary professionals to validate extraction rules.

The service is intended to structure reported symptoms, not diagnose animals or replace veterinary assessment.

## 11. AI Assistance Disclosure

ChatGPT was used as a development assistant to help with:

- FastAPI implementation guidance.
- Pydantic schema design.
- Pytest test development.

Developer: Casper Moyo  
Project: V-Vet Symptom Extraction Service  
Framework: FastAPI
# Symptom_extraction
