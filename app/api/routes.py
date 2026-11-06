from fastapi import APIRouter, HTTPException

from app.schemas.symptom import (
    ExtractionRequest,
    ExtractionResponse
)

from app.services.extraction_service import process_message


router = APIRouter()

import logging

logger = logging.getLogger(__name__)

@router.post("/extract", response_model=ExtractionResponse)
def extract(request: ExtractionRequest):
    try:
        return process_message(request.message)
    except Exception as error:
        logger.exception("Symptom extraction failed")
        raise HTTPException(
            status_code=502,
            detail="Symptom extraction service failed."
        ) from error
