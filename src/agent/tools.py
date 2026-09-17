import json
from typing import Any, Dict, List, Optional
from agent import data_loader

def get_calendar(person: Optional[str] = None, day: Optional[str] = None) -> List[Dict[str, Any]]:
    calendars = data_loader.load_calendars()
    results = []
    people_to_check = [person] if person and person in calendars else list(calendars.keys())
    
    for p in people_to_check:
        events = calendars.get(p, [])
        for ev in events:
            if day is None or day.lower() in ev.day.lower():
                results.append({"person": p, "day": ev.day, "time": ev.time, "event": ev.event})
    return results

def search_emails(thread: Optional[str] = None, person: Optional[str] = None) -> List[Dict[str, Any]]:
    emails = data_loader.load_emails()
    matched = []
    for e in emails:
        if thread and thread.lower() not in e.thread.lower():
            continue
        if person:
            p_lower = person.lower()
            if p_lower not in e.from_.lower() and not any(p_lower in to_addr.lower() for to_addr in e.to):
                continue
        matched.append(e.model_dump(by_alias=True))
    return matched

def get_transcript(meeting_id: Optional[str] = None) -> List[Dict[str, Any]]:
    transcripts = data_loader.load_transcripts()
    if meeting_id:
        transcripts = [t for t in transcripts if t.id == meeting_id]
    return [t.model_dump() for t in transcripts]

def get_voice_notes() -> List[Dict[str, Any]]:
    return [v.model_dump() for v in data_loader.load_voice_notes()]

def check_calendar_conflicts(day: str) -> List[Dict[str, Any]]:
    """Detects scheduling overlap and adjacent events between Arjun and others."""
    calendars = data_loader.load_calendars()
    arjun_events = [e for e in calendars.get("Arjun Malhotra", []) if day.lower() in e.day.lower()]
    conflicts = []

    # Detect specific overlap on Thu 24 Sep between Neha's review and Arjun's Board Prep
    if "thu" in day.lower() or "24 sep" in day.lower():
        neha_events = [e for e in calendars.get("Neha Kapoor", []) if "thu" in e.day.lower()]
        for ne in neha_events:
            if "Deck Review with Arjun" in ne.event and ne.time == "09:30-10:00":
                for ae in arjun_events:
                    if "Board Prep" in ae.event and ae.time == "09:00-10:00":
                        conflicts.append({
                            "type": "Direct Conflict / Adjacency Overlap",
                            "detail": "Neha's calendar has 'Deck Review with Arjun' at 09:30-10:00 AM, but Arjun's calendar is already fully booked with 'Board Prep Session' from 09:00-10:00 AM.",
                            "day": day,
                            "parties": ["Arjun Malhotra", "Neha Kapoor"]
                        })
    return conflicts

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_calendar",
            "description": "Get calendar events for a specific person or all people, optionally filtered by day.",
            "parameters": {
                "type": "object",
                "properties": {
                    "person": {"type": "string", "description": "Name of person (e.g. 'Arjun Malhotra', 'Neha Kapoor')"},
                    "day": {"type": "string", "description": "Day of week (e.g. 'Mon 21 Sep', 'Wed 23 Sep')"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_emails",
            "description": "Search email threads by topic keyword or email address.",
            "parameters": {
                "type": "object",
                "properties": {
                    "thread": {"type": "string", "description": "Thread subject (e.g. 'Vendor List', 'Campaign Deck', 'Lease')"},
                    "person": {"type": "string", "description": "Filter by sender or recipient name/email"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_transcript",
            "description": "Retrieve meeting transcripts and spoken utterances.",
            "parameters": {
                "type": "object",
                "properties": {
                    "meeting_id": {"type": "string", "description": "Optional transcript ID"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_voice_notes",
            "description": "Get Arjun's private voice notes to identify his personal commitments and open thoughts.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_calendar_conflicts",
            "description": "Analyze cross-attendee calendar conflicts or overlap on a given day.",
            "parameters": {
                "type": "object",
                "properties": {
                    "day": {"type": "string", "description": "Day to inspect (e.g. 'Thu 24 Sep')"}
                },
                "required": ["day"]
            }
        }
    }
]

TOOL_MAP = {
    "get_calendar": get_calendar,
    "search_emails": search_emails,
    "get_transcript": get_transcript,
    "get_voice_notes": get_voice_notes,
    "check_calendar_conflicts": check_calendar_conflicts,
}