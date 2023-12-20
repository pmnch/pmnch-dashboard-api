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
from typing import Optional

from pydantic import BaseModel, Field, validator

from app.schemas.category import ParentCategory


class CampaignConfigBase(BaseModel):
    campaign_code: str = Field(
        min_length=1,
        description="The campaign code. This value should be unique per campaign.",
    )
    dashboard_path: str = Field(
        description="The dashboard path that will be used to access it in the front. This value should be unique per campaign."
    )
    seo_title: str = Field(description="Title of the dashboard for SEO.")
    seo_meta_description: str = Field(
        description="A description of the dashboard for SEO."
    )
    respondent_noun_singular: str = Field(
        min_length=1, default="respondent", description="Respondent noun singular."
    )
    respondent_noun_plural: str = Field(
        min_length=1, default="respondents", description="Respondent noun plural."
    )
    video_link: str = Field(
        default="", description="A Link to a video related to the dashboard."
    )
    about_us_link: str = Field(
        default="", description="Link to a page about the campaign."
    )

    @validator("dashboard_path", pre=True)
    def dashboard_path_check(cls, v: str):
        if not v or " " in v:
            raise Exception("Invalid dashboard path provided.")

        return v


class File(BaseModel):
    local: Optional[str] = Field(default=None, description="Local file name.")
    link: Optional[str] = Field(default=None, description="Direct link to file.")
    cloud: Optional[str] = Field(default=None, description="Blob name.")


class CampaignConfigInternal(CampaignConfigBase):
    password: str = Field(default="", description="Password to access protected paths.")
    file: File = Field("Where to find the CSV file.")
    filepath: str = Field(
        default="",
        description="Local path to the CSV file. This field will be filled automatically while loading the config.",
    )
    parent_categories: list[ParentCategory] = Field(
        description="A hierarchy of categories."
    )
    questions: dict[str, str] = Field(
        description="Questions that were asked to respondents."
    )

    @validator("questions", pre=True)
    def question_check(cls, v):
        for key, value in v.items():
            if not key.startswith("q") or not key.replace("q", "", 1).isnumeric():
                raise Exception("Invalid question code provided.")

        return v


class CampaignConfigResponse(CampaignConfigBase):
    pass
