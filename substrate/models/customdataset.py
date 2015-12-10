"""Custom data source record uploaded by user.
"""

from substrate.models.dataset import Dataset


class CustomDataset(Dataset):

    __mapper_args__ = {'polymorphic_identity': 'custom'}

    def __init__(self, **kwargs):
        super(CustomDataset, self).__init__(**kwargs)

    def __repr__(self):
        return '<CustomDataset %r>' % self.id
