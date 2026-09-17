import json
from pathlib import Path
from typing import Dict, List, Optional
from agent.models import Person, CalendarEvent, Email, VoiceNote, MeetingTranscript

#DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
# Always anchors to the repo root regardless of current working directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

_PEOPLE_CACHE: Optional[List[Person]] = None
_CALENDARS_CACHE: Optional[Dict[str, List[CalendarEvent]]] = None
_EMAILS_CACHE: Optional[List[Email]] = None
_VOICE_NOTES_CACHE: Optional[List[VoiceNote]] = None
_TRANSCRIPTS_CACHE: Optional[List[MeetingTranscript]] = None

def load_people() -> List[Person]:
    global _PEOPLE_CACHE
    if _PEOPLE_CACHE is None:
        with open(DATA_DIR / "people.json", "r") as f:
            _PEOPLE_CACHE = [Person(**p) for p in json.load(f)]
    return _PEOPLE_CACHE

def load_calendars() -> Dict[str, List[CalendarEvent]]:
    global _CALENDARS_CACHE
    if _CALENDARS_CACHE is None:
        with open(DATA_DIR / "calendars.json", "r") as f:
            raw = json.load(f)
            _CALENDARS_CACHE = {
                person: [CalendarEvent(**ev) for ev in events]
                for person, events in raw.items()
            }
    return _CALENDARS_CACHE

def load_emails() -> List[Email]:
    global _EMAILS_CACHE
    if _EMAILS_CACHE is None:
        with open(DATA_DIR / "emails.json", "r") as f:
            _EMAILS_CACHE = [Email(**e) for e in json.load(f)]
    return _EMAILS_CACHE

def load_voice_notes() -> List[VoiceNote]:
    global _VOICE_NOTES_CACHE
    if _VOICE_NOTES_CACHE is None:
        with open(DATA_DIR / "voice_notes.json", "r") as f:
            _VOICE_NOTES_CACHE = [VoiceNote(**v) for v in json.load(f)]
    return _VOICE_NOTES_CACHE

def load_transcripts() -> List[MeetingTranscript]:
    global _TRANSCRIPTS_CACHE
    if _TRANSCRIPTS_CACHE is None:
        with open(DATA_DIR / "meeting_transcripts.json", "r") as f:
            _TRANSCRIPTS_CACHE = [MeetingTranscript(**t) for t in json.load(f)]
    return _TRANSCRIPTS_CACHE

def get_latest_email_in_thread(thread_name: str) -> Optional[Email]:
    """Deterministic recency resolution: returns the latest email in a thread by seq."""
    thread_emails = [e for e in load_emails() if e.thread.lower() == thread_name.lower()]
    if not thread_emails:
        return None
    return max(thread_emails, key=lambda e: e.seq)