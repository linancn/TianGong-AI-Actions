import json
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Source(BaseModel):
    uuid: str = Field(..., alias="uuid")
    short_name: json = Field(..., alias="short_name")
    classification: json = Field(..., alias="classification")
    source_citation: str = Field(..., alias="source_citation")
    pulication_type: str = Field(..., alias="pulication_type")
    source_description_comment: json = Field(..., alias="source_description_comment")
    belongs_to: json = Field(..., alias="belongs_to")
    time_stamp_last_saved: datetime = Field(..., alias="time_stamp_last_saved")
    data_set_format: json = Field(..., alias="data_set_format")
    data_set_version: str = Field(..., alias="data_set_version")
    preceding_data_set_version: json = Field(..., alias="preceding_data_set_version")
    permanent_data_set_uri: str = Field(..., alias="permanent_data_set_uri")
    owner_of_data_set: json = Field(..., alias="owner_of_data_set")
    logo_of_organisation_or_source: json = Field(
        ..., alias="logo_of_organisation_or_source"
    )
    schema_version: str = Field(..., alias="schema_version")
    reference_file: List[str] = Field(..., alias="reference_file")
    link_to_digital_file: json = Field(..., alias="link_to_digital_file")
