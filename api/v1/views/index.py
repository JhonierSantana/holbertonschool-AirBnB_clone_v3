#!/usr/bin/python3
"""Index file for Flask"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def r_json():
    """a route for return JSON status """
    return jsonify(status='OK')


@app_views.route('/api/v1/stats', strict_slashes=False)
def count_clases():
    classes = {"amenities": Amenity, "cities": City,
               "places": Place, "reviews": Review,
               "states": State, "users": User}
    ret_dict = dict()
    for name, cls in classes.items():
        ret_dict[name] = storage.count(cls)
    return (jsonify(ret_dict))
