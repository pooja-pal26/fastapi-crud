from sqlalchemy.orm import Session
import models
import schemas
from auth import hash_password

def save_message(db: Session, sender_username: str, message: str):
    db_message = models.ChatMessage(sender_username=sender_username, message=message)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_recent_messages(db: Session, limit: int = 50):
    return db.query(models.ChatMessage).order_by(models.ChatMessage.timestamp.desc()).limit(limit).all()[::-1]

# ---------- USER CRUD ----------

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


# ---------- ITEM CRUD ----------

def create_item(db: Session, item: schemas.ItemCreate, owner_id: int):
    db_item = models.Item(**item.dict(), owner_id=owner_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db: Session, owner_id: int):
    return db.query(models.Item).filter(models.Item.owner_id == owner_id).all()

def get_item(db: Session, item_id: int, owner_id: int):
    return db.query(models.Item).filter(
        models.Item.id == item_id, models.Item.owner_id == owner_id
    ).first()

def update_item(db: Session, item_id: int, item: schemas.ItemCreate, owner_id: int):
    db_item = get_item(db, item_id, owner_id)
    if db_item:
        db_item.title = item.title
        db_item.description = item.description
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int, owner_id: int):
    db_item = get_item(db, item_id, owner_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item