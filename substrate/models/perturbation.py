"""Represents person, group, course, entity, etc. that collected gene
signatures for a tag.
"""

from .. import db


class Perturbation(db.Model):

    __tablename__ = 'perturbation'
    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Integer)
    name = db.Column(db.String(255))
    score = db.Column(db.Float)
    
    l1000cds2_result_fk = db.Column(
        db.Integer,
        db.ForeignKey('l1000cds2_result.id')
    )

    l1000cds2_results = db.relationship('L1000CDS2Results',
                                        backref='perturbations')

    def __init__(self, rank, name, score):
        self.rank = rank
        self.name = name
        self.score = score

    def __repr__(self):
        return '<Perturbation %r>' % self.id
