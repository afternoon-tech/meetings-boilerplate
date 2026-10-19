import datetime
import uuid

from sqlalchemy import DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.calendar_providers.domain import CalendarProvider
from src.database import Base


class AdvisorEntity(Base):
    """A user of the platform: a financial advisor at the firm."""

    __tablename__ = "advisor"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(320), unique=True)


class ClientEntity(Base):
    __tablename__ = "client"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(320), unique=True)


class CalendarConnectionEntity(Base):
    """An advisor's connected Google or Microsoft calendar. OAuth tokens would live here in production."""

    __tablename__ = "calendar_connection"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    advisor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("advisor.id"))
    provider: Mapped[CalendarProvider] = mapped_column(Enum(CalendarProvider, name="calendar_provider"))
    account_email: Mapped[str] = mapped_column(String(320))
    connected_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_synced_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True))

    advisor: Mapped[AdvisorEntity] = relationship(lazy="joined")


class MeetingEntity(Base):
    __tablename__ = "meeting"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(500))
    starts_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    ends_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
