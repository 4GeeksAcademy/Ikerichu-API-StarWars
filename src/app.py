"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,Fav_planet,Fav_char,Planets,Characters
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

@app.route('/people',methods=['GET'])
def get_all_people():
    peoples = Characters.get_all_characters()
    response_body = {"Characters": [character.serialize() for character in peoples]}
    return jsonify(response_body), 200

@app.route('/people/<int:id>',methods=['GET'])
def get_a_char(id):
    character=Characters.get_a_people(id)
    if character is None:
        return jsonify({"msg":"id no encontrada"}), 404
    response_body = {"Character": character.serialize()}
    return jsonify(response_body), 200

@app.route('/planets',methods=['GET'])
def get_all_planets():
    planets = Planets.get_all_planets()
    response_body = {"Planets": [planet.serialize() for planet in planets]}
    return jsonify(response_body), 200

@app.route('/planets/<int:id>',methods=['GET'])
def get_a_planet(id):
    planet=Planets.get_a_planet(id)
    if planet is None:
        return jsonify({"msg":"id no encontrada"}), 404
    response_body = {"Planet": planet.serialize()}
    return jsonify(response_body), 200

@app.route('/users',methods=['GET'])
def get_all_users():
    users = User.get_all_users()
    response_body = {"Users": [user.serialize() for user in users]}
    return jsonify(response_body), 200

@app.route('/users/favorites',methods=['GET'])
def get_all_favorites():
    fav_planets = Fav_planet.get_all_fav_planets()
    fav_characters = Fav_char.get_all_fav_characters()
    response_body = {
        "Fav_planets": [fav_planet.serialize() for fav_planet in fav_planets],
        "Fav_characters": [fav_char.serialize() for fav_char in fav_characters]
    }
    return jsonify(response_body), 200

@app.route('/favorites/planet/<int:id>',methods=['POST'])
def add_fav_planet(id):
    user_id = request.json.get("user_id")
    if not user_id:
        return jsonify({"msg": "user_id is required"}), 400
    Fav_planet.add_fav_planet(user_id, id)
    return jsonify({"msg": "Favorite planet added successfully"}), 201

@app.route('/favorites/character/<int:id>',methods=['POST'])
def add_fav_character(id):
    user_id = request.json.get("user_id")
    if not user_id:
        return jsonify({"msg": "user_id is required"}), 400
    Fav_char.add_fav_char(user_id, id)
    return jsonify({"msg": "Favorite character added successfully"}), 201

@app.route('/favorites/planet/<int:id>',methods=['DELETE'])
def delete_fav_planet(id):
    deleted = Fav_planet.delete_planet(id)
    if not deleted:
        return jsonify({"msg": "Favorite planet not found"}), 404
    return jsonify({"msg": "Favorite planet deleted successfully"}), 200

@app.route('/favorites/character/<int:id>',methods=['DELETE'])
def delete_fav_character(id):
    deleted = Fav_char.delete_character(id)
    if not deleted:
        return jsonify({"msg": "Favorite character not found"}), 404
    return jsonify({"msg": "Favorite character deleted successfully"}), 200