from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.calendar_providers.stub_client import StubCalendarClient, get_calendar_client
from src.database import get_session
from src.meetings.adaptors.schemas import CalendarConnectionResponse, ClientResponse, MeetingResponse
from src.meetings.application.MeetingSyncService import MeetingSyncService
from src.meetings.infrastructure.repositories import (
    CalendarConnectionRepository,
    ClientRepository,
    MeetingRepository,
)

router = APIRouter(prefix="/api")

Session = Annotated[AsyncSession, Depends(get_session)]
CalendarClient = Annotated[StubCalendarClient, Depends(get_calendar_client)]


@router.get("/meetings")
async def list_meetings(session: Session) -> list[MeetingResponse]:
    meetings = await MeetingRepository(session).list_all()
    return [MeetingResponse.model_validate(meeting) for meeting in meetings]


@router.post("/meetings/sync", status_code=status.HTTP_204_NO_CONTENT)
async def sync_meetings(session: Session, calendar_client: CalendarClient) -> None:
    try:
        await MeetingSyncService(session, calendar_client).sync_all()
    except NotImplementedError:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Meeting sync is not implemented yet"
        ) from None


@router.get("/calendar-connections")
async def list_calendar_connections(session: Session) -> list[CalendarConnectionResponse]:
    connections = await CalendarConnectionRepository(session).list_all()
    return [CalendarConnectionResponse.model_validate(connection) for connection in connections]


@router.get("/clients")
async def list_clients(session: Session) -> list[ClientResponse]:
    clients = await ClientRepository(session).list_all()
    return [ClientResponse.model_validate(client) for client in clients]
