"""Creates a GeneSignature, which represents a single instance of a user's
processed data, with links to the SOFT file, gene lists, and metadata.
"""


import hashlib
import time

from substrate import db


class GeneSignature(db.Model):

    __tablename__ = 'gene_signature'
    id = db.Column(db.Integer, primary_key=True)
    # This is a hexadecimal hash of the time that the extraction occured. This
    # is how the front-end identifies the dataset, so that we do not display
    # the actual database ID to the users.
    extraction_id = db.Column(db.String(10))
    soft_file = db.relationship(
        'SoftFile',
        uselist=False,
        backref='gene_signature'
    )
    gene_lists = db.relationship(
        'GeneList',
        backref=db.backref('gene_signatures', order_by=id)
    )
    required_metadata = db.relationship(
        'RequiredMetadata',
        uselist=False,
        backref=db.backref('gene_signature', order_by=id)
    )
    optional_metadata = db.relationship(
        'OptionalMetadata',
        backref=db.backref('gene_signatures', order_by=id)
    )
    resource = db.relationship(
        'Resource',
        backref=db.backref('gene_signatures', order_by=id)
    )

    def __init__(self, soft_file, gene_lists, required_metadata, optional_metadata, tags):
        """Construct an Extraction instance. This is called only by class
        methods.
        """
        # This is *not* the database ID. This is hashed so that users cannot
        # simply guess the ID for other user's data.
        self.extraction_id = hashlib.sha1(str(time.time())).hexdigest()[:10]
        self.soft_file = soft_file
        self.gene_lists = gene_lists
        self.required_metadata = required_metadata
        self.optional_metadata = optional_metadata
        self.tags = tags

    def __repr__(self):
        return '<GeneSignature %r>' % self.id

    def get_optional_metadata(self, name):
        name = name.lower()
        for opt in self.optional_metadata:
            if opt.name.lower() == name:
                return opt
        return None

    @property
    def serialize(self):
        return {
            'extraction_id': self.extraction_id,
            'soft_file': self.soft_file.serialize,
            'gene_lists': [gl.serialize for gl in self.gene_lists],
            'required_metadata': self.required_metadata.serialize,
            'optional_metadata': {om.name: om.value for om in self.optional_metadata},
            'tags': [t.name for t in self.tags]
        }
