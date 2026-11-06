from app.services.llm_service import extract_symptoms
from app.schemas.symptom import Finding


ESCALATION_SIGNS = {
    "froth_nose_mouth",
    "unable_to_stand",
    "cloudy_eye"
}


def process_message(message: str):

    raw_findings = extract_symptoms(message)

    findings = [
        Finding.model_validate(item)
        for item in raw_findings
    ]

    escalate = any(
        finding.sign_id.value in ESCALATION_SIGNS
        and finding.value.value in {"yes", "not_sure"}
        for finding in findings
    )

    if escalate:
        reason = (
            "One or more escalation signs were detected "
            "or reported as uncertain."
        )
    else:
        reason = "No escalation signs were identified."

    return {
        "findings": [
            finding.model_dump(mode="json")
            for finding in findings
        ],
        "escalate": escalate,
        "reason": reason
    }
