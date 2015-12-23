"""Parent class for GEN3VA reports.
"""

from substrate import db


class Report(db.Model):

    __tablename__ = 'report'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String, nullable=False)
    report_type = db.Column(db.Text, nullable=False)
    tag_fk = db.Column(db.Integer, db.ForeignKey('tag.id'))

    links = db.relationship(
        'TargetAppLink',
        backref=db.backref('report', order_by=id)
    )

    # TODO: Implement custom vs tag-based reporting.
    #__mapper_args__ = {'polymorphic_on': report_type}

    def __init__(self, report_type, tag):
        self.status = 'pending'
        self.report_type = report_type
        self.tag = tag
        self.links = []

    def __repr__(self):
        return '<Report %r>' % self.id

    def set_link(self, link):
        self.links.append(link)

    def set_pca_visualization(self, pca_visualization):
        self.pca_visualization = pca_visualization

    @property
    def ready(self):
        return self.status == 'ready'

    @property
    def pending(self):
        return self.status == 'pending'
