#! /usr/bin/env python

import os
import unittest

from flask_script import Manager

from app import create_app, db
import utils

app = create_app(os.getenv('APP_CONFIG', 'default'))
manager = Manager(app)

@manager.option('-p', '--csv-path', dest='path', default='data/countries_translated.csv')
def initdb(path):
    "(Re)initializes the database file. Run it with -p to import a custom CSV file."
    db.drop_all()
    db.create_all()
    utils.import_country_data(path, db)

@manager.command
def test():
    "Run all currently available tests"
    tests = unittest.TestLoader().discover('tests', pattern='*.py')
    unittest.TextTestRunner(verbosity=3).run(tests)

@manager.shell
def make_shell_context():
    return dict(app=app, db=db, utils=utils)
 
if __name__ == '__main__':
    manager.run()
