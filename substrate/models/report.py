"""Parent class for GEN3VA reports.
"""

from substrate import db


class Report(db.Model):

    __tablename__ = 'report'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String, nullable=False)
    report_type = db.Column(db.Text, nullable=False)
    tag_fk = db.Column(db.Integer, db.ForeignKey('tag.id'))

    # TODO: Implement custom vs tag-based reporting.
    #__mapper_args__ = {'polymorphic_on': report_type}

    def __init__(self, report_type, tag):
        self.status = 'pending'
        self.report_type = report_type
        self.tag = tag
        # Generate link

    def __repr__(self):
        return '<Report %r>' % self.id

    @property
    def ready(self):
        return self.status == 'ready'

    @property
    def pending(self):
        return self.status == 'pending'
