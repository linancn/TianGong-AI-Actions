from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Source(BaseModel):
    belongs_to: Optional[Dict[str, Any]] = None
    classification: Optional[List[Dict[str, Any]]] = None
    data_set_format: Optional[List[Dict[str, Any]]] = None
    data_set_version: Optional[str] = None
    link_to_digital_file: Optional[List[str]] = None
    logo_of_organisation_or_source: Optional[Dict[str, Any]] = None
    owner_of_data_set: Optional[Dict[str, Any]] = None
    permanent_data_set_uri: Optional[str] = None
    preceding_data_set_version: Optional[Dict[str, Any]] = None
    pulication_type: Optional[str] = None
    schema_version: Optional[str] = None
    short_name: Optional[List[Dict[str, Any]]] = None
    source_citation: Optional[str] = None
    source_description_comment: Optional[Dict[str, Any]] = None
    time_stamp_last_saved: Optional[datetime] = None
    uuid: str = Field(...)
