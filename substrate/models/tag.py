"""Represents a metadata tag for aggregating signatures.
"""

from .. import db


gene_signature_to_tag = db.Table(
    'gene_signature_to_tag',
    db.metadata,
    db.Column('gene_signature_fk', db.Integer,
              db.ForeignKey('gene_signature.id')),
    db.Column('tag_fk', db.Integer, db.ForeignKey('tag.id'))
)


class Tag(db.Model):

    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    curator_fk = db.Column(db.Integer,
                           db.ForeignKey('curator.id'),
                           nullable=True)
    bio_category_fk = db.Column(db.Integer,
                                db.ForeignKey('bio_category.id'),
                                nullable=True)
    is_restricted = db.Column(db.Boolean)

    # Back references.
    gene_signatures = db.relationship(
        'GeneSignature',
        secondary=gene_signature_to_tag,
        backref=db.backref('tags', order_by=id)
    )

    reports = db.relationship('Report', backref=db.backref('tag', order_by=id))

    def __init__(self, name, is_restricted=False):
        self.name = name
        self.is_restricted = is_restricted

    @property
    def approved_report(self):
        """Returns the approved report if it exists, None otherwise.
        """
        for report in self.reports:
            if report.is_approved:
                return report
        return None

    @property
    def custom_reports(self):
        """Returns custom reports, i.e. those that are not approved.
        """
        results = []
        for report in self.reports:
            if not report.is_approved:
                results.append(report)
        return results

    def __repr__(self):
        return '<Tag %r>' % self.id
