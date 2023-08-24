import re

from app import constants
from app.constants import CAMPAIGN_CODES
from app.enums.campaign_code import CampaignCode
from app.enums.question_code import QuestionCode


def contains_letters(text: str):
    """Check if a string contains letters"""

    if type(text) is str:
        return re.search(r"[a-zA-Z]", text)


def divide_list_into_chunks(my_list: list, n: int):
    """divide list into chunks"""

    def divide():
        for i in range(0, len(my_list), n):
            yield my_list[i : i + n]

    return list(divide())


def get_campaign_q_codes(campaign_code: CampaignCode) -> list[QuestionCode]:
    """Get campaign question codes"""

    # All campaigns have q1
    q_codes = [QuestionCode.q1]

    # Campaign economic_empowerment_mexico has q2
    if campaign_code == CampaignCode.economic_empowerment_mexico:
        q_codes.append(QuestionCode.q2)

    return q_codes


def check_language(lang: str) -> str:
    """Check if language exists, If not, default to 'en'"""

    if lang in constants.TRANSLATION_LANGUAGES:
        return lang
    else:
        return "en"


def check_campaign(campaign: str) -> CampaignCode:
    """Check if campaign exists and return its campaign code"""

    if campaign.lower() in [c.lower() for c in CAMPAIGN_CODES]:
        for campaign_code in CampaignCode:
            if campaign_code.value == campaign:
                return campaign_code