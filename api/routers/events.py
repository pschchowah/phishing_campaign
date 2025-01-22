from fastapi import APIRouter, Depends, Request, HTTPException, Response
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, database
from pydantic import BaseModel
from datetime import datetime
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix="/events", tags=["events"])
templates = Jinja2Templates(directory="api/templates")


class EventResponse(BaseModel):
    id: int
    email: str
    ip: str
    event_type: str
    campaign_id: int
    employee_id: int
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

    # Get employee_id from email
    employee = db.query(models.Employee).filter(models.Employee.email == email).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    event = models.Event(
        email=email,
        campaign_id=campaign_id,
        employee_id=employee.id,
        event_type=models.EventType.OPEN,
        ip=request.client.host,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return {"status": "success"}


@router.get("/track_click", response_class=HTMLResponse)
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

    # Get employee_id from email
    employee = db.query(models.Employee).filter(models.Employee.email == email).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    event = models.Event(
        email=email,
        campaign_id=campaign_id,
        employee_id=employee.id, #add employee
        event_type=models.EventType.CLICK,
        ip=request.client.host,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    # return fake submission html form to log a submitted event
    return templates.TemplateResponse(
        "submission.html", {"request": request, "campaign_id": campaign_id,"email": email}
    )


@router.post("/track_submitted")
async def track_submitted(request: Request, db: Session = Depends(database.get_db)):
    form = await request.form()
    email = form.get("email")
    campaign_id = form.get("campaign_id")
    employee_id = form.get("employee_id")
    print(email)
    
    # Get employee_id from email
    employee = db.query(models.Employee).filter(models.Employee.email == email).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    
    # Create SUBMITTED event
    event = models.Event(
        email=email,
        campaign_id=campaign_id,
        employee_id=employee_id,
        event_type=models.EventType.SUBMITTED,
        ip=request.client.host,
    )
    db.add(event)
    db.commit()
    db.refresh(event)

    return {"status": "success"}


@router.get("/track_reported")
def track_reported(
    request: Request,
    email: str,
    campaign_id: int,
    employee_id: int,
    db: Session = Depends(database.get_db),
):
    event = models.Event(
        email=email,
        campaign_id=campaign_id,
        employee_id=employee_id,
        event_type=models.EventType.REPORTED,
        ip=request.client.host,
    )
    db.add(event)
    db.commit()
    db.refresh(event)

    return {"status": "success"}


@router.get("/", response_model=List[EventResponse])
def get_events(
    campaign_id: Optional[int] = None,
    employee_id: Optional[int] = None,
    db: Session = Depends(database.get_db)
):
    query = db.query(models.Event, models.Campaign.name.label("campaign_name")).join(
        models.Campaign
    )

    if campaign_id:
        query = query.filter(models.Event.campaign_id == campaign_id)
    if employee_id:
        query = query.filter(models.Event.employee_id == employee_id)

    events = query.all()

    # Convert SQLAlchemy objects to Pydantic model format
    return [
        EventResponse(
            id=event.Event.id,
            email=event.Event.email,
            ip=event.Event.ip,
            event_type=event.Event.event_type.value,
            campaign_id=event.Event.campaign_id,
            employee_id=event.Event.employee_id,
            campaign_name=event.campaign_name,
            timestamp=event.Event.timestamp,
        )
        for event in events
    ]
