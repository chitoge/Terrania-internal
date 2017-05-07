from flask import jsonify, request

from . import api
from .. import db
from ..models.game import Game
from ..schemas.game import game_schema, games_schema

# POST a new game
@api.route('/games/new', methods=['POST'])
def post_new_game():
    pass

# GET current game question
@api.route('/games/<int:id>/question', methods=['GET'])
def get_game_question(id):
    pass

# POST an answer to this current question, associated with that game
@api.route('/games/<int:id>/answer', methods=['POST'])
def post_game_answer(id):
    pass