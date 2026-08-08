from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import models
import schemas
import crud
from database import engine, get_db
from auth import verify_password, create_access_token, get_current_user

# Database tables actually create ho rahi hain yahan (agar exist nahi karti)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Patient Management system API"}

# ---------- REGISTER ----------
@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    return crud.create_user(db, user)


# ---------- LOGIN ----------
@app.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# ---------- CREATE ITEM (protected) ----------
@app.post("/items/", response_model=schemas.ItemOut)
def create_item(
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.create_item(db, item, current_user.id)


# ---------- READ ITEMS (protected) ----------
@app.get("/items/", response_model=list[schemas.ItemOut])
def read_items(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_items(db, current_user.id)


# ---------- UPDATE ITEM (protected) ----------
@app.put("/items/{item_id}", response_model=schemas.ItemOut)
def update_item(
    item_id: int,
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    updated_item = crud.update_item(db, item_id, item, current_user.id)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item


# ---------- DELETE ITEM (protected) ----------
@app.delete("/items/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    deleted_item = crud.delete_item(db, item_id, current_user.id)
    if not deleted_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}