"""Represents person, group, course, entity, etc. that collected gene
signatures for a tag.
"""

from substrate import db


class EnrichmentTerm(db.Model):

    __tablename__ = 'enrichment_term'
    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.Integer)
    name = db.Column(db.String(255))
    combined_score = db.Column(db.Float)

    enrichr_result_fk = db.Column(
        db.Integer,
        db.ForeignKey('enrichr_result.id')
    )

    enrichr_results = db.relationship('EnrichrResults',
                                      backref='enrichment_terms')

    def __init__(self, rank, name, combined_score):
        self.rank = rank
        self.name = name
        self.combined_score = combined_score

    def __repr__(self):
        return '<EnrichmentTerm %r>' % self.id
