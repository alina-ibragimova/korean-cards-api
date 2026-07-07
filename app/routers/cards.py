from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
from sqlalchemy import func

from app.database import get_db
from app import models, schemas
from app.spaced_repetition import calculate_sm2
from app.auth import get_current_user

router = APIRouter(prefix="/cards", tags = ["cards"])

@router.post("/", response_model=schemas.CardResponse, status_code = 201)
def create_card(card: schemas.CardCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_card = models.Card(**card.model_dump(), user_id=current_user.id)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

@router.get("/", response_model=List[schemas.CardResponse])
def get_cards(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
    ):
    return db.query(models.Card).filter(
        models.Card.user_id == current_user.id).order_by(
            models.Card.id.desc()).offset(skip).limit(limit).all()


@router.get("/due", response_model = List[schemas.CardResponse])
def get_due_cards(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    now = datetime.now(timezone.utc)
    return db.query(models.Card).filter(
        models.Card.user_id == current_user.id, 
        models.Card.next_review <= now).all()
    

@router.get("/stats", response_model = schemas.StatsResponse)
def get_stats(db: Session = Depends(get_db),
              current_user: models.User = Depends(get_current_user)):
    now = datetime.now(timezone.utc)
    query = db.query(models.Card).filter(models.Card.user_id == current_user.id)

    total_cards = query.count()
    due_today = query.filter(models.Card.next_review <= now).count()
    learned = query.filter(models.Card.interval > 21).count()
    new_cards = query.filter(models.Card.repetitions == 0).count()
    avg_ease = query.with_entities(func.avg(models.Card.ease_factor)).scalar()

    return schemas.StatsResponse(
        total_cards=total_cards,
        due_today=due_today,
        learned=learned,
        new_cards=new_cards,
        average_ease_factor=round(avg_ease, 2) if avg_ease else 0.0,
    )

@router.get("/{card_id}", response_model=schemas.CardResponse)
def get_card(card_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    card = db.query(models.Card).filter(
        models.Card.id == card_id,
        models.Card.user_id == current_user.id
        ).first()
    if card is None:
        raise HTTPException(status_code=404,detail="Карточка не найдена")
    return card

@router.patch("/{card_id}", response_model = schemas.CardResponse)
def update_card(
    card_id: int, 
    card_data: schemas.CardUpdate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
    ):
    card = db.query(models.Card).filter(
        models.Card.id == card_id,
        models.Card.user_id == current_user.id
        ).first()
    if card is None:
        raise HTTPException(status_code=404, detail="Карточка не найдена")
    update_data = card_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(card, field, value)
    db.commit()
    db.refresh(card)
    return card
    
@router.delete("/{card_id}", status_code=204)
def delete_card(
    card_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
    ):
    card = db.query(models.Card).filter(
        models.Card.id == card_id, 
        models.Card.user_id == current_user.id).first()
    if card is None:
        raise HTTPException(status_code = 404, detail="Карточка не найдена")
    
    db.delete(card)
    db.commit()


@router.post("/{card_id}/review", response_model=schemas.CardResponse)
def review_card(
    card_id: int, 
    review: schemas.ReviewCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
    ):
    card = db.query(models.Card).filter(
        models.Card.id == card_id,
        models.Card.user_id == current_user.id
        ).first()
    if card is None:
        raise HTTPException(status_code=404, detail = "Карточка не найдена")
    result = calculate_sm2(
        repetitions=card.repetitions,
        ease_factor=card.ease_factor,
        interval=card.interval,
        quality=review.quality,
    )
    card.repetitions = result.repetitions
    card.ease_factor = result.ease_factor
    card.interval = result.interval
    card.next_review = result.next_review
    db.commit()
    db.refresh(card)
    return card
