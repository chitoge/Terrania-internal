from .. import db


class Game(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    # Additional fields

    def __repr__(self):
        return 'Game {}>'.format(self.id)
