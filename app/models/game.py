from .. import db
import os
from ..core.question_generators import generators

# internal data
class Country(db.Model):
    i18n_name_id = db.Column(db.Integer, db.ForeignKey('translations.id'))
    i18n_name = db.relationship("Translation", foreign_keys=[i18n_name_id])
    region = db.Column(db.String)
    country_code = db.Column(db.String, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    i18n_capital_id = db.Column(db.Integer, db.ForeignKey('translations.id'))
    i18n_capital = db.relationship("Translation", foreign_keys=[i18n_capital_id])
    population = db.Column(db.Integer)
    area = db.Column(db.Integer)
    coastline = db.Column(db.Integer)
    currency = db.Column(db.Unicode)
    dialing_prefix = db.Column(db.Integer)
    birth_rate = db.Column(db.Float)
    death_rate = db.Column(db.Float)
    life_expectancy = db.Column(db.Float)

    def __init__(self, name, region, country_code, latitude, longitude, capital, population, area, coastline, currency, dialing_prefix, birth_rate, death_rate, life_expectancy):
        self.i18n_name = name
        self.region = region
        self.country_code = country_code
        self.latitude = latitude
        self.longitude = longitude
        self.i18n_capital = capital
        self.population = population
        self.area = area
        self.coastline = coastline
        self.currency = currency
        self.dialing_prefix = dialing_prefix
        self.birth_rate = birth_rate
        self.death_rate = death_rate
        self.life_expectancy = life_expectancy

    def __repr__(self):
        return '<Country {}>'.format(self.country_code)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Additional fields
    hashed_id = db.Column(db.String, unique=True) # should be unique, if it's not, then congratulations, you've found another SHA-1 collision!
    #creator = db.Column()
    continent = db.Column(db.String(16))
    language = db.Column(db.String(16))
    question_count = db.Column(db.Integer)
    question_id = db.Column(db.Integer)
    game_type = db.Column(db.String)
    current_question = db.Column(db.PickleType, nullable=True)
    value = db.Column(db.Integer)
    past_countries = db.Column(db.PickleType)

    def __init__(self, continent, language, question_count, game_type):
        # TODO: attribute with an user for rate-limiting mechanism
        # for now, we'll generate signature with just urandom()
        self.hashed_id = os.urandom(20).encode('hex')
        self.continent = continent
        self.language = language
        self.question_count = question_count
        self.question_id = 0
        self.game_type = game_type
        self.current_question = None
        self.value = 0
        self.past_countries = []

    def __repr__(self):
        return '<Game {}>'.format(self.id)

    def next_question(self):
        # if we generated enough questions then stop
        if (self.question_id >= self.question_count):
            self.current_question = None
            return
        # generate candidate list on-the-fly to reduce storage cost
        if (self.continent == 'all'):
            candidates = db.session.query(Country)
        else:
            candidates = db.session.query(Country).filter(Country.region == self.continent)
        generator = generators[self.game_type](self.past_countries, candidates, self.language)
        self.current_question, data_tag = generator.generate()
        self.past_countries.append((self.current_question.choices[self.current_question.correct_answer].country_code, data_tag))
        self.question_id += 1
