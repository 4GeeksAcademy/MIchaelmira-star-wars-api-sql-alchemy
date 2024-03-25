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
        characters_dictionaries = [character.serialize() for character in characters]
        return jsonify(characters_dictionaries), 200
    
@app.route('/characters/<int:people_id>', methods=['PUT'])
def update_person(people_id):
    character = Character.query.get(people_id)
    character_data = request.json 
    if character:    
        character.name=character_data["name"],
        character.height=character_data["height"],
        character.mass=character_data["mass"],
        character.hair_color=character_data["hair_color"],
        character.skin_color=character_data["skin_color"],
        character.eye_color=character_data["eye_color"],
        character.birth_year=character_data["birth_year"],
        character.gender=character_data["gender"],
        character.homeworld=character_data["homeworld"]
        db.session.commit()
        return jsonify({"msg": "Edit Character success"}), 200
    else :
        return jsonify({"msg": "The character Id you provided does not exist" }), 404
    
        
@app.route('/characters/<int:people_id>', methods=['DELETE'])
def delete_person(people_id):
    character = Character.query.get(people_id)
    favorites = Favorite.query.filter_by(character_id = people_id)
    for favorite in favorites:
        db.session.delete(favorite)
        db.session.commit()
    if character:
        db.session.delete(character)
        db.session.commit()
        return jsonify({"msg": "DELETE Character success"}), 200
    else:
        return jsonify({"msg": "The character Id you provided does not exist" }), 404
    
@app.route('/characters/<int:people_id>', methods=['GET'])
def handle_person(people_id):
    character = Character.query.get(people_id)

    if character is None:
        return jsonify({"message": "Character not found"}), 404
    else:
        return jsonify(character.serialize()), 200
    
@app.route('/planets', methods=['GET', 'POST'])
def handle_planets():
    if request.method == 'POST':
        planet_data = request.json 
        new_planet = Planet(
            name=planet_data["name"],
            diameter=planet_data["diameter"],
            rotation_period=planet_data["rotation_period"],
            orbital_period=planet_data["orbital_period"],
            gravity=planet_data["gravity"],
            population=planet_data["population"],
            climate=planet_data["climate"],
            terrain=planet_data["terrain"],
            surface_water=planet_data["surface_water"],
            planet_pic=planet_data["planet_pic"]
        )
        db.session.add(new_planet)
        db.session.commit()
        return jsonify(new_planet.serialize()), 201
    else:
        planets = Planet.query.all()
        planets_dictionaries = [planet.serialize() for planet in planets]
        return jsonify(planets_dictionaries), 200
    
@app.route('/planets/<int:planets_id>', methods=['GET'])
def handle_planet(planets_id):
    planet = Planet.query.get(planets_id)

    if planet is None:
        return jsonify({"message": "Planets not found"}), 404
    else:
        return jsonify(planet.serialize()), 200
    
@app.route('/planets/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    planet = Planet.query.get(planet_id)
    planet_data = request.json 
    if planet:    
        planet.name=planet_data["name"],
        planet.diameter=planet_data["diameter"],
        planet.rotation_period=planet_data["rotation_period"],
        planet.orbital_period=planet_data["orbital_period"],
        planet.gravity=planet_data["gravity"],
        planet.population=planet_data["population"],
        planet.climate=planet_data["climate"],
        planet.terrain=planet_data["terrain"],
        planet.surface_water=planet_data["surface_water"],
        planet.planet_pic=planet_data["planet_pic"]
        db.session.commit()
        return jsonify({"msg": "Edit Planet success"}), 200
    else :
        return jsonify({"msg": "The planets Id you provided does not exist" }), 404
    
@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)
    favorites = Favorite.query.filter_by(planet_id = planet_id)
    for favorite in favorites:
        db.session.delete(favorite)
        db.session.commit()
    if planet:
        db.session.delete(planet)
        db.session.commit()
        return jsonify({"msg": "DELETE Planet success"}), 200
    else:
        return jsonify({"msg": "The planet Id you provided does not exist" }), 404
    
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
        favorites_dictionaries = [favorite.serialize() for favorite in favorites]
        return jsonify(favorites_dictionaries), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():

    # Retrieve all favorites belonging to the current user
    user_favorites = Favorite.query.all()
    if request.method == "GET":
        if user_favorites is None:
            return jsonify({"message": "No Favorite Found"}), 404
        
        else:
            return jsonify(data=[user_favorites.serialize() for user_favorites in user_favorites]), 200
        
@app.route('/users/favorites/<int:user_id>', methods=['GET'])
def get_one_favorite(user_id):
    one_favorite = Favorite.query.all()[user_id]
    returned_favorites = {
        "favorite_character": one_favorite.character_id,
        "favorite_planet": one_favorite.planet_id
    }
    return jsonify(data=[returned_favorites])

@app.route('/favorites/characters/<int:character_id>', methods=['POST'])
def post_favorite_character(character_id):
    data = request.get_json()
    if data is None or "user_id" not in data:
        return jsonify({"error": "Invalid request data"}), 400

    user_id = data["user_id"]

    
    newFavorite = Favorite (character_id = character_id, user_id = user_id, name = 0000) 
    
    db.session.add(newFavorite)
    db.session.commit()
    returned_favorites = Favorite.query.filter_by(user_id=user_id).first()

    return jsonify("Character Added to Favorites!", returned_favorites.serialize())

@app.route('/favorites/planets/<int:planet_id>', methods=['POST'])
def post_favorite_planet(planet_id):
    data = request.get_json()
    if data is None or "user_id" not in data:
        return jsonify({"error": "Invalid request data"}), 400

    user_id = data["user_id"]
    favorite = Planet.query.filter_by(id=planet_id).first()
    
    newFavorite = Favorite (planet_id = planet_id, user_id = user_id, name = favorite.name) 
    
    db.session.add(newFavorite)
    db.session.commit()
    returned_favorites = Favorite.query.filter_by(user_id=user_id).first()

    return jsonify("Planet Added to Favorites!", returned_favorites.serialize())
    
@app.route('/favorites/<int:favorite_id>', methods = ['DELETE'])
def delete_favorite(favorite_id):
    

    if request.method == "DELETE":
        remove_character = Favorite.query.get(favorite_id)
        db.session.delete(remove_character)
        db.session.commit()
        return jsonify("Removed Character Successfully!"), 200 
    return "Post or Delete requests were invalid", 404




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
