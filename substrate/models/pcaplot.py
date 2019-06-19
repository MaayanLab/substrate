"""PCA plot of a gene signatures in a report.
"""

from .. import db


class PCAPlot(db.Model):

    __tablename__ = 'pca_plot'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Binary, nullable=False)
    report_fk = db.Column(db.Integer, db.ForeignKey('report.id'))

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return '<PCAPlot %r>' % self.id

    def to_json(self):
        # self.data is already serialized JSON, stored in the database.
        return self.data
