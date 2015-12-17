"""Parent class for GEN3VA reports.
"""

from substrate import db


class Report(db.Model):

    __tablename__ = 'report'
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(32), nullable=False)
    report_type = db.Column(db.Text, nullable=False)
    tag_fk = db.Column(db.Integer, db.ForeignKey('tag.id'))

    # TODO: Implement custom vs tag-based reporting.
    #__mapper_args__ = {'polymorphic_on': report_type}

    def __init__(self, **kwargs):
        self.link = kwargs['link']
        self.status = kwargs['status']
        self.report_type = kwargs['report_type']
        self.tag_fk = kwargs['tag_fk']

    def __repr__(self):
        return '<Report %r>' % self.id
