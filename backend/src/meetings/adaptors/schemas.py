import datetime
import uuid

from src.calendar_providers.domain import CalendarProvider
from src.camel_model import CamelModel


class AdvisorResponse(CamelModel):
    id: uuid.UUID
    name: str
    email: str


class CalendarConnectionResponse(CamelModel):
    id: uuid.UUID
    provider: CalendarProvider
    account_email: str
    advisor: AdvisorResponse
    last_synced_at: datetime.datetime | None


class ClientResponse(CamelModel):
    id: uuid.UUID
    name: str
    email: str


class MeetingResponse(CamelModel):
    id: uuid.UUID
    title: str
    starts_at: datetime.datetime
    ends_at: datetime.datetime
