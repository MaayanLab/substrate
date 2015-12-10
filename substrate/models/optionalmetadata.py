"""Optional metadata for a gene signature extraction.
"""

from substrate import db


class OptionalMetadata(db.Model):

    __tablename__ = 'optional_metadata'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    value = db.Column(db.String(255))
    gene_signature_fk = db.Column(
        db.Integer,
        db.ForeignKey('gene_signature.id')
    )

    def __init__(self, name, value):
        """Constructs a Metadata instance.
        """
        self.name = name
        self.value = value

    def __repr__(self):
        return '<OptionalMetadata %r>' % self.id
