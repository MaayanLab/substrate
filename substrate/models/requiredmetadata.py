"""Required metadata for a gene signature extraction.
"""


from .. import db


class RequiredMetadata(db.Model):

    __tablename__ = 'required_metadata'
    id = db.Column(db.Integer, primary_key=True)
    diff_exp_method = db.Column(db.String(255))
    ttest_correction_method = db.Column(db.String(255))
    cutoff = db.Column(db.Integer)
    threshold = db.Column(db.Float)
    gene_signature_fk = db.Column(db.Integer, db.ForeignKey('gene_signature.id'))

    def __init__(self, cutoff, threshold, diff_exp_method, ttest_correction_method):
        """Constructs a Metadata instance.
        """
        self.cutoff = cutoff
        self.threshold = threshold
        self.diff_exp_method = diff_exp_method
        self.ttest_correction_method = ttest_correction_method

    def __repr__(self):
        return '<RequiredMetadata %r>' % self.id

    def __str__(self):
        """Stringifies the metadata instance.
        """
        # This is used primarily for sending a description to third-party
        # target applications.
        result = []
        for key,val in self.__dict__.items():
            # Ignore SQLAlchemy relationships, e.g. gene_signature_fk.
            if key == '_sa_instance_state':
                continue
            if val:
                result.append(str(val))
        return '-'.join(result)

    @property
    def serialize(self):
        return {
            'cutoff': self.cutoff,
            'threshold': self.threshold,
            'diff_exp_method': self.diff_exp_method,
            'ttest_correction_method': self.ttest_correction_method
        }
