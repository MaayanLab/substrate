"""Resource for a set of gene signatures.
"""


from substrate import db


class Resource(db.Model):

    __tablename__ = 'resource'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(255))
    name = db.Column(db.String(255))

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __repr__(self):
        return '<Resource %r>' % self.id
