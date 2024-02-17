from flask import request, jsonify, render_template
from models.baby_model import BabyRepository, Baby
from configs import logger

baby_repo = BabyRepository()

def add_baby():
    match request.get_json():
        case {'first_name': first_name, 'last_name': last_name, 'born_timestamp': born_timestamp}:
            logger.info(f"Request is valid. Values {first_name} {last_name} {born_timestamp}")
            baby_repo.save_baby(Baby(first_name=first_name, last_name=last_name, born_timestamp=born_timestamp))
            return jsonify({'message': 'Baby added successfully'}), 201
        case _:
            logger.info(f"Request is invalid")
            return jsonify({'message': 'Request is invalid. Please provide first_name, last_name and born_timestamp for a new baby'}), 400    


def get_all_babies():
    return jsonify(baby_repo.get_all())
