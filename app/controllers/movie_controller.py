from flask import Blueprint, jsonify, request
from services.movie_service import import_csv_to_database
from werkzeug.exceptions import BadRequest

movie_blueprint = Blueprint('movies', __name__)

@movie_blueprint.route('/movies/import', methods=['PUT'])
def import_data():
    try:
        data = request.json
        file_path_or_url = data.get('file_path_or_url')   
        import_csv_to_database(file_path_or_url)
        return jsonify({'status': 'succeeded'}), 200

    except BadRequest as e:
        return jsonify({'status': 'failed', "reason": str(e) }), 400
    except Exception as e:
        # print(type(e))
        return jsonify({'status': 'failed', "reason": str(e) }), 500
