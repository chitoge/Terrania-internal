from .. import db

class Translation(db.Model):
    __tablename__ = 'translations'
    id = db.Column(db.Integer, primary_key=True)
    # a dictionary of translations, seems like broken normal form, right?
    translations = db.Column(db.PickleType)

    def __repr__(self):
        return '<Translation {} ({})>'.format(self.id, self.translations['en'])

    def get_translation(self, language):
        if (language not in self.translations):
            # fall back to English
            language = 'en'
        return self.translations[language]

    def __init__(self, trans):
        # check if given translations arg a dictionary
        if not (isinstance(trans, dict)):
            raise TypeError('Translations must be stored in a dict')
        # check for mandatory English translation
        if not ('en' in trans):
            raise TypeError("English translation is required but couldn't be found")
        self.translations = trans

    @staticmethod
    def translate(obj, language):
        res = obj
        # find all i18n fields in object
        for f in dir(obj):
            if (f.startswith('i18n_') and (not f.endswith('_id'))):
                setattr(res, f[5:], getattr(obj, f).get_translation(language))
        return res
