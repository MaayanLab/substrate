"""A visualization from a supported downstream analysis application.
"""


from substrate import db


class HierClustVisualization(db.Model):

    __tablename__ = 'hier_clust_visualization'
    id = db.Column(db.Integer, primary_key=True)
    target_app_fk = db.Column(db.Integer, db.ForeignKey('target_app.id'))
    report_fk = db.Column(db.Integer, db.ForeignKey('report.id'))

    title = db.Column(db.String)
    description = db.Column(db.Text)
    link = db.Column(db.Text)

    def __init__(self, title, description, link, viz_type, target_app):
        self.title = title
        self.description = description
        self.link = link
        if viz_type not in ['enrichr', 'l1000cds2']:
            raise ValueError('viz_type must be "enrichr" or "l1000cds2"')
        self.viz_type = viz_type
        self.target_app = target_app

    def __repr__(self):
        return '<Visualization %r>' % self.id
