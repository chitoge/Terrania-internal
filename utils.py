# contain various utilities like CSV importing
import csv
from app.models.game import Country

# import a country file CSV given file name
def import_country_data(filename, db):
    with open(filename, 'rb') as f:
        reader = csv.DictReader(f, delimiter=';', quotechar='"')
        for row in reader:
            country = Country(row['country'].decode('utf8'), row['region'], row['country_code'], row['latitude'], row['longitude'], row['capital'].decode('utf8'), row['population'], row['area'], row['coastline'], row['currency'].decode('utf8'), row['dialling_prefix'], row['birth_rate'], row['death_rate'], row['life_expectancy'])
            db.session.add(country)
        db.session.commit()