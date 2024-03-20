from flask import Blueprint, jsonify
from services.movie_service import get_producers_intervals

producer_blueprint = Blueprint('producers', __name__)

@producer_blueprint.route('/producers/worsts', methods=['GET'])
def get_intervals():
    intervals = get_producers_intervals()
    return jsonify(intervals), 200
