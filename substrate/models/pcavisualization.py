"""Unique gene symbol in a table of canonical symbols.
"""

from substrate import db


class PCAVisualization(db.Model):

    __tablename__ = 'pca_visualization'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Binary, nullable=False)
    report_fk = db.relationship(
        'Report',
        backref=db.backref('pca_visualization', order_by=id)
    )

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return '<PCAVisualization %r>' % self.id