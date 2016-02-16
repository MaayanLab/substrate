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
    is_approved = db.Column(db.Boolean, default=False)
    contact = db.Column(db.String(255), nullable=True)
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

    def __init__(self, tag, contact=None, is_approved=False):
        self.tag = tag
        self.contact = contact
        self.is_approved = is_approved
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
        """Returns a list of Enrichr heat maps if any exist, an empty list
        otherwise.
        """
        return [viz for viz in self.heat_maps if viz.viz_type == 'enrichr']

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

    def complete(self, enrichr_libraries):
        """Returns True if:

        - The PCA plot is ready.
        - All heat maps are ready.
        - The number of heat maps is equal to the number of supported Enrichr
          libraries, plus the genes and L1000CDS2 heat maps.

        False otherwise.
        """
        if not self.pca_plot:
            return False
        if len(self.heat_maps) != len(enrichr_libraries) + 2:
            return False
        return self.ready
