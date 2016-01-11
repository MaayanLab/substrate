"""Parent class for GEN3VA reports.
"""

import requests
from requests.exceptions import RequestException

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
    CLUSTERGRAMMER_URL = 'http://amp.pharm.mssm.edu/clustergrammer/status_check/'

    def __init__(self, tag):
        self.status = self.PROCESSING
        self.tag = tag
        self.hier_clusts = []

    def __repr__(self):
        return '<Report %r>' % self.id

    def add_hier_clust(self, hier_clust):
        """Adds a hierarchical clustering visualization to report.
        """
        self.hier_clusts.append(hier_clust)

    def set_pca_visualization(self, pca_visualization):
        """Sets the PCA visualization to report.
        """
        self.pca_visualization = pca_visualization

    def reset(self):
        """Deletes all associated visualizations for report.
        """
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

    @property
    def gene_signatures(self):
        """Returns the gene signatures associated with report.
        """
        return self.tag.gene_signatures

    @property
    def ready(self):
        """Returns True if at least one hierarchical clustering visualization
        is ready.
        """
        for viz in self.hier_clusts:
            clustergrammer_id = viz.link.split('/')[-2:-1][0]
            url = self.CLUSTERGRAMMER_URL + str(clustergrammer_id)
            try:
                resp = requests.get(url)
                if resp.text == 'finished':
                    return True
            except RequestException as e:
                print(e)
                return False
        return False
