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

    def get_all_users():
        return db.session.scalars(db.select(User)).all()

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

    def get_all_fav_planets():
        return db.session.scalars(db.select(Fav_planet)).all()
    
    def add_fav_planet(user_id, planet_id):
        new_fav_planet = Fav_planet(user_id=user_id, planet_id=planet_id)
        db.session.add(new_fav_planet)
        db.session.commit()

    def delete_planet(id):
        fav_planet = db.session.get(Fav_planet, id)
        if fav_planet is None:
            return False
        db.session.delete(fav_planet)
        db.session.commit()
        return True

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

    def get_all_fav_characters():
        return db.session.scalars(db.select(Fav_char)).all()
    
    def add_fav_char(user_id, char_id):
        new_fav_char = Fav_char(user_id=user_id, char_id=char_id)
        db.session.add(new_fav_char)
        db.session.commit()

    def delete_character(id):
        fav_char = db.session.get(Fav_char, id)
        if fav_char is None:
            return False
        db.session.delete(fav_char)
        db.session.commit()
        return True

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
    

    def get_all_planets():
        return db.session.scalars(db.select(Planets)).all()

    def get_a_planet(id):
        return db.session.get(Planets, id)
    


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
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
        return db.session.scalars(db.select(Characters)).all()

    def get_a_people(id):
        return db.session.get(Characters, id)


    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "gender": self.gender,
            "specie":self.specie,
            "planet":self.planet_id
        }
