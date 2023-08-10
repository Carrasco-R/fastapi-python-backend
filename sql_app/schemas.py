from typing import List, Union
from pydantic import BaseModel

class PhotoBase(BaseModel):
  album_id: str
  title: str
  description: Union[str, None] = None
  filename: str 
  timestamp: str
  location: str

class PhotoCreate(PhotoBase):
  pass

class Photo(PhotoBase):
  id: int

  class Config:
    orm_mode = True


class AlbumBase(BaseModel):
  title: str = ""
  description: Union[str, None] = None

class AlbumCreate(AlbumBase):
  pass

class Album(AlbumBase):
  id: int 
  photos: List[Photo] = []

  class Config:
    orm_mode = True

