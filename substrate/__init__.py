"""Configures substrate's API.
"""


from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()

from models.customdataset import CustomDataset as CustomDataset
from models.dataset import Dataset as Dataset
from models.gene import Gene as Gene
from models.genelist import GeneList as GeneList
from models.genesignature import GeneSignature as GeneSignature
from models.geodataset import GeoDataset as GeoDataset
from models.optionalmetadata import OptionalMetadata as OptionalMetadata
from models.rankedgene import RankedGene as RankedGene
from models.requiredmetadata import RequiredMetadata as RequiredMetadata
from models.softfile import SoftFile as SoftFile
from models.softfilesample import SoftFileSample as SoftFileSample
from models.tag import Tag as Tag
from models.targetapp import TargetApp as TargetApp
from models.targetapplink import TargetAppLink as TargetAppLink
