#!/usr/bin/env python3
"""
macOS Calendar manipulation utilities using EventKit framework.
Requires: pip install pyobjc-framework-EventKit (in the pytest conda env)
"""

import sys
import json
from datetime import datetime, timedelta
from typing import Optional

try:
    from EventKit import (
        EKEventStore,
        EKEvent,
        EKReminder,
        EKEntityTypeEvent,
        EKEntityTypeReminder,
        EKSpanThisEvent,
        EKSpanFutureEvents,
        EKAuthorizationStatusAuthorized,
        EKAuthorizationStatusNotDetermined,
    )
    from Foundation import NSDate, NSDateComponents, NSCalendar
except ImportError:
    print("Error: pyobjc-framework-EventKit not installed.", file=sys.stderr)
    print("Install with: pip install pyobjc-framework-EventKit", file=sys.stderr)
    sys.exit(1)


def _nsdate_from_datetime(dt: datetime) -> NSDate:
    """Convert Python datetime to NSDate."""
    return NSDate.dateWithTimeIntervalSince1970_(dt.timestamp())


def _datetime_from_nsdate(nsdate: NSDate) -> datetime:
    """Convert NSDate to Python datetime."""
    return datetime.fromtimestamp(nsdate.timeIntervalSince1970())


class CalendarManager:
    """Manager for macOS Calendar operations via EventKit."""

    def __init__(self):
        self.store = EKEventStore.alloc().init()
        self._authorized_events = False
        self._authorized_reminders = False

    def request_event_access(self) -> bool:
        """Request access to calendar events. Returns True if granted."""
        status = EKEventStore.authorizationStatusForEntityType_(EKEntityTypeEvent)
        
        if status == EKAuthorizationStatusAuthorized:
            self._authorized_events = True
            return True
        
        if status == EKAuthorizationStatusNotDetermined:
            # Request access synchronously using a semaphore pattern
            import threading
            granted = [False]
            event = threading.Event()
            
            def callback(success, error):
                granted[0] = success
                event.set()
            
            self.store.requestAccessToEntityType_completion_(EKEntityTypeEvent, callback)
            event.wait(timeout=30)
            self._authorized_events = granted[0]
            return granted[0]
        
        return False

    def request_reminder_access(self) -> bool:
        """Request access to reminders. Returns True if granted."""
        status = EKEventStore.authorizationStatusForEntityType_(EKEntityTypeReminder)
        
        if status == EKAuthorizationStatusAuthorized:
            self._authorized_reminders = True
            return True
        
        if status == EKAuthorizationStatusNotDetermined:
            import threading
            granted = [False]
            event = threading.Event()
            
            def callback(success, error):
                granted[0] = success
                event.set()
            
            self.store.requestAccessToEntityType_completion_(EKEntityTypeReminder, callback)
            event.wait(timeout=30)
            self._authorized_reminders = granted[0]
            return granted[0]
        
        return False

    def list_calendars(self, entity_type: str = "event") -> list[dict]:
        """List all available calendars.
        
        Args:
            entity_type: "event" or "reminder"
        """
        ek_type = EKEntityTypeEvent if entity_type == "event" else EKEntityTypeReminder
        calendars = self.store.calendarsForEntityType_(ek_type)
        
        return [
            {
                "title": cal.title(),
                "calendar_id": cal.calendarIdentifier(),
                "type": cal.type(),
                "allows_modifications": cal.allowsContentModifications(),
                "color": str(cal.color()) if cal.color() else None,
            }
            for cal in calendars
        ]

    def get_calendar_by_name(self, name: str, entity_type: str = "event"):
        """Get a calendar by its name."""
        ek_type = EKEntityTypeEvent if entity_type == "event" else EKEntityTypeReminder
        calendars = self.store.calendarsForEntityType_(ek_type)
        
        for cal in calendars:
            if cal.title() == name:
                return cal
        return None

    def create_event(
        self,
        title: str,
        start: datetime,
        end: datetime,
        calendar_name: Optional[str] = None,
        location: Optional[str] = None,
        notes: Optional[str] = None,
        all_day: bool = False,
        url: Optional[str] = None,
    ) -> dict:
        """Create a new calendar event.
        
        Args:
            title: Event title
            start: Start datetime
            end: End datetime
            calendar_name: Name of calendar (uses default if None)
            location: Event location
            notes: Event notes/description
            all_day: Whether this is an all-day event
            url: URL associated with event
            
        Returns:
            Dict with event details including event_id
        """
        event = EKEvent.eventWithEventStore_(self.store)
        event.setTitle_(title)
        event.setStartDate_(_nsdate_from_datetime(start))
        event.setEndDate_(_nsdate_from_datetime(end))
        event.setAllDay_(all_day)
        
        if location:
            event.setLocation_(location)
        if notes:
            event.setNotes_(notes)
        if url:
            from Foundation import NSURL
            event.setURL_(NSURL.URLWithString_(url))
        
        # Set calendar
        if calendar_name:
            calendar = self.get_calendar_by_name(calendar_name, "event")
            if not calendar:
                raise ValueError(f"Calendar '{calendar_name}' not found")
            event.setCalendar_(calendar)
        else:
            event.setCalendar_(self.store.defaultCalendarForNewEvents())
        
        # Save
        success, error = self.store.saveEvent_span_error_(event, EKSpanThisEvent, None)
        if not success:
            raise RuntimeError(f"Failed to save event: {error}")
        
        return {
            "event_id": event.eventIdentifier(),
            "title": title,
            "start": start.isoformat(),
            "end": end.isoformat(),
            "calendar": event.calendar().title(),
        }

    def get_events(
        self,
        start: datetime,
        end: datetime,
        calendar_names: Optional[list[str]] = None,
    ) -> list[dict]:
        """Get events within a date range.
        
        Args:
            start: Start of range
            end: End of range
            calendar_names: Filter by calendar names (all if None)
        """
        calendars = None
        if calendar_names:
            calendars = [
                self.get_calendar_by_name(name, "event")
                for name in calendar_names
            ]
            calendars = [c for c in calendars if c]
        
        predicate = self.store.predicateForEventsWithStartDate_endDate_calendars_(
            _nsdate_from_datetime(start),
            _nsdate_from_datetime(end),
            calendars,
        )
        
        events = self.store.eventsMatchingPredicate_(predicate)
        
        return [
            {
                "event_id": e.eventIdentifier(),
                "title": e.title(),
                "start": _datetime_from_nsdate(e.startDate()).isoformat(),
                "end": _datetime_from_nsdate(e.endDate()).isoformat(),
                "location": e.location(),
                "notes": e.notes(),
                "all_day": e.isAllDay(),
                "calendar": e.calendar().title(),
                "url": str(e.URL()) if e.URL() else None,
            }
            for e in (events or [])
        ]

    def delete_event(self, event_id: str, future_events: bool = False) -> bool:
        """Delete an event by ID.
        
        Args:
            event_id: The event identifier
            future_events: If True, delete all future occurrences of recurring event
        """
        event = self.store.eventWithIdentifier_(event_id)
        if not event:
            raise ValueError(f"Event '{event_id}' not found")
        
        span = EKSpanFutureEvents if future_events else EKSpanThisEvent
        success, error = self.store.removeEvent_span_error_(event, span, None)
        
        if not success:
            raise RuntimeError(f"Failed to delete event: {error}")
        return True

    def update_event(
        self,
        event_id: str,
        title: Optional[str] = None,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        location: Optional[str] = None,
        notes: Optional[str] = None,
        future_events: bool = False,
    ) -> dict:
        """Update an existing event.
        
        Args:
            event_id: The event identifier
            title: New title (unchanged if None)
            start: New start time (unchanged if None)
            end: New end time (unchanged if None)
            location: New location (unchanged if None)
            notes: New notes (unchanged if None)
            future_events: If True, update all future occurrences
        """
        event = self.store.eventWithIdentifier_(event_id)
        if not event:
            raise ValueError(f"Event '{event_id}' not found")
        
        if title is not None:
            event.setTitle_(title)
        if start is not None:
            event.setStartDate_(_nsdate_from_datetime(start))
        if end is not None:
            event.setEndDate_(_nsdate_from_datetime(end))
        if location is not None:
            event.setLocation_(location)
        if notes is not None:
            event.setNotes_(notes)
        
        span = EKSpanFutureEvents if future_events else EKSpanThisEvent
        success, error = self.store.saveEvent_span_error_(event, span, None)
        
        if not success:
            raise RuntimeError(f"Failed to update event: {error}")
        
        return {
            "event_id": event.eventIdentifier(),
            "title": event.title(),
            "start": _datetime_from_nsdate(event.startDate()).isoformat(),
            "end": _datetime_from_nsdate(event.endDate()).isoformat(),
            "calendar": event.calendar().title(),
        }


