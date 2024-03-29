from sqlalchemy.orm import Session
from typing import List

from . import models, schemas

def get_album(db: Session, album_id: int):
  return db.query(models.Album).filter(models.Album.id == album_id).first()

def create_album(db: Session, album: schemas.AlbumCreate):
  db_album = models.Album(title=album.title, description=album.description)
  db.add(db_album)
  db.commit()
  db.refresh(db_album)
  return db_album

def get_albums(db: Session):
  return db.query(models.Album).all()

def update_album(db: Session, album_id:int, album: schemas.Album):
  db_album = get_album(db, album_id)
  db_album.title = album.title
  db_album.description = album.description
  db_album.photos = album.photos
  db.commit()
  db.refresh(db_album)
  return db_album

def delete_album(db: Session, album_id: int):
  db_album = get_album(db, album_id)
  db.delete(db_album)
  db.commit()
  return True

def get_photo(db: Session, photo_id: int):
 return db.query(models.Photo).filter(models.Photo.id == photo_id).first()

def create_photo(db: Session, photo: schemas.PhotoCreate):
  db_photo = models.Photo(
    album_id = photo.album_id,
    title = photo.title,
    description = photo.title,
    filename = photo.filename,
    timestamp = photo.timestamp,
    location = photo.location
  )
  db.add(db_photo)
  db.commit()
  db.refresh(db_photo)
  return db_photo