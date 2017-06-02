# contain various utilities like CSV importing
import csv
from app.models.game import Country
from app.models.i18n import Translation
from os import listdir
from os.path import isfile, join

# import a country file CSV given file name
def import_country_data(filename, db):
    # load list of flags file
    flagfiles = [f for f in listdir('data/flags/') if isfile(join('data/flags/', f))]
    with open(filename, 'rb') as f:
        reader = csv.DictReader(f, delimiter=';', quotechar='"')
        for row in reader:
            # check if there exists a flag that corresponds to this country
            if ((row['country_code'].lower() + '.png') not in flagfiles):
                raise AttributeError("Can't find the flag file for " + row['country'])
            name = Translation({'en': row['country'].decode('utf8'), 'vi': row['country_vi'].decode('utf8')})
            capital = Translation({'en': row['capital'].decode('utf8'), 'vi': row['capital_vi'].decode('utf8')})
            country = Country(name, row['region'], row['country_code'], row['latitude'], row['longitude'], capital, row['population'], row['area'], row['coastline'], row['currency'].decode('utf8'), row['dialling_prefix'], row['birth_rate'], row['death_rate'], row['life_expectancy'])
            db.session.add_all([name, capital, country])
            db.session.commit()