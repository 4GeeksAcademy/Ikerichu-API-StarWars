from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    fav_planet: Mapped["Fav_planet"] = relationship(back_populates="user")
    fav_char: Mapped["Fav_char"] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
        }
    
class Fav_planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))
    user: Mapped["User"] = relationship(back_populates="fav_planet")
    planet: Mapped["Planets"] = relationship(back_populates="fav_planet")



    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
        }

class Fav_char(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    char_id: Mapped[int] = mapped_column(ForeignKey("characters.id"))
    user: Mapped["User"] = relationship(back_populates="fav_char")
    characters: Mapped["Characters"] = relationship(back_populates="fav_char")



    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "char_id": self.char_id,
        }
    
class Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    population: Mapped[int] = mapped_column(nullable=False)
    character: Mapped[list["Characters"]]=relationship(back_populates="planet")
    characters: Mapped[list[int]]=mapped_column(ForeignKey("characters.id"))

    
    


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "characters": self.characters
        }

class Characters(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120),nullable=False)
    gender: Mapped[str] = mapped_column(String(120), nullable=False)
    specie: Mapped["str"]=mapped_column(String(120), nullable=False)
    planet_id: Mapped[int]=mapped_column(ForeignKey("planets.id"))
    planet: Mapped["Planets"]=relationship(back_populates="characters")

    def get_all_characters():
        return Characters

    def get_a_people(id):
        char=None
        for m in Characters.id:
            if id == m["id"]:
                char=m
        return char


    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "gender": self.gender,
            "specie":self.specie,
            "planet":self.planet_id
        }