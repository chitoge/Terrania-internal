from flask import Flask
from flask_testing import TestCase, LiveServerTestCase
from app import create_app, db
from utils import import_country_data

class LiveTest(LiveServerTestCase):
    def create_app(self):
        app = create_app('testing')
        # random port for not colliding
        app.config['LIVESERVER_PORT'] = 0
        return app

    def setUp(self):
        db.create_all()
        import_country_data('data/countries_translated.csv', db)

    def tearDown(self):
        pass

    def test_up_and_running(self):
        print self.get_server_url()