# CLI interface for testing
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="macOS Calendar CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # List calendars
    list_cal = subparsers.add_parser("list-calendars", help="List all calendars")
    
    # List events
    list_events = subparsers.add_parser("list-events", help="List events in date range")
    list_events.add_argument("--start", help="Start date (YYYY-MM-DD)", default=None)
    list_events.add_argument("--end", help="End date (YYYY-MM-DD)", default=None)
    list_events.add_argument("--days", type=int, default=7, help="Days from today (default: 7)")
    
    # Create event
    create = subparsers.add_parser("create", help="Create new event")
    create.add_argument("title", help="Event title")
    create.add_argument("--start", required=True, help="Start datetime (ISO format)")
    create.add_argument("--end", help="End datetime (ISO format)")
    create.add_argument("--duration", type=int, default=60, help="Duration in minutes (default: 60)")
    create.add_argument("--calendar", help="Calendar name")
    create.add_argument("--location", help="Event location")
    create.add_argument("--notes", help="Event notes")
    create.add_argument("--all-day", action="store_true", help="All-day event")
    
    # Delete event
    delete = subparsers.add_parser("delete", help="Delete an event")
    delete.add_argument("event_id", help="Event identifier")
    delete.add_argument("--future", action="store_true", help="Delete future occurrences")
    
    args = parser.parse_args()
    
    mgr = CalendarManager()
    
    if not mgr.request_event_access():
        print("Error: Calendar access not granted", file=sys.stderr)
        sys.exit(1)
    
    if args.command == "list-calendars":
        calendars = mgr.list_calendars()
        print(json.dumps(calendars, indent=2))
    
    elif args.command == "list-events":
        if args.start:
            start = datetime.fromisoformat(args.start)
        else:
            start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        if args.end:
            end = datetime.fromisoformat(args.end)
        else:
            end = start + timedelta(days=args.days)
        
        events = mgr.get_events(start, end)
        print(json.dumps(events, indent=2, default=str))
    
    elif args.command == "create":
        start = datetime.fromisoformat(args.start)
        if args.end:
            end = datetime.fromisoformat(args.end)
        else:
            end = start + timedelta(minutes=args.duration)
        
        result = mgr.create_event(
            title=args.title,
            start=start,
            end=end,
            calendar_name=args.calendar,
            location=args.location,
            notes=args.notes,
            all_day=args.all_day,
        )
        print(json.dumps(result, indent=2))
    
    elif args.command == "delete":
        mgr.delete_event(args.event_id, future_events=args.future)
        print(f"Deleted event: {args.event_id}")
