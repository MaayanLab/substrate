"""Parent class for GEN3VA reports.
"""

import requests
from requests.exceptions import RequestException

from substrate import db, HeatMap, PCAPlot


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
    tag_fk = db.Column(db.Integer, db.ForeignKey('tag.id'))

    heat_maps = db.relationship(
        'HeatMap',
        backref=db.backref('report', order_by=id)
    )

    pca_plot = db.relationship(
        'PCAPlot',
        uselist=False,
        backref=db.backref('report', order_by=id)
    )

    # Back references.
    gene_signatures = db.relationship(
        'GeneSignature',
        secondary=gene_signature_to_report,
        backref=db.backref('reports', order_by=id)
    )

    def __init__(self, tag):
        self.tag = tag
        self.heat_maps = []
        self.pca_plot = None

    def __repr__(self):
        return '<Report %r>' % self.id

    def add_heat_map(self, heat_map):
        """Adds a heat map (hierarchical clustering) to report.
        """
        self.heat_maps.append(heat_map)

    def reset(self):
        """Deletes all associated visualizations for report.
        """
        for heat_map in self.heat_maps:
            HeatMap \
                .query \
                .filter_by(id=heat_map.id) \
                .delete()

        if self.pca_plot:
            PCAPlot \
                .query \
                .filter_by(id=self.pca_plot.id) \
                .delete()

    @property
    def l1000cds2_heat_map(self):
        """Returns the L1000CDS2 heat map if it exists, None otherwise.
        """
        for viz in self.heat_maps:
            if viz.viz_type == 'l1000cds2':
                return viz
        return None

    @property
    def genes_heat_map(self):
        """Returns the L1000CDS2 heat map if it exists, None otherwise.
        """
        for viz in self.heat_maps:
            if viz.viz_type == 'gen3va':
                return viz
        return None

    @property
    def enrichr_heat_maps(self):
        return [viz for viz in self.heat_maps if viz.viz_type == 'enrichr']

    @property
    def gene_signatures(self):
        """Returns the gene signatures associated with report.
        """
        return self.tag.gene_signatures

    @property
    def ready(self):
        """Returns True if the PCA visualization or at least one hierarchical
        clustering visualization is ready.
        """
        CLUSTERGRAMMER_URL = 'http://amp.pharm.mssm.edu/clustergrammer/status_check/'
        if self.pca_plot:
            return True
        for viz in self.heat_maps:
            clustergrammer_id = viz.link.split('/')[-2:-1][0]
            url = CLUSTERGRAMMER_URL + str(clustergrammer_id)
            try:
                resp = requests.get(url)
                if resp.text == 'finished':
                    return True
            except RequestException as e:
                print(e)
                return False
        return False
