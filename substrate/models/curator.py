"""Represents person, group, course, entity, etc. that collected gene
signatures for a tag.
"""

from substrate import db


class Curator(db.Model):

    __tablename__ = 'curator'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    # Back references.
    tags = db.relationship(
        'Tag',
        backref=db.backref('curator', order_by=id)
    )

    def __init__(self, name, is_curated=False):
        self.name = name
        self.is_curated = is_curated

    def __repr__(self):
        return '<Curator %r>' % self.id
