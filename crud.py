from sqlalchemy.orm import Session
import models
import schemas
from auth import hash_password


def get_recent_messages(db: Session, limit: int = 50):
    return db.query(models.ChatMessage).order_by(models.ChatMessage.timestamp.desc()).limit(limit).all()[::-1]

def save_message(db: Session, sender_username: str, message: str = None, file_url: str = None, file_type: str = None):
    db_message = models.ChatMessage(
        sender_username=sender_username,
        message=message,
        file_url=file_url,
        file_type=file_type,
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

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
    db_item = models.Item(**item.model_dump(), owner_id=owner_id)
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


def save_message(db: Session, sender_username: str, receiver_username: str, message: str = None, file_url: str = None, file_type: str = None):
    db_message = models.ChatMessage(
        sender_username=sender_username,
        receiver_username=receiver_username,
        message=message,
        file_url=file_url,
        file_type=file_type,
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_conversation(db: Session, user1: str, user2: str, limit: int = 50):
    messages = db.query(models.ChatMessage).filter(
        ((models.ChatMessage.sender_username == user1) & (models.ChatMessage.receiver_username == user2)) |
        ((models.ChatMessage.sender_username == user2) & (models.ChatMessage.receiver_username == user1))
    ).order_by(models.ChatMessage.timestamp.desc()).limit(limit).all()
    return messages[::-1]


def get_all_users(db: Session, exclude_username: str):
    return db.query(models.User).filter(models.User.username != exclude_username).all()