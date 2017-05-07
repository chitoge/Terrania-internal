from .. import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    hashed_id = db.Column(db.String, unique=True) # should be unique, if it's not, then congratulations, you've found another SHA-1 collision!
    creator = db.Column()
    continent = db.Column(db.String(16))
    language = db.Column(db.String(16))
    question_count = db.Column(db.Integer)
    question_answered = db.Column(db.Integer)
    game_type = db.Column(db.String)
    current_question = db.Column(db.PickleType)
    value = db.Column(db.Integer)
    past_countries = db.Column(db.PickleType)

    def __repr__(self):
        return 'Game {}>'.format(self.id)

# internal data
class Country(db.Model):
    name = db.Column(db.String, unique=True)
    region = db.Column(db.String)
    country_code = db.Column(db.String, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    capital = db.Column(db.String)
    population = db.Column(db.Integer)
    area = db.Column(db.Integer)
    coastline = db.Column(db.Integer)
    currency = db.Column(db.String)
    dialing_prefix = db.Column(db.Integer)
    birth_rate = db.Column(db.Float)
    death_rate = db.Column(db.Float)
    life_expectancy = db.Column(db.Float)

    def __repr__(self):
        return 'Country {}'.format(self.country_code)
