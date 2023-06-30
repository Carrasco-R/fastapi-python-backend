from typing import List
from enum import Enum

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db = {
  "albums":[1,2,3]
}

@app.get("/albums", response_model=List[schemas.Album])
async def list_albums(db: Session = Depends(get_db)):
  albums = crud.get_albums(db)
  return albums

@app.post("/albums", response_model=schemas.Album, status_code=201)
async def create_album(album: schemas.AlbumCreate, db: Session = Depends(get_db)):
  return crud.create_album(db=db, album=album)

@app.get("/albums/{album_id}", response_model=schemas.Album)
async def get_album(album_id: int, db: Session = Depends(get_db)):
  db_album = crud.get_album(db, album_id)
  return db_album

@app.put("/albums/{album_id}")
async def update_album(album_id: int, album: schemas.Album, db: Session = Depends(get_db)):
  if(album_id != album.id):
    raise HTTPException(status_code=400, detail="album_id in path and body mismatch")
  return crud.update_album(db,album_id,album)

@app.delete("/albums/{album_id}")
async def delete_album(album_id: int, db: Session = Depends(get_db)):
  if crud.delete_album(db, album_id):
     return {"id":album_id}

@app.post("/albums/{album_id}/photos")
async def upload_photo():
  return {"message": "under construction"}

@app.put("/albums/{album_id}/photos/{photo_id}")
async def update_photo():
  return {"message": "under construction"}