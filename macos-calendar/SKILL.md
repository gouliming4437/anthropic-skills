---
name: macos-calendar
description: Manipulate macOS Calendar.app events and Reminders.app using Python and the EventKit framework. Use this skill when the user wants to create, read, update, or delete calendar events or reminders, list calendars/reminder lists, query upcoming events or tasks, or automate calendar and reminder-related tasks on macOS.
---

# macOS Calendar & Reminders Skill

Manipulate macOS Calendar.app and Reminders.app using the native EventKit framework via Python.

## Requirements

This skill runs in the user's miniconda `pytest` environment. Install the dependency:

```bash
conda activate pytest
pip install pyobjc-framework-EventKit
```

**First-run permission**: macOS will prompt for Calendar and Reminders access the first time. The user must grant these permissions.

## Usage

Always use the wrapper script `scripts/calendar.sh` which handles conda environment activation:

### Event Commands

```bash
# List calendars
bash scripts/calendar.sh list-calendars

# List events for next 7 days
bash scripts/calendar.sh list-events

# List events for specific range
bash scripts/calendar.sh list-events --start 2025-01-01 --end 2025-01-31

# Create event
bash scripts/calendar.sh create-event "Meeting" --start "2025-01-15T10:00:00" --duration 60

# Create event with details
bash scripts/calendar.sh create-event "Team Sync" \
    --start "2025-01-15T14:00:00" \
    --end "2025-01-15T15:00:00" \
    --calendar "Work" \
    --location "Zoom" \
    --notes "Weekly sync"

# Delete event
bash scripts/calendar.sh delete-event <event_id>
```

### Reminder Commands

```bash
# List reminder lists
bash scripts/calendar.sh list-reminder-lists

# List incomplete reminders
bash scripts/calendar.sh list-reminders

# List reminders from specific list
bash scripts/calendar.sh list-reminders --list "Shopping"

# List all reminders including completed
bash scripts/calendar.sh list-reminders --include-completed

# Create reminder
bash scripts/calendar.sh create-reminder "Buy groceries"

# Create reminder with due date and priority
bash scripts/calendar.sh create-reminder "Submit report" \
    --due "2025-01-15T17:00:00" \
    --list "Work" \
    --priority 1 \
    --notes "Q4 quarterly report"

# Mark reminder as completed
bash scripts/calendar.sh complete-reminder <reminder_id>

# Mark reminder as incomplete
bash scripts/calendar.sh complete-reminder <reminder_id> --undo

# Delete reminder
bash scripts/calendar.sh delete-reminder <reminder_id>
```

## Python API

For more complex operations, use the `CalendarManager` class directly (ensure pytest env is active):

```python
from calendar_utils import CalendarManager
from datetime import datetime, timedelta

mgr = CalendarManager()

# ===== EVENTS =====
mgr.request_event_access()  # Required before event operations

# List all calendars
calendars = mgr.list_calendars()

# Create an event
event = mgr.create_event(
    title="Team Meeting",
    start=datetime(2025, 1, 15, 10, 0),
    end=datetime(2025, 1, 15, 11, 0),
    calendar_name="Work",
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

# ===== REMINDERS =====
mgr.request_reminder_access()  # Required before reminder operations

# List all reminder lists
lists = mgr.list_reminder_lists()

# Create a reminder
reminder = mgr.create_reminder(
    title="Buy milk",
    due_date=datetime(2025, 1, 15, 18, 0),
    list_name="Shopping",
    notes="Whole milk",
    priority=5,  # 0=none, 1=high, 5=medium, 9=low
)

# Get incomplete reminders
reminders = mgr.get_reminders()

# Get all reminders including completed
all_reminders = mgr.get_reminders(include_completed=True)

# Mark as completed
mgr.complete_reminder(reminder["reminder_id"])

# Update a reminder
mgr.update_reminder(reminder["reminder_id"], title="Buy oat milk", priority=1)

# Delete a reminder
mgr.delete_reminder(reminder["reminder_id"])
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
