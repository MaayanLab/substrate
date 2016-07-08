"""Represents results from L1000CDS2.
"""

import json
import requests

from substrate import db


class L1000CDS2Results(db.Model):

    __tablename__ = 'l1000cds2_result'
    id = db.Column(db.Integer, primary_key=True)
    share_id = db.Column(db.String(255))
    is_up = db.Column(db.Boolean)
    gene_signature_fk = db.Column(
        db.Integer,
        db.ForeignKey('gene_signature.id')
    )

    L1000CDS2_URL = 'http://amp.pharm.mssm.edu/L1000CDS2/'

    def __init__(self, share_id, is_up):
        self.share_id = share_id
        self.is_up = is_up

    def __repr__(self):
        return '<L1000CDS2Results %r>' % self.id

    @property
    def is_mimic(self):
        return self.is_up

    @property
    def perts_scores(self):
        url = self.L1000CDS2_URL + self.share_id
        resp = requests.get(url)
        data = json.loads(resp.text)['results']
        perts = []
        scores = []
        top_meta = data['topMeta']

        for obj in top_meta:
            desc_temp = obj['pert_desc']
            if desc_temp == '-666':
                desc_temp = obj['pert_id']
            pert = '%s - %s' % (desc_temp, obj['cell_id'])

            # L1000CDS^2 gives scores from 0 to 2. With mimic, low scores are
            # better; with reverse, high scores are better. If we subtract
            # this score from 1, we get a negative value for reverse and a
            # positive value for mimic.
            score = 1 - obj['score']
            perts.append(pert)
            scores.append(score)

        return perts, scores

    @property
    def link(self):
        return self.L1000CDS2_URL + '#/result/' + self.share_id
