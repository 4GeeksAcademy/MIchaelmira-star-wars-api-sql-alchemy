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
from models import db, User, Favorite, Character, Planet
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



@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'POST':
        user_data = request.json 
        new_user = User(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.serialize()), 201
    else:
        users = User.query.all()
        # users_dictionaries = []
        # for user in users:
        #     users_dictionaries.append(
        #         user.serialize()
        #     )
        users_dictionaries= [user.serialize() for user in users]
        return jsonify(users_dictionaries), 200
    
@app.route('/favorites', methods=['GET', 'POST'])
def handle_favorites():
    if request.method == 'POST':
        favorite_data = request.json 
        new_favorite = Favorite(
            name=favorite_data["name"]
        )
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify(new_favorite.serialize()), 201
    else:
        favorites = Favorite.query.all()
        # favorites_dictionaries = []
        # for favorite in favorites:
        #     favorites_dictionaries.append(
        #         favorite.serialize()
        #     )
        favorites_dictionaries = [favorite.serialize() for favorite in favorites]
        return jsonify(favorites_dictionaries), 200
    
@app.route('/characters', methods=['GET', 'POST'])
def handle_characters():
    if request.method == 'POST':
        character_data = request.json 
        new_character = Character(
            name=character_data["name"],
            height=character_data["height"],
            mass=character_data["mass"],
            hair_color=character_data["hair_color"],
            skin_color=character_data["skin_color"],
            eye_color=character_data["eye_color"],
            birth_year=character_data["birth_year"],
            gender=character_data["gender"],
            homeworld=character_data["homeworld"]
        )
        db.session.add(new_character)
        db.session.commit()
        return jsonify(new_character.serialize()), 201
    else:
        characters = Character.query.all()
        # favorites_dictionaries = []
        # for favorite in favorites:
        #     favorites_dictionaries.append(
        #         favorite.serialize()
        #     )
        characters_dictionaries = [character.serialize() for character in characters]
        return jsonify(characters_dictionaries), 200
    
@app.route('/planets', methods=['GET', 'POST'])
def handle_planets():
    if request.method == 'POST':
        planet_data = request.json 
        new_planet = Planet(
            name=planet_data["name"],
            height=planet_data["height"],
            mass=planet_data["mass"],
            hair_color=planet_data["hair_color"],
            skin_color=planet_data["skin_color"],
            eye_color=planet_data["eye_color"],
            birth_year=planet_data["birth_year"],
            gender=planet_data["gender"],
            homeworld=planet_data["homeworld"]
        )
        db.session.add(new_planet)
        db.session.commit()
        return jsonify(new_planet.serialize()), 201
    else:
        planets = Planet.query.all()
        # favorites_dictionaries = []
        # for favorite in favorites:
        #     favorites_dictionaries.append(
        #         favorite.serialize()
        #     )
        planets_dictionaries = [planet.serialize() for planet in planets]
        return jsonify(planets_dictionaries), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
