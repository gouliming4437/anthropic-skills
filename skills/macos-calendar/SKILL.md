---
name: macos-calendar
description: Manipulate macOS Calendar.app events and reminders using Python and the EventKit framework. Use this skill when the user wants to create, read, update, or delete calendar events, list calendars, query upcoming events, or automate calendar-related tasks on macOS.
---

# macOS Calendar Skill

Manipulate macOS Calendar.app using the native EventKit framework via Python.

## Requirements

This skill runs in the user's miniconda `pytest` environment. Install the dependency:

```bash
conda activate pytest
pip install pyobjc-framework-EventKit
```

**First-run permission**: macOS will prompt for Calendar access the first time the script runs. The user must grant this permission.

## Usage

Always use the wrapper script `scripts/calendar.sh` which handles conda environment activation:

```bash
# List calendars
bash scripts/calendar.sh list-calendars

# List events for next 7 days
bash scripts/calendar.sh list-events

# List events for specific range
bash scripts/calendar.sh list-events --start 2025-01-01 --end 2025-01-31

# Create event
bash scripts/calendar.sh create "Meeting" --start "2025-01-15T10:00:00" --duration 60

# Create event with details
bash scripts/calendar.sh create "Team Sync" \
    --start "2025-01-15T14:00:00" \
    --end "2025-01-15T15:00:00" \
    --calendar "Work" \
    --location "Zoom" \
    --notes "Weekly sync"

# Delete event
bash scripts/calendar.sh delete <event_id>
```

## Python API

For more complex operations, use the `CalendarManager` class directly (ensure pytest env is active):

```python
from calendar_utils import CalendarManager
from datetime import datetime, timedelta

mgr = CalendarManager()
mgr.request_event_access()  # Required before any operations

# List all calendars
calendars = mgr.list_calendars()

# Create an event
event = mgr.create_event(
    title="Team Meeting",
    start=datetime(2025, 1, 15, 10, 0),
    end=datetime(2025, 1, 15, 11, 0),
    calendar_name="Work",  # Optional, uses default if omitted
    location="Conference Room A",
    notes="Discuss Q1 planning",
)

# Get events for the next 7 days
now = datetime.now()
events = mgr.get_events(now, now + timedelta(days=7))

# Update an event
mgr.update_event(event["event_id"], title="Updated Meeting Title")

# Delete an event
mgr.delete_event(event["event_id"])
```

## API Reference

### CalendarManager Methods

| Method | Description |
|--------|-------------|
| `request_event_access()` | Request calendar access. Call before any operations. Returns `bool`. |
| `list_calendars(entity_type="event")` | List all calendars. Returns list of dicts with `title`, `calendar_id`, `allows_modifications`. |
| `create_event(title, start, end, ...)` | Create event. Returns dict with `event_id`. |
| `get_events(start, end, calendar_names=None)` | Query events in date range. Returns list of event dicts. |
| `update_event(event_id, ...)` | Update event fields. Returns updated event dict. |
| `delete_event(event_id, future_events=False)` | Delete event. Set `future_events=True` for recurring events. |

### Event Dict Structure

```python
{
    "event_id": str,       # Unique identifier
    "title": str,
    "start": str,          # ISO format datetime
    "end": str,            # ISO format datetime
    "location": str | None,
    "notes": str | None,
    "all_day": bool,
    "calendar": str,       # Calendar name
    "url": str | None,
}
```

## Common Patterns

### Find events by title

```python
events = mgr.get_events(start, end)
matching = [e for e in events if "standup" in e["title"].lower()]
```

### Create recurring-like events

EventKit supports recurrence rules, but for simple cases, create multiple events:

```python
from datetime import datetime, timedelta

base = datetime(2025, 1, 6, 9, 0)  # First Monday
for week in range(4):
    mgr.create_event(
        title="Weekly Standup",
        start=base + timedelta(weeks=week),
        end=base + timedelta(weeks=week, minutes=30),
    )
```

### Move an event to a different time

```python
mgr.update_event(
    event_id,
    start=new_start,
    end=new_end,
)
```

## Troubleshooting

**"Calendar access not granted"**: Go to System Settings → Privacy & Security → Calendars and enable access for Terminal or your Python environment.

**Calendar not found**: Use `list_calendars()` to see exact calendar names. Names are case-sensitive.

**Event not appearing**: Check you're looking at the correct calendar in Calendar.app. Events created without specifying `calendar_name` go to the default calendar.
