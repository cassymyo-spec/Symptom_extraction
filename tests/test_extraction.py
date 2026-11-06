
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def mock_llm(findings):
    return findings


@patch("app.services.extraction_service.extract_symptoms")
def test_reduced_appetite_and_rapid_breathing(mock_extract):

    mock_extract.return_value = [
        {
            "sign_id": "reduced_appetite",
            "value": "yes",
            "quote": "has not been eating"
        },
        {
            "sign_id": "rapid_breathing",
            "value": "yes",
            "quote": "breathing very fast"
        }
    ]

    response = client.post("/extract", json={
        "message": "My cow has not been eating and is breathing very fast."
    })

    assert response.status_code == 200
    assert response.json()["escalate"] is False
    assert len(response.json()["findings"]) == 2


@patch("app.services.extraction_service.extract_symptoms")
def test_froth_and_unable_to_stand_escalates(mock_extract):

    mock_extract.return_value = [
        {
            "sign_id": "froth_nose_mouth",
            "value": "yes",
            "quote": "foam coming from her nose"
        },
        {
            "sign_id": "unable_to_stand",
            "value": "yes",
            "quote": "can't get up"
        }
    ]

    response = client.post("/extract", json={
        "message": "There's foam coming from her nose and she can't get up."
    })

    assert response.status_code == 200
    assert response.json()["escalate"] is True


@patch("app.services.extraction_service.extract_symptoms")
def test_uncertain_cloudy_eye_escalates(mock_extract):

    mock_extract.return_value = [
        {
            "sign_id": "cloudy_eye",
            "value": "not_sure",
            "quote": "eyes look a bit cloudy but I'm not sure"
        },
        {
            "sign_id": "swelling",
            "value": "yes",
            "quote": "mbandabvu under the ear"
        }
    ]

    response = client.post("/extract", json={
        "message": "I think the eyes look a bit cloudy but I'm not sure."
    })

    assert response.status_code == 200
    assert response.json()["escalate"] is True


@patch("app.services.extraction_service.extract_symptoms")
def test_ticks_without_escalation_signs(mock_extract):

    mock_extract.return_value = [
        {
            "sign_id": "ticks",
            "value": "yes",
            "quote": "lots of ticks on the ears"
        }
    ]

    response = client.post("/extract", json={
        "message": "The calf is fine, just lots of ticks on the ears."
    })

    assert response.status_code == 200
    assert response.json()["escalate"] is False


@patch("app.services.extraction_service.extract_symptoms")
def test_red_urine_and_reduced_appetite(mock_extract):

    mock_extract.return_value = [
        {
            "sign_id": "reduced_appetite",
            "value": "yes",
            "quote": "Mombe yangu haisi kudya"
        },
        {
            "sign_id": "red_urine",
            "value": "yes",
            "quote": "her urine is dark like tea"
        }
    ]

    response = client.post("/extract", json={
        "message": "Mombe yangu haisi kudya, and her urine is dark like tea."
    })

    assert response.status_code == 200
    assert response.json()["escalate"] is False
    assert len(response.json()["findings"]) == 2


def test_empty_message_is_rejected():

    response = client.post("/extract", json={
        "message": ""
    })

    assert response.status_code == 422
