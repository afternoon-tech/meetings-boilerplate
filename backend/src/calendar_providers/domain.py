import datetime
import enum

from pydantic import BaseModel


class CalendarProvider(str, enum.Enum):
    GOOGLE = "GOOGLE"
    MICROSOFT = "MICROSOFT"


class EventStatus(str, enum.Enum):
    CONFIRMED = "CONFIRMED"
    TENTATIVE = "TENTATIVE"
    CANCELLED = "CANCELLED"


class RsvpStatus(str, enum.Enum):
    NEEDS_ACTION = "NEEDS_ACTION"
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"
    TENTATIVE = "TENTATIVE"


class ExternalAttendee(BaseModel):
    email: str
    name: str | None = None
    rsvp: RsvpStatus = RsvpStatus.NEEDS_ACTION


class ExternalCalendarEvent(BaseModel):
    """An event as one connected calendar reports it, already normalised from the provider's API shape.

    `external_id` is only unique within the calendar it came from: the same meeting has a different
    `external_id` in every attendee's calendar. `ical_uid` is set by the organiser's calendar and copied
    into every invitee's calendar, so it is shared across calendars. For a recurring series every
    occurrence carries the series' `ical_uid`; `original_starts_at` says which occurrence this is.
    """

    external_id: str
    ical_uid: str | None
    recurring_event_id: str | None = None
    original_starts_at: datetime.datetime | None = None
    title: str
    description: str | None = None
    starts_at: datetime.datetime
    ends_at: datetime.datetime
    status: EventStatus = EventStatus.CONFIRMED
    organiser_email: str
    attendees: list[ExternalAttendee] = []
    updated_at: datetime.datetime


class CalendarProviderError(Exception):
    """The provider could not be reached or rejected the request (timeout, 5xx, revoked token...)."""
