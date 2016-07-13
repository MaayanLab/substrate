"""Parent class for GEN3VA reports.
"""

import json
import requests
from requests.exceptions import RequestException

from substrate import db, EnrichrResults, L1000CDS2Results, HeatMap, PCAPlot


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
    name = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(255), nullable=True)
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
    _gene_signatures = db.relationship(
        'GeneSignature',
        secondary=gene_signature_to_report,
        backref=db.backref('reports', order_by=id)
    )

    def __init__(self, tag, _gene_signatures=None, contact=None,
                 is_approved=False, name=None, category=None):
        self.tag = tag

        if not _gene_signatures:
            self._gene_signatures = self.tag.gene_signatures
        else:
            # Report can be built on any subset of gene signatures from a tag.
            subset = set(_gene_signatures)
            superset = set(self.tag.gene_signatures)
            if not subset.issubset(superset):
                msg = 'Gene signatures must be subset of tag\'s signatures.'
                raise ValueError(msg)
            self._gene_signatures = _gene_signatures

        self.contact = contact
        self.is_approved = is_approved
        self.name = name
        self.heat_maps = []
        self.pca_plot = None

    def __repr__(self):
        return '<Report %r>' % self.id

    @property
    def gene_signatures(self):
        """Returns the correct gene signatures per report type if they exist.
        """

        # If this is a newer report and has self._gene_signatures correctly
        # set, then use those signatures.
        if len(self._gene_signatures) > 0:
            return self._gene_signatures

        # When a new approved report is created, we should automatically take
        # set self._gene_signature to the tag's signatures. But for older
        # reports, we want to make sure they still work.
        elif self.is_approved:
            return self.tag.gene_signatures

        # What happens if the report is not approved and there are no
        # signatures in self._gene_signatures? Too bad. We'll need to rebuild
        # that custom report.
        return []

    def reset(self, reanalyze=False):
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

        if reanalyze:
            for sig in self.gene_signatures:
                EnrichrResults.query.filter_by(gene_signature_fk=sig.id)\
                    .delete()
                L1000CDS2Results.query.filter_by(gene_signature_fk=sig.id)\
                    .delete()

    @property
    def ready(self):
        """Returns True if the PCA visualization or at least one hierarchical
        clustering visualization is ready.
        """
        if self.pca_plot:
            return True
        for hm in self.heat_maps:
            if hm.network:
                return True
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

    @property
    def genes_heat_map(self):
        """Returns the genes heat map if it exists, None otherwise.
        """
        for viz in self.heat_maps:
            if viz.viz_type == 'gen3va':
                return viz
        return None

    @property
    def l1000cds2_heat_map(self):
        """Returns the L1000CDS2 heat map if it exists, None otherwise.
        """
        for viz in self.heat_maps:
            if viz.viz_type == 'l1000cds2':
                return viz
        return None

    @property
    def enrichr_heat_maps(self):
        """Returns a list of Enrichr heat maps if any exist, an empty list
        otherwise.
        """
        return [viz.to_dict() for viz in self.heat_maps if viz.viz_type == 'enrichr']
