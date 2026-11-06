from enum import Enum
from pydantic import BaseModel, Field


class SignValue(str, Enum):
    YES = "yes"
    NO = "no"
    NOT_SURE = "not_sure"


class SignID(str, Enum):
    REDUCED_APPETITE = "reduced_appetite"
    WEAKNESS = "weakness"
    SWELLING = "swelling"
    RAPID_BREATHING = "rapid_breathing"
    CLOUDY_EYE = "cloudy_eye"
    FROTH_NOSE_MOUTH = "froth_nose_mouth"
    RED_URINE = "red_urine"
    UNABLE_TO_STAND = "unable_to_stand"
    TICKS = "ticks"


class Finding(BaseModel):
    sign_id: SignID
    value: SignValue
    quote: str


class ExtractionRequest(BaseModel):
    message: str = Field(min_length=1, max_length=5000)


class ExtractionResponse(BaseModel):
    findings: list[Finding]
    escalate: bool
    reason: str
