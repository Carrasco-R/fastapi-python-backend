from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class Album(Base):
  __tablename__ = "albums"

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String, index=True)
  description = Column(String, index=True)

  photos = relationship("Photo", back_populates="album")


class Photo(Base):
  __tablename__ = "photos"
  
  id = Column(Integer, primary_key=True, index=True)
  title = Column(String, index=True)
  description = Column(String, index=True)
  filename = Column(String, index=True)
  album_id = Column(Integer, ForeignKey("albums.id"))
  timestamp = Column(String, index=True) 
  location = Column(String, index=True)

  album = relationship("Album", back_populates="photos")