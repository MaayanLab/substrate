"""Represents results from enrichment analysis via Enrichr.
"""

import json
import requests

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

    ENRICHR_URL = 'http://amp.pharm.mssm.edu/Enrichr/'

    def __init__(self, user_list_id, is_up):
        self.user_list_id = user_list_id
        self.is_up = is_up

    def __repr__(self):
        return '<EnrichrResults %r>' % self.id

    def terms_scores(self, library):
        url = self.ENRICHR_URL + 'enrich?userListId=%s&backgroundType=%s' % (
            self.user_list_id, library
        )
        resp = requests.get(url)
        if not resp.ok:
            raise Exception('Error fetching enrichment results.')

        results = json.loads(resp.text)[library]
        terms = []
        scores = []
        for r in results:
            term = r[1]
            p_value = r[2]
            combined_score = r[4]
            if p_value > 0.05:
                continue
            if combined_score < 0:
                continue
            terms.append(term)
            scores.append(combined_score)
        return terms[:50], scores[:50]
