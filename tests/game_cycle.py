from flask import Flask
from flask_testing import TestCase, LiveServerTestCase
from app import create_app, db
from utils import import_country_data
import random
import json
from app.core.question_generators import generators

# Test how a game should be played

class OrdinaryPlayTest(TestCase):
    def create_app(self):
        app = create_app('testing')
        return app

    @classmethod
    def setUpClass(self):
        db.create_all()
        import_country_data('data/countries_translated.csv', db)

    def runTest(self):
        # randomly choose a game mode, with 10 questions, for whole world, in English
        chosen_game_type = random.choice(list(generators))
        print '[+] Chosen game type to test = {}'.format(chosen_game_type) 
        payload = json.dumps({'continent': 'World', 'question_count': 10, 'type': chosen_game_type, 'language': 'en'})
        resp = self.client.post('/api/games/new', content_type='application/json', data=payload)
        self.assert200(resp)
        self.assertIn(u'hashed_id', resp.json)
        game_id = resp.json[u'hashed_id'].encode('utf8')
        for i in xrange(10):
            resp = self.client.get('/api/games/{}/question'.format(game_id))
            self.assert200(resp)
            # check question format
            self.assertIn(u'question', resp.json)
            self.assertIn(u'answers', resp.json)
            self.assertEquals(len(resp.json['answers']), 4)
            # another request should not change the question if the client did not respond
            another_resp = self.client.get('/api/games/{}/question'.format(game_id))
            self.assertDictEqual(resp.json, another_resp.json)
            # responds randomly with zero
            resp = self.client.post('/api/games/{}/answer'.format(game_id), content_type='application/json', data=json.dumps({'answer': 0}))
            # check answer back format
            self.assertIn(u'correct_answer', resp.json)
            self.assertIn(u'recorded_answer', resp.json)
            self.assertIn(u'current_score', resp.json)
        # question ran out, should stahp
        # can i post answer again? should be 303
        resp = self.client.post('/api/games/{}/answer'.format(game_id), content_type='application/json', data=json.dumps({'answer': 0}))
        self.assertEqual(resp.status_code, 303)
        resp = self.client.get('/api/games/{}/question'.format(game_id))
        self.assertEqual(resp.status_code, 303)
            