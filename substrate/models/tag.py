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

    # Back references.
    gene_signatures = db.relationship(
        'GeneSignature',
        secondary=gene_signatures_to_tags,
        backref=db.backref('tags', order_by=id)
    )
    reports = db.relationship(
        'Report',
        backref=db.backref('report', order_by=id)
    )

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tag %r>' % self.id