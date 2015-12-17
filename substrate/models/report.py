"""Parent class for GEO record subclasses: GeoDataset (GDS), GeoProfile (GSE),
and GeoPlatform (GPL).
"""

from substrate import db


class Report(db.Model):

    __tablename__ = 'report'
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(32), nullable=False)
    report_type = db.Column(db.Text, nullable=False)

    __mapper_args__ = {'polymorphic_on': report_type}

    # Back references.
    tag = db.relationship(
        'SoftFile',
        uselist=False,
        backref=db.backref('dataset', order_by=id)
    )

    def __init__(self, **kwargs):
        self.link = kwargs['link']

    def __repr__(self):
        return '<Report %r>' % self.id
