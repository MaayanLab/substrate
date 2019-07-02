"""Creates a GeneSignature, which represents a single instance of a user's
processed data, with links to the SOFT file, gene lists, and metadata.
"""


import hashlib
import time

from .. import db


class GeneSignature(db.Model):

    __tablename__ = 'gene_signature'
    id = db.Column(db.Integer, primary_key=True)
    # This is a hexadecimal hash of the time that the extraction occured. This
    # is how the front-end identifies the dataset, so that we do not display
    # the actual database ID to the users.
    extraction_id = db.Column(db.String(10))
    resource_fk = db.Column(
        db.Integer,
        db.ForeignKey('resource.id')
    )
    _name = db.Column(db.Integer, nullable=True)

    soft_file = db.relationship(
        'SoftFile',
        uselist=False,
        backref='gene_signature'
    )
    gene_lists = db.relationship(
        'GeneList',
        backref=db.backref('gene_signature', order_by=id)
    )
    required_metadata = db.relationship(
        'RequiredMetadata',
        uselist=False,
        backref=db.backref('gene_signature', order_by=id)
    )
    optional_metadata = db.relationship(
        'OptionalMetadata',
        backref=db.backref('gene_signature', order_by=id)
    )
    l1000cds2_results = db.relationship(
        'L1000CDS2Results',
        backref=db.backref('gene_signature', order_by=id)
    )
    enrichr_results = db.relationship(
        'EnrichrResults',
        backref=db.backref('gene_signature', order_by=id)
    )

    def __init__(self, soft_file, gene_lists, required_metadata,
                 optional_metadata, tags, resource, _name=None):
        """Construct an Extraction instance. This is called only by class
        methods.
        """
        # This is *not* the database ID. This is hashed so that users cannot
        # simply guess the ID for other user's data.
        self.extraction_id = hashlib.sha1(str(time.time()).encode()).hexdigest()[:10]
        self.soft_file = soft_file
        self.gene_lists = gene_lists
        self.required_metadata = required_metadata
        self.optional_metadata = optional_metadata
        self.tags = tags
        self.resource = resource
        self._name = _name

    def __repr__(self):
        return '<GeneSignature %r>' % self.id

    @property
    def name(self):
        """Returns the most specific name for the gene signature, depending on
        the SOFT file name, the dataset title or the extraction ID.
        """
        if self._name:
            return self._name

        # Return the GEO dataset title or SOFT file name if possible.
        if self.is_from_geo:
            sf = self.soft_file
            ds = sf.dataset
            if ds.title:
                return ds.title
            if sf.name:
                return sf.name

        # Munge some metadata to construct a name if possible.
        if len(self.filtered_optional_metadata) > 0:
            return '_'.join([x.value for x in
                             self.filtered_optional_metadata])

        # Return the extraction ID.
        return self.extraction_id

    @property
    def combined_genes(self):
        """Returns combined gene list.
        """
        return self._genes_by_direction(0)

    @property
    def up_genes(self):
        """Returns up gene list.
        """
        # If we have an up, down, and combined gene list, find the correct
        # one. Otherwise, create it manually.
        if len(self.gene_lists) == 3:
            return self._genes_by_direction(1)
        return [x for x in self.combined_genes if x.value > 0]

    @property
    def down_genes(self):
        """Returns down gene list.
        """
        if len(self.gene_lists) == 3:
            return self._genes_by_direction(-1)
        return []#[x for x in self.combined_genes if x.value and x.value < 0]

    def gene_list_by_direction(self, direction):
        """Returns correct gene list based on direction.
        """
        for gl in self.gene_lists:
            if gl.direction == direction:
                return gl
        return None

    def _genes_by_direction(self, direction):
        """Returns correct ranked genes based on direction.
        """
        gl = self.gene_list_by_direction(direction)
        if gl:
            return gl.ranked_genes
        return None

    @property
    def filtered_optional_metadata(self):
        """Utility method that returns optional metadata, filtering out
        private metadata that we don't want users to see.
        """
        results = []
        for om in self.optional_metadata:
            if (not om.value or
                om.value.strip() == '' or
                om.name == 'user_key' or
                om.name == 'userKey' or
                om.name == 'userEmail' or
                om.name == 'user_email'
            ):
                continue

            results.append(om)
        return results

    @property
    def organism(self):
        """Returns organism if it exists, None otherwise.
        """
        if self.is_from_geo:
            return self.soft_file.dataset.organism
        opt_meta = self.get_optional_metadata('organism')
        if opt_meta:
            return opt_meta.value
        return None

    @property
    def platform(self):
        """Returns platform if it exists, None otherwise.
        """
        if self.is_from_geo:
            return self.soft_file.dataset.organism
        opt_meta = self.get_optional_metadata('platform')
        if opt_meta:
            return opt_meta.value
        return None

    @property
    def is_from_geo(self):
        """Returns True if gene signature was extracted from GEO, False
        otherwise.
        """
        return self.resource.code == 'geo'

    def get_optional_metadata(self, name):
        """Returns optional metadata value if it exists, None otherwise.
        """
        if type(name) is str or type(name) is unicode:
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

    def get_l1000cds2_results(self, use_mimic):
        """Returns the correct L1000CDS2 results if they exist.
        """
        for r in self.l1000cds2_results:
            if r.is_up == use_mimic:
                return r
        return None

    def get_enrichr_results(self, is_up, library):
        """Returns the correct Enrichr results if they exist.
        """
        for r in self.enrichr_results:
            if r.is_up == is_up and r.library == library:
                return r
        return None
