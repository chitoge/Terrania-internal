from .. import db

class Translation(db.Model):
    __tablename__ = 'translations'
    id = db.Column(db.Integer, primary_key=True)
    translations = db.Column(db.PickleType)

    def __repr__(self):
        return '<Translation {} ({})>'.format(self.id, self.translations['en'])

    def get_translation(self, language):
        if (language not in self.translations):
            # fall back to English
            language = 'en'
        return self.translations[language]

    def __init__(self, trans):
        self.translations = trans

    @staticmethod
    def translate(obj, language):
        res = obj
        # find all i18n fields in object
        for f in dir(obj):
            if (f.startswith('i18n_') and (not f.endswith('_id'))):
                setattr(res, f[5:], getattr(obj, f).get_translation(language))
        return res
