from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, database
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/events", tags=["events"])


class EventResponse(BaseModel):
    id: int
    email: str
    ip: str
    event_type: str
    campaign_id: int
    campaign_name: str
    timestamp: datetime

    class Config:
        from_attributes = True


@router.get("/track_open")
def track_open(
    request: Request,
    email: str,
    campaign_id: int,
    db: Session = Depends(database.get_db),
):
    # Verify campaign exists
    campaign = (
        db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    )
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    event = models.Event(
        email=email,
        campaign_id=campaign_id,
        event_type=models.EventType.OPEN,
        ip=request.client.host,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return {"status": "success"}


@router.get("/track_click")
def track_click(
    request: Request,
    email: str,
    campaign_id: int,
    db: Session = Depends(database.get_db),
):
    # Verify campaign exists
    campaign = (
        db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    )
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    event = models.Event(
        email=email,
        campaign_id=campaign_id,
        event_type=models.EventType.CLICK,
        ip=request.client.host,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return {"status": "success"}


@router.get("/", response_model=List[EventResponse])
def get_events(
    campaign_id: Optional[int] = None, db: Session = Depends(database.get_db)
):
    query = db.query(models.Event, models.Campaign.name.label("campaign_name")).join(
        models.Campaign
    )

    if campaign_id:
        query = query.filter(models.Event.campaign_id == campaign_id)

    events = query.all()

    # Convert SQLAlchemy objects to Pydantic model format
    return [
        EventResponse(
            id=event.Event.id,
            email=event.Event.email,
            ip=event.Event.ip,
            event_type=event.Event.event_type.value,
            campaign_id=event.Event.campaign_id,
            campaign_name=event.campaign_name,
            timestamp=event.Event.timestamp,
        )
        for event in events
    ]
