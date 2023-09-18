"""BigQuery interactions"""

import logging
import os

from google.cloud import bigquery
from google.cloud import bigquery_storage
from google.oauth2 import service_account
from pandas import DataFrame
import pandas as pd
from app.enums.campaign_code import CampaignCode
from app.logginglib import init_custom_logger

logger = logging.getLogger(__name__)
init_custom_logger(logger)

table_name = "wra_prod.responses"


def get_bigquery_client() -> bigquery.Client:
    """Get BigQuery client"""

    credentials = service_account.Credentials.from_service_account_file(
        filename="credentials.json",
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    return bigquery.Client(
        credentials=credentials,
        project=credentials.project_id,
    )


def get_bigquery_storage_client() -> bigquery_storage.BigQueryReadClient:
    """Get BigQuery storage client"""

    credentials = service_account.Credentials.from_service_account_file(
        filename="credentials.json",
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    return bigquery_storage.BigQueryReadClient(credentials=credentials)


def get_campaign_df_from_bigquery(campaign_code: CampaignCode) -> DataFrame:
    """
    Get the dataframe of a campaign from BigQuery

    :param campaign_code: The campaign code
    """

    # Load from .pkl file
    if os.getenv("LOAD_FROM_LOCAL_PKL_FILE", "").lower() == "true":
        return pd.read_pickle(f"{campaign_code.value}.pkl")

    bigquery_client = get_bigquery_client()

    # Use BigQuery Storage client for faster results to dataframe
    bigquery_storage_client = get_bigquery_storage_client()

    # Set minimum age
    if campaign_code == CampaignCode.what_young_people_want:
        min_age = "10"
    elif campaign_code == CampaignCode.healthwellbeing:
        min_age = "0"
    else:
        min_age = "15"

    query_job = bigquery_client.query(
        f"""
        SELECT CASE WHEN response_english_text IS null THEN response_original_text ELSE CONCAT(response_original_text, ' (', response_english_text, ')')  END as q1_raw_response,
        response_original_lang as q1_original_language,
        response_nlu_category AS q1_canonical_code,
        response_lemmatized_text as q1_lemmatized,
        respondent_country_code as alpha2country,
        respondent_region_name as region,
        coalesce(cast(respondent_age as string),respondent_age_bucket) as age,
        REGEXP_REPLACE(REGEXP_REPLACE(INITCAP(respondent_gender), 'Twospirit', 'Two Spirit'), 'Unspecified', 'Prefer Not To Say') as gender,
        ingestion_time as ingestion_time,
        JSON_VALUE(respondent_additional_fields.data_source) as data_source,
        JSON_VALUE(respondent_additional_fields.profession) as profession,
        JSON_VALUE(respondent_additional_fields.setting) as setting,
        respondent_additional_fields as additional_fields,
        FROM deft-stratum-290216.{table_name}
        WHERE campaign = '{campaign_code.value}'
        AND response_original_text is not null
        AND (respondent_age >= {min_age} OR respondent_age is null)
        AND respondent_country_code is not null
        AND response_nlu_category is not null
        AND response_lemmatized_text is not null
        AND LENGTH(response_original_text) > 3
       """
    )

    results = query_job.result()

    df_responses = results.to_dataframe(bqstorage_client=bigquery_storage_client)

    # Save to .pkl file
    if os.getenv("SAVE_TO_PKL_FILE", "").lower() == "true":
        df_responses.to_pickle(f"{campaign_code.value}.pkl")

    return df_responses
