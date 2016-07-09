"""Represents results from enrichment analysis via Enrichr.
"""

from substrate import db


class EnrichrResults(db.Model):

    __tablename__ = 'enrichr_result'
    id = db.Column(db.Integer, primary_key=True)
    user_list_id = db.Column(db.String(255))
    is_up = db.Column(db.Boolean)
    gene_signature_fk = db.Column(
        db.Integer,
        db.ForeignKey('gene_signature.id')
    )
    library = db.Column(db.String)

    def __init__(self, user_list_id, is_up, library):
        self.user_list_id = user_list_id
        self.is_up = is_up
        self.library = library

    def __repr__(self):
        return '<EnrichrResults %r>' % self.id

    def get_enrichment_terms(self, cutoff=50):
        if self.enrichment_terms:
            return self.enrichment_terms[:cutoff]
        return []
