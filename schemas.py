from pydantic import BaseModel
from typing import List, Optional

class Issue(BaseModel):
    description: str
    severity: Optional[str]
    source: str
    image: Optional[str]

class AreaObservation(BaseModel):
    area: str
    issues: List[Issue]

class DDRReport(BaseModel):
    property_issue_summary: str
    area_wise_observations: List[AreaObservation]
    probable_root_cause: str
    severity_assessment: str
    recommended_actions: List[str]
    additional_notes: str
    missing_or_unclear_information: List[str]