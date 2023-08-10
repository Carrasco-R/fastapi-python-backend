# fastapi
from fastapi import Depends, FastAPI, HTTPException, File, UploadFile, Form 
from fastapi.responses import FileResponse
# db
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from sqlalchemy.orm import Session
# utils
from typing import List
from enum import Enum
import shutil
import os

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
  return crud.get_album(db, album_id)

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
async def upload_photo(
  album_id: int,
  file: UploadFile = File(),
  title: str = Form(),
  description: str = Form(),
  timestamp: str = Form(),
  location: str = Form(),
  db: Session = Depends(get_db)
):
  new_photo = schemas.PhotoCreate(
    album_id = album_id,
    title  =  title,
    description = description,
    filename = file.filename,
    timestamp = timestamp,
    location = location
  )
  db_photo = crud.create_photo(db, new_photo)

  file_location = f"./storage/{album_id}/{db_photo.id}/{file.filename}"
  os.makedirs(os.path.dirname(file_location), exist_ok=True)
  with open(file_location, "wb+") as file_object:
    shutil.copyfileobj(file.file, file_object)
  
  return db_photo

@app.get("/albums/{album_id}/photos/{photo_id}/file")
async def get_photo(album_id: int, photo_id: int, db: Session = Depends(get_db)):
  db_photo = crud.get_photo(db, photo_id)
  print(db_photo.filename)
  some_file_path = f"storage/{album_id}/{photo_id}/{db_photo.filename}"
  return FileResponse(some_file_path)

@app.put("/albums/{album_id}/photos/{photo_id}")
async def update_photo():
  return {"message": "under construction"}