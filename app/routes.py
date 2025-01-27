from app import db
from app.models.planet import Planet
from flask import Blueprint, jsonify, make_response, request, abort

# create an instance of Blueprint and assign to variable planets_bp
planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))

    planet = cls.query.get(model_id)

    if not planet:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))

    return planet


@planets_bp.route("", methods=["POST"])
def create_planet():
    request_body = request.get_json()
    new_planet = Planet.from_dict(request_body)
    # new_planet = Planet(
    #     name=request_body["name"],
    #     description=request_body["description"],
    #     type=request_body["type"]
    # )

    db.session.add(new_planet)
    db.session.commit()

    return make_response(jsonify(f"Planet {new_planet.name} successfully created"), 201)


@planets_bp.route("", methods=["GET"])
def get_all_planets():
    name_query = request.args.get("name")
    if name_query:
        planets = Planet.query.filter_by(name=name_query)
    else:
        planets = Planet.query.all()

    planets_response = []
    # planets = Planet.query.all()

    for planet in planets:
        planets_response.append(planet.to_dict())
            # {
            #     "id": planet.id,
            #     "name": planet.name,
            #     "description": planet.description,
            #     "type": planet.type
            # }

    return jsonify(planets_response)


@planets_bp.route("/<planet_id>", methods=["GET"])
def read_one_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    return planet.to_dict()
    # return {
    #     "id": planet.id,
    #     "name": planet.name,
    #     "description": planet.description,
    #     "type": planet.type
    # }


@planets_bp.route("/<planet_id>", methods=["PUT"])
def update_planet(planet_id):
    """Updates one existing planet data"""
    planet = validate_model(Planet, planet_id)

    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.type = request_body["type"]

    db.session.commit()

    return make_response(jsonify(f"Planet #{planet_id} successfully updated"))


@planets_bp.route("/<planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    """Deletes one eexisting planet data"""
    planet = validate_model(Planet, planet_id)

    db.session.delete(planet)
    db.session.commit()

    return make_response(jsonify(f"Planet #{planet.id} successfully deleted"))


# class Planet:
#     """Create class Planet"""

#     def __init__(self, id, name, description, type):
#         """Constructor with class attributes"""
#         self.id = id
#         self.name = name
#         self.description = description
#         self.type = type


# # Create a list of instances of class Planet for each planet in our solar system.
# planets = [
#     Planet(1, "Mercury", "Smallest planet in the solar system. Its year is 88 days long. Closest to the Sun.", "Rocky/Terrestrial"),
#     Planet(2, "Venus", "Hottest planet in the solar system. Has a thick, toxic atmosphere. Second planet from the Sun.", "Rocky/Terrestrial"),
#     Planet(3, "Earth", "Water world rich with life. Third rock from the Sun.",
#            "Rocky/Terrestrial"),
#     Planet(4, "Mars", "Cold and desert-like; iron oxide makes it look red. Fourth planet from the Sun.", "Rocky/Terrestrial"),
#     Planet(5, "Jupiter", "Largest planet in the solar system; home to the Great Red Spot. Fifth planet from the Sun.", "Gas giant"),
#     Planet(6, "Saturn", "Known for its large and distinct planetary ring. Sixth planet from the Sun.", "Gas giant"),
#     Planet(7, "Uranus", "Orbits on its side! Clouds of hydrogen sulfide makes it smell like rotten eggs. Seventh planet from the Sun.", "Ice giant"),
#     Planet(8, "Neptune", "Coldest planet in the solar system; stormy and bright blue. Eighth planet from the Sun.", "Ice giant"),
# ]

# @planets_bp.route("", methods=["GET"])
# def show_all_planets():
#     """Response body in JSON format for a request to see all planetary information."""
#     planets_response = []
#     for planet in planets:
#         planets_response.append(
#             {
#                 "id": planet.id,
#                 "name": planet.name,
#                 "description": planet.description,
#                 "type": planet.type,
#             }
#         )
#     return jsonify(planets_response)

# Defines an endpoint that returns a response for one planet with its id, title, description, and type


# @planets_bp.route("/<planet_id>", methods=["GET"])
# def validate_model(planet_id):
#     """Helper function that handles invalid planet_id"""
#     try:
#         planet_id = int(planet_id)
#     except:
#         abort(make_response({"message": f"planet {planet_id} invalid"}, 400))

#     for planet in planets:
#         if planet.id == planet_id:
#             return planet
#     abort(make_response({"message": f"planet {planet_id}, not found"}, 404))


# def display_one_planet(planet_id):
#     """Returns response body: dictionary literal for one planet with matching planet_id"""
#     planet = validate_model(planet_id)

#     return {
#         "id": planet.id,
#         "name": planet.name,
#         "description": planet.description,
#         "type": planet.type
#     }
