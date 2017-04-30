from flask import jsonify, request

from . import api
from .. import db
from ..models.game import Game
from ..schemas.game import game_schema, games_schema


@api.route('/games', methods=['GET'])
def get_games():
    pass


@api.route('/games/<int:id>', methods=['GET'])
def get_game(id):
    pass


@api.route('/games/<int:id>', methods=['PUT'])
def update_game(id):
    pass
