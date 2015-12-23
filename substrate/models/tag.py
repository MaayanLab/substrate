"""Groups the Extraction class's various experimental metadata as user inputs.
"""

from substrate import db


gene_signatures_to_tags = db.Table(
    'gene_signatures_to_tags',
    db.metadata,
    db.Column(
        'gene_signature_fk',
        db.Integer,
        db.ForeignKey('gene_signature.id')
    ),
    db.Column('tag_fk', db.Integer, db.ForeignKey('tag.id'))
)


class Tag(db.Model):

    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    is_curated = db.Column(db.Boolean)

    # Back references.
    gene_signatures = db.relationship(
        'GeneSignature',
        secondary=gene_signatures_to_tags,
        backref=db.backref('tags', order_by=id)
    )

    reports = db.relationship(
        'Report',
        backref=db.backref('tag', order_by=id)
    )

    def __init__(self, name, is_curated=False):
        self.name = name
        self.is_curated = is_curated

    def __repr__(self):
        return '<Tag %r>' % self.id