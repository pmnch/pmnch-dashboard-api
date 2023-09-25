from fastapi import Request
from pydantic import BaseModel

from app.enums.campaign_code import CampaignCode
from app.enums.question_code import QuestionCode


class CommonParametersCampaign(BaseModel):
    campaign_code: CampaignCode
    language: str
    request: Request | None
    q_code: QuestionCode
    response_year: str

    class Config:
        arbitrary_types_allowed = True
