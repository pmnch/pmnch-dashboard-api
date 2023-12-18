"""
MIT License

Copyright (c) 2023 White Ribbon Alliance. Maintainers: Thomas Wood, https://fastdatascience.com, Zairon Jacobs, https://zaironjacobs.com.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import os
from functools import lru_cache

from pydantic import BaseSettings

from app.enums.api_prefix import ApiPrefix

STAGE = os.getenv("STAGE", "prod")

if os.path.isfile("credentials.json"):
    GOOGLE_CREDENTIALS_INCLUDED = True
else:
    GOOGLE_CREDENTIALS_INCLUDED = False


class Settings(BaseSettings):
    STAGE: str = STAGE
    HOST: str = os.getenv("HOST")
    PORT: int = int(os.getenv("PORT", 8000))
    VERSION: str = "1.0.0"
    APP_TITLE: str = os.getenv("APP_TITLE", "")
    APP_DESCRIPTION: str = os.getenv("APP_DESCRIPTION", "")
    API_PREFIX: str = ApiPrefix.v1.value
    GOOGLE_CLOUD_STORAGE_BUCKET_NAME = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET_NAME", "")
    ACCESS_TOKEN_SECRET_KEY: str = os.getenv("ACCESS_TOKEN_SECRET_KEY")
    TRANSLATIONS_ENABLED: bool = os.getenv("TRANSLATIONS_ENABLED", "").lower() == "true"
    NEWRELIC_API_KEY: str = os.getenv("NEWRELIC_API_KEY", "")
    NEW_RELIC_URL: str = os.getenv("NEW_RELIC_URL", "")
    GOOGLE_CREDENTIALS_INCLUDED: bool = GOOGLE_CREDENTIALS_INCLUDED

    # These env variables are only used for legacy campaign pmn01a
    ONLY_PMNCH: bool = os.getenv("ONLY_PMNCH", "").lower() == "true"
    AZURE_TRANSLATOR_KEY: str = os.getenv("AZURE_TRANSLATOR_KEY")
    AZURE_STORAGE_CONNECTION_STRING: str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    AZURE_STORAGE_ACCOUNT_KEY: str = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
    AZURE_STORAGE_ACCOUNT_NAME: str = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")

    ONLY_LEGACY_CAMPAIGNS: bool = (
        os.getenv("ONLY_LEGACY_CAMPAIGNS", "").lower() == "true"
    )
    GOOGLE_MAPS_API_KEY: str = os.getenv("GOOGLE_MAPS_API_KEY")


class DevSettings(Settings):
    DEBUG: bool = True
    RELOAD: bool = True
    CORS: dict = {
        "allow_origins": [
            "http://localhost",
            "http://localhost:3000",
            "http://explore.whiteribbonalliance.local:3000",
            "http://whatyoungpeoplewant.whiteribbonalliance.local:3000",
        ],
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    }


class ProdSettings(Settings):
    DEBUG: bool = False
    RELOAD: bool = False
    CORS: dict = {
        "allow_origins": [
            "https://explore.whiteribbonalliance.org",
            "https://whatwomenwant.whiteribbonalliance.org",
            "https://whatyoungpeoplewant.whiteribbonalliance.org",
            "https://midwivesvoices.whiteribbonalliance.org",
            "https://admin.whiteribbonalliance.org",
            "https://pmnch-front.azurewebsites.net",
            "https://wypw.1point8b.org",
        ],
        "allow_credentials": True,
        "allow_methods": ["GET", "POST", "OPTIONS", "HEAD"],
        "allow_headers": [
            "Access-Control-Allow-Headers",
            "Access-Control-Allow-Methods",
            "Access-Control-Allow-Credentials",
            "Access-Control-Allow-Origin",
            "Access-Control-Max-Age",
            "Authorization",
            "Content-Type",
            "Set-Cookie",
        ],
    }


@lru_cache()
def get_settings():
    if STAGE == "dev":
        return DevSettings()
    else:
        return ProdSettings()
