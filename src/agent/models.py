from typing import Optional, List
from pydantic import BaseModel, Field,ConfigDict

class Person(BaseModel):
    name: str
    role: str
    email: str
    is_user: bool = False

class CalendarEvent(BaseModel):
    day: str
    time: str
    event: str

class Email(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    thread: str
    seq: int
    datetime: str
    from_: str = Field(..., alias="from")
    to: List[str]
    body: str


class VoiceNote(BaseModel):
    id: str
    datetime: str
    context: str
    note: str
    text: str

class TranscriptUtterance(BaseModel):
    speaker: str
    text: str

class MeetingTranscript(BaseModel):
    id: str
    title: str
    date: str
    time: str
    attendees: List[str]
    utterances: List[TranscriptUtterance]

class BriefingItem(BaseModel):
    description: str
    owner: str
    counterparty: Optional[str] = None
    deadline: Optional[str] = None
    status: str
    source_refs: List[str]

class AgentResponse(BaseModel):
    answer: str
    citations: List[str] = Field(default_factory=list)
    reasoning_trace: List[str] = Field(default_factory=list)