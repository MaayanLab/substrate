"""Represents a SoftFile, either from GEO or a user upload, with a link to
the cleaned file and associated metadata.
"""

from substrate import db


class SoftFile(db.Model):
    """Metadata for the processed SOFT file.
    """
    __tablename__ = 'soft_file'
    id = db.Column(db.Integer, primary_key=True)

    gene_signature_fk = db.Column(db.Integer, db.ForeignKey('gene_signature.id'), nullable=False)
    dataset_fk = db.Column(db.Integer, db.ForeignKey('dataset.id'), nullable=False)
    samples = db.relationship('SoftFileSample', backref='soft_files')

    normalize = db.Column(db.Boolean)
    text_file = db.Column(db.String(255))

    # TODO: Drop after transfering data!
    is_geo = db.Column(db.Boolean)
    name = db.Column(db.String(200))

    def __init__(self, samples, dataset, text_file, genes, a_vals, b_vals, normalize=False, stats=None):
        """Constructs a SoftFile instance.
        """
        self.samples = samples
        self.dataset = dataset
        self.text_file = text_file
        self.normalize = normalize

        # These are *not* persisted to the database. Used by diffexp module.
        self.genes = genes
        self.a_vals = a_vals
        self.b_vals = b_vals
        self.stats = stats

    def __repr__(self):
        return '<SoftFile %r>' % self.id

    @property
    def serialize(self):
        """Return serialized object.
        """
        if hasattr(self.dataset, 'platform'):
            platform = self.dataset.platform
        else:
            platform = None

        if hasattr(self.dataset, 'accession'):
            accession = self.dataset.accession
        else:
            accession = None

        if self.samples:
            selected_samples = [{'name':x.name, 'is_control':x.is_control} for x in self.samples]
        else:
            selected_samples = 'na'

        return {
            'title': self.dataset.title,
            'accession': accession,
            'normalize': self.normalize,
            'is_geo': self.dataset.record_type == 'geo',
            'platform': platform,
            'organism': self.dataset.organism,
            'text_file': self.text_file,
            'selected_samples': selected_samples
        }
