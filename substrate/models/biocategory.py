"""Represents a biological category that groups tags into meaningful
subsets.
"""

from .. import db


class BioCategory(db.Model):

    __tablename__ = 'bio_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    order = db.Column(db.Integer)
    tags = db.relationship('Tag',
                           backref=db.backref('bio_category', order_by=id))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<BioCategory %r>' % self.id
