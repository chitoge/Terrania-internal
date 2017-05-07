from .. import ma
from ..models.game import Game
from marshmallow import fields, validates

class GameSchema(ma.Schema):
    hashed_id = fields.Str()

class DataTypeSchema(ma.Schema):
    type = fields.Str(required=True)
    data = fields.Str(required=True)
    title = fields.Str(default='')

class QuestionSchema(ma.Schema):
    question = fields.Nested(DataTypeSchema)
    answers = fields.Nested(DataTypeSchema, many=True)

class AnswerSchema(ma.Schema):
    answer = fields.Int(required=True)

    @validates('answer')
    def validate_answer_range(self, value):
        if (value < 0) or (value > 3):
            raise TypeError('Invalid answer value.')

class AnswerResponseSchema(ma.Schema):
    recorded_answer = fields.Int()
    correct_answer = fields.Int()
    current_score = fields.Int()

game_schema = GameSchema()
games_schema = GameSchema(many=True)
question_schema = QuestionSchema()
answer_schema = AnswerSchema()
answer_response_schema = AnswerResponseSchema()
