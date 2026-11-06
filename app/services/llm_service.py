import json

from groq import Groq

from app.core.config import settings
from app.schemas.symptom import Finding


client = Groq(api_key=settings.GROQ_API_KEY)


SYSTEM_PROMPT = """
IMPORTANT: Return your response in valid JSON format.
Your response must contain a JSON object with a "findings" array.
Do not include Markdown or explanations outside the JSON.

STRICT OUTPUT STRUCTURE:
Every finding MUST contain exactly these three fields:
- sign_id: one of the approved sign IDs.
- value: "yes", "no", or "not_sure".
- quote: the exact supporting text from the farmer's message.

Use this JSON structure:
{
  "findings": [
    {
      "sign_id": "reduced_appetite",
      "value": "yes",
      "quote": "not eating properly"
    }
  ]
}

Do not use alternative field names such as "sign", "symptom",
"status", or "answer".
Never omit sign_id, value, or quote.

You are a livestock symptom extraction assistant.

Your task is to extract explicitly mentioned symptoms
from farmers' messages.

The approved signs are:

1. reduced_appetite:
Eating less or stopped eating/grazing.

2. weakness:
Dull, weak, lying down more than usual.

3. swelling:
Lump below the ear, under the jaw, or in front
of the shoulder. May be called mbandabvu.

4. rapid_breathing:
Breathing fast while resting.

5. cloudy_eye:
Eye looks white, grey or milky.

6. froth_nose_mouth:
Foam or froth from the nose or mouth.

7. red_urine:
Urine is red, brown or dark like strong tea.

8. unable_to_stand:
Cannot get up or stay standing.

9. ticks:
Ticks can be seen on the animal.

RULES:

- Only extract signs explicitly mentioned.
- Never invent symptoms.
- Use yes when the sign is explicitly present.
- Use no when the farmer explicitly denies the sign.
- Use not_sure when the farmer expresses uncertainty.
- Do not include signs that were not mentioned.
- Understand English and Shona expressions.
- Recognise mbandabvu as swelling when the location
  matches the description.
- Every finding must include an exact supporting quote
  from the farmer's message.
- Do not diagnose diseases.
"""


def extract_symptoms(message: str) -> list[Finding]:

    response = client.chat.completions.create(

        model=settings.GROQ_MODEL,

        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": message
            }
        ],

        response_format={
            "type": "json_object"
        },

        temperature=0
    )

    content = response.choices[0].message.content

    data = json.loads(content)

    return [
        Finding.model_validate(item)
        for item in data["findings"]
    ]
