#!/usr/bin/python3
"""
This module defines routes related to Place objects in a Flask web application.

It includes routes for:
- Listing all Place objects in a specified City.
- Retrieving a specific Place object.
- Deleting a specific Place object.
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from datetime import datetime
import uuid


@app_views.route('/cities/<city_id>/places', methods=['GET'])
@app_views.route('/cities/<city_id>/places/', methods=['GET'])
def list_places_of_city(city_id):
    '''Retrieves a list of all Place objects in a specified city.

    Args:
        city_id (str): The ID of the city whose places are to be listed.

    Returns:
        Response: A JSON response containing a list of Place objects in the specified city.

    Raises:
        404: If the city with the given ID does not exist.
    '''
    all_cities = storage.all("City").values()
    city_obj = [obj.to_dict() for obj in all_cities if obj.id == city_id]
    if not city_obj:
        abort(404)
    list_places = [obj.to_dict() for obj in storage.all("Place").values()
                   if city_id == obj.city_id]
    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    '''Retrieves a specific Place object.

    Args:
        place_id (str): The ID of the Place object to be retrieved.

    Returns:
        Response: A JSON response containing the details of the Place object.

    Raises:
        404: If the Place object with the given ID does not exist.
    '''
    all_places = storage.all("Place").values()
    place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
    if not place_obj:
        abort(404)
    return jsonify(place_obj[0])


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    '''Deletes a specific Place object.

    Args:
        place_id (str): The ID of the Place object to be deleted.

    Returns:
        Response: An empty JSON response with a status code 200.

    Raises:
        404: If the Place object with the given ID does not exist.
    '''
    all_places = storage.all("Place").values()
    place_obj = [obj.to_dict() for obj in all_places if obj.id == place_id]
    if not place_obj:
        abort(404)
    place_obj.remove(place_obj[0])
    for obj in all_places:
        if obj.id == place_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200
