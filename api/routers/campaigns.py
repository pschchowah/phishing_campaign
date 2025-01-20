from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from .. import models, database
from pydantic import BaseModel


router = APIRouter(prefix="/campaigns", tags=["campaigns"])


class CampaignCreate(BaseModel):
    name: str
    description: str = ""


class CampaignResponse(BaseModel):
    id: int
    name: str
    description: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


@router.post("/", response_model=CampaignResponse)
def create_campaign(campaign: CampaignCreate, db: Session = Depends(database.get_db)):
    try:
        db_campaign = models.Campaign(
            name=campaign.name,
            description=campaign.description,
            status=models.CampaignStatus.RUNNING,
        )
        db.add(db_campaign)
        db.commit()
        db.refresh(db_campaign)
        return db_campaign
    except Exception as e:
        print(f"Error creating campaign: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[CampaignResponse])
def get_campaigns(db: Session = Depends(database.get_db)):
    return db.query(models.Campaign).all()


@router.get("/{campaign_id}", response_model=CampaignResponse)
def get_campaign(campaign_id: int, db: Session = Depends(database.get_db)):
    try:
        campaign = (
            db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
        )
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        return campaign
    except Exception as e:
        print(f"Error fetching campaign: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{campaign_id}/status")
def update_campaign_status(
    campaign_id: int,
    status: models.CampaignStatus,
    db: Session = Depends(database.get_db),
):
    try:
        campaign = (
            db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
        )
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")

        campaign.status = status
        db.commit()
        db.refresh(campaign)
        return campaign
    except Exception as e:
        print(f"Error updating campaign status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
