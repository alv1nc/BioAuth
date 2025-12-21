from pydantic import BaseModel
from typing import List,Optional,Any,Dict

class RegistrationResponse(BaseModel):
    user_id: str
    status: str
    message: str

class VerificationResponse(BaseModel):
    authorized: bool
    face_score: float
    voice_score: float
    metadata: Optional[Dict[str,Any]] = None
    message: str

class IdentificationResponse(BaseModel):
    identified: bool
    best_match_user_id: Optional[str] = None
    face_score: float
    voice_score: float
    metadata: Optional[Dict[str, Any]] = None
    message: str


class UserSummary(BaseModel):
    user_id: str
    is_active: bool
    created_at: str
    metadata: Optional[Dict[str, Any]] = None

class UserListResponse(BaseModel):
    total_users: int
    users: List[UserSummary]

class DeleteResponse(BaseModel):
    user_id: str
    deleted: bool
    mode: str  # "Soft Delete" or "Hard Delete"
    message: str

class LogEntry(BaseModel):
    id: int
    timestamp: str
    user_id: Optional[str]
    status: str
    face_score: float
    voice_score: float

class LogListResponse(BaseModel):
    logs: List[LogEntry]


class HelthResponse(BaseModel):
    status: str
    service: str
