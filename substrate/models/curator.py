"""Represents person, group, course, entity, etc. that collected gene
signatures for a tag.
"""

from substrate import db


class Curator(db.Model):

    __tablename__ = 'curator'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    # Back references.
    tags = db.relationship('Tag', backref='curator')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Curator %r>' % self.id
