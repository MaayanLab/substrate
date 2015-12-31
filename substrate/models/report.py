"""Parent class for GEN3VA reports.
"""

from substrate import db, HierClustVisualization, PCAVisualization

PROCESSING = 'processing'
READY = 'ready'


class Report(db.Model):
    __tablename__ = 'report'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String, nullable=False)
    report_type = db.Column(db.String, nullable=False)
    tag_fk = db.Column(db.Integer, db.ForeignKey('tag.id'))

    hier_clusts = db.relationship(
        'HierClustVisualization',
        backref=db.backref('report', order_by=id)
    )

    pca_visualization = db.relationship(
        'PCAVisualization',
        uselist=False,
        backref=db.backref('report', order_by=id)
    )

    # TODO: Implement custom vs tag-based reporting.
    # __mapper_args__ = {'polymorphic_on': report_type}

    def __init__(self, report_type, tag):
        self.status = PROCESSING
        self.report_type = report_type
        self.tag = tag
        self.hier_clusts = []

    def __repr__(self):
        return '<Report %r>' % self.id

    def set_hier_clust(self, hier_clust):
        self.hier_clusts.append(hier_clust)

    def set_pca_visualization(self, pca_visualization):
        self.pca_visualization = pca_visualization

    def reset(self):
        for hier_clust in self.hier_clusts:
            HierClustVisualization \
                .query \
                .filter_by(id=hier_clust.id) \
                .delete()

        if self.pca_visualization:
            PCAVisualization \
                .query \
                .filter_by(id=self.pca_visualization.id) \
                .delete()
        self.status = PROCESSING

    @property
    def ready(self):
        return self.status == READY

    @property
    def processing(self):
        return self.status == PROCESSING
