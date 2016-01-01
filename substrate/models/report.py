"""Parent class for GEN3VA reports.
"""

from substrate import db, HierClustVisualization, PCAVisualization


gene_signature_to_report = db.Table(
    'gene_signature_to_report',
    db.metadata,
    db.Column('gene_signature_fk', db.Integer,
              db.ForeignKey('gene_signature.id')),
    db.Column('report_fk', db.Integer, db.ForeignKey('report.id'))
)


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

    # Back references.
    gene_signatures = db.relationship(
        'GeneSignature',
        secondary=gene_signature_to_report,
        backref=db.backref('reports', order_by=id)
    )

    PROCESSING = 'processing'
    READY = 'ready'
    CUSTOM = 'custom'

    def __init__(self, report_type, tag):
        self.status = self.PROCESSING
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
        self.status = self.PROCESSING

    @property
    def ready(self):
        return self.status == self.READY

    @property
    def processing(self):
        return self.status == self.PROCESSING

    @property
    def custom(self):
        return self.report_type == self.CUSTOM
