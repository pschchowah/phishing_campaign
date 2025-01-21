from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base


class EventType(enum.Enum):
    OPEN = "open"
    CLICK = "click"
    SUBMITTED = "submitted"
    REPORTED = "reported"
    DOWNLOADED_ATTACHMENT = "downloaded_attachement"


class CampaignStatus(enum.Enum):
    RUNNING = "running"
    FINISHED = "finished"


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(CampaignStatus), default=CampaignStatus.RUNNING)
    created_at = Column(DateTime, server_default=func.now())

    # Relationship with events
    events = relationship("Event", back_populates="campaign")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    email = Column(String, index=True)
    ip = Column(String)
    event_type = Column(Enum(EventType))
    timestamp = Column(DateTime, default=func.now())

    # Relationship with Campaign
    campaign = relationship("Campaign", back_populates="events")
