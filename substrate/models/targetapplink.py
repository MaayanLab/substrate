"""A supported downstream target application.
"""

from substrate import db


class TargetAppLink(db.Model):

    __tablename__ = 'target_app_link'
    id = db.Column(db.Integer, primary_key=True)
    target_app_fk = db.Column(db.Integer, db.ForeignKey('target_app.id'))
    gene_list_fk = db.Column(db.Integer, db.ForeignKey('gene_list.id'))
    link = db.Column(db.Text)
    gene_list_direction = db.Column(db.Integer)

    def __init__(self, target_app, gene_list_direction, link):
        self.target_app = target_app
        self.link = link
        self.gene_list_direction = gene_list_direction

    def __repr__(self):
        return '<TargetAppLink %r>' % self.id