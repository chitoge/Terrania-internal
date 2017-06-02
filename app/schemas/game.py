from .. import ma
from ..models.game import Game
from marshmallow import fields, validates, ValidationError
from marshmallow.validate import Range, OneOf
from ..core.question_generators import generators

class GameSchema(ma.Schema):
    hashed_id = fields.Str()

class GameRequestSchema(ma.Schema):
    type = fields.Str(required=True, validate=OneOf(generators))
    question_count = fields.Int(required=True, validate=Range(min=0))
    language = fields.Str(default='en')
    continent = fields.Str(default='World')

class DataTypeSchema(ma.Schema):
    type = fields.Str(required=True)
    data = fields.Str(required=True)
    title = fields.Str(default='')

class QuestionSchema(ma.Schema):
    question = fields.Nested(DataTypeSchema)
    answers = fields.Nested(DataTypeSchema, many=True)
    question_type = fields.Str(required=True)

class AnswerSchema(ma.Schema):
    answer = fields.Int(required=True, validate=Range(min=0, max=3))

class AnswerResponseSchema(ma.Schema):
    recorded_answer = fields.Int()
    correct_answer = fields.Int()
    current_score = fields.Int()

game_schema = GameSchema()
games_schema = GameSchema(many=True)
question_schema = QuestionSchema()
answer_schema = AnswerSchema()
answer_response_schema = AnswerResponseSchema()
game_request_schema = GameRequestSchema()
