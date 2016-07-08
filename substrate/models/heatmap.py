"""A visualization from a supported downstream analysis application.
"""

import json

from substrate import db


class HeatMap(db.Model):

    __tablename__ = 'heat_map'
    id = db.Column(db.Integer, primary_key=True)
    report_fk = db.Column(db.Integer, db.ForeignKey('report.id'))
    network = db.Column(db.Text)

    # We want to deploy a new version of GEN3VA that works with both links and
    # networks. Any newly created heat maps should have network data rather
    # than links to Clustergrammer. Set this to an empty string for now.
    link = db.Column(db.Text, default='')

    viz_type = db.Column(db.String(255))
    enrichr_library = db.Column(db.String(255))

    def __init__(self, network, viz_type, enrichr_library=None):
        self.network = network
        if viz_type not in ['enrichr', 'l1000cds2', 'gen3va']:
            raise ValueError('source must be "enrichr", "l1000cds2", or "gen3va"')
        self.viz_type = viz_type
        self.enrichr_library = enrichr_library

    def __repr__(self):
        return '<HeatMap %r>' % self.id

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        # Network is a JSON string stored in the database. We want to convert
        # it to a Python dictionary.
        network = json.loads(self.network)
        return {
            'network': network,
            'link': self.link,
            'viz_type': self.viz_type,
            'enrichr_library': self.enrichr_library
        }
