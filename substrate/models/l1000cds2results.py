"""Represents results from L1000CDS2.
"""

import json
import requests

from .. import db


class L1000CDS2Results(db.Model):

    __tablename__ = 'l1000cds2_result'
    id = db.Column(db.Integer, primary_key=True)
    share_id = db.Column(db.String(255))
    is_up = db.Column(db.Boolean)

    gene_signature_fk = db.Column(
        db.Integer,
        db.ForeignKey('gene_signature.id')
    )

    def __init__(self, share_id, is_up):
        self.share_id = share_id
        self.is_up = is_up

    def __repr__(self):
        return '<L1000CDS2Results %r>' % self.id

    @property
    def is_mimic(self):
        return self.is_up

    def get_perturbations(self):
        if self.perturbations:
            return self.perturbations
        return []

    @property
    def link(self):
        return self.L1000CDS2_URL + '#/result/' + self.share_id
