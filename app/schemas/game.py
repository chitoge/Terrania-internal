from .. import ma
from ..models.game import Game


class GameSchema(ma.ModelSchema):

    class Meta:
        model = Game


game_schema = GameSchema()
games_schema = GameSchema(many=True)
