"""A visualization from a supported downstream analysis application.
"""


from substrate import db


class HierClustVisualization(db.Model):

    __tablename__ = 'hier_clust_visualization'
    id = db.Column(db.Integer, primary_key=True)
    target_app_fk = db.Column(db.Integer, db.ForeignKey('target_app.id'))
    report_fk = db.Column(db.Integer, db.ForeignKey('report.id'))

    link = db.Column(db.Text)
    viz_type = db.Column(db.String(255))
    enrichr_library = db.Column(db.String(255))

    def __init__(self, link, viz_type, target_app, enrichr_library=None):
        self.link = link
        if viz_type not in ['enrichr', 'l1000cds2']:
            raise ValueError('viz_type must be "enrichr" or "l1000cds2"')
        self.viz_type = viz_type
        self.target_app = target_app
        self.enrichr_library = enrichr_library

    def __repr__(self):
        return '<HierClustVisualization %r>' % self.id
