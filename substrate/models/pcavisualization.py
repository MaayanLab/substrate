"""PCA visualization of a gene signatures in a report.
"""

from substrate import db


class PCAVisualization(db.Model):

    __tablename__ = 'pca_visualization'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Binary, nullable=False)
    report_fk = db.Column(db.Integer, db.ForeignKey('report.id'))

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return '<PCAVisualization %r>' % self.id