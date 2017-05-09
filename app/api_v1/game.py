from flask import jsonify, request
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from . import api
from .. import db
from ..models.game import Game
from ..schemas.game import game_schema, games_schema, question_schema, answer_schema, answer_response_schema
from ..core.question_generators import generators

# cache
def nocache(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

# POST a new game
@api.route('/games/new', methods=['POST'])
def post_new_game():
    print request.json
    if True:
        if ('continent' in request.json):
            continent = request.json['continent']
        else:
            continent = 'World'

        if ('language' in request.json):
            language = request.json['language']
        else:
            language = 'en'

        if ('type' in request.json):
            game_type = request.json['type']
        else:
            game_type = 'flag2country'

        game = Game(continent, language, request.json['question_count'], game_type)
        game.next_question()
        db.session.add(game)
        db.session.commit()
        return game_schema.jsonify(game)
    else:
        res = jsonify({'status': 404, 'message': 'Invalid parameters'})
        res.status_code = 404
        return res
    
# GET current game question
@api.route('/games/<string:id>/question', methods=['GET'])
def get_game_question(id):
    try:
        question, generator_name, language = db.session.query(Game.current_question, Game.game_type, Game.language).filter(Game.hashed_id == id).one()
        if (question == None):
            # no more questions
            res = jsonify({'status': 303, 'message': 'No more questions for this game'})
            res.status_code = 303
            return res
        print question
        generator = generators[generator_name]([], [], language)
        return nocache(question_schema.jsonify(generator.view(question)))
    except MultipleResultsFound, e:
        res = jsonify({'status': 404, 'message': 'Invalid parameters'})
        res.status_code = 404
        return nocache(res)
    except NoResultFound, e:
        res = jsonify({'status': 404, 'message': 'Game not found'})
        res.status_code = 404
        return nocache(res)

# POST an answer to this current question, associated with that game
@api.route('/games/<string:id>/answer', methods=['POST'])
def post_game_answer(id):
    try:
        game = db.session.query(Game).filter(Game.hashed_id == id).one()
        # end of game
        if (game.current_question == None):
            res = jsonify({'status': 303, 'message': 'No more questions for this game'})
            res.status_code = 303
            return res
        data, errors = answer_schema.load(request.get_json())
        answer = data['answer']
        # hopefully no race condition here
        if (game.current_question.validate(answer)):
            game.value += 10
        res = dict(recorded_answer=answer, correct_answer=game.current_question.correct_answer, current_score=game.value)
        if (game.question_id >= game.question_count):
            game.current_question = None
        else:
            game.next_question()
        db.session.commit()
        return answer_response_schema.jsonify(res)
    except MultipleResultsFound, e:
        res = jsonify({'status': 404, 'message': 'Invalid parameters'})
        res.status_code = 404
        return res
    except NoResultFound, e:
        res = jsonify({'status': 404, 'message': 'Game not found'})
        res.status_code = 404
        return res
    except TypeError, e:
        res = jsonify({'status': 404, 'message': e.message})
        res.status_code = 404
        return res