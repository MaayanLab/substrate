"""Configures substrate's API.
"""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

from models.customdataset import CustomDataset
from models.dataset import Dataset
from models.gene import Gene
from models.genelist import GeneList
from models.genesignature import GeneSignature
from models.geodataset import GeoDataset
from models.optionalmetadata import OptionalMetadata
from models.pcavisualization import PCAVisualization
from models.rankedgene import RankedGene
from models.requiredmetadata import RequiredMetadata
from models.report import Report
from models.softfile import SoftFile
from models.softfilesample import SoftFileSample
from models.tag import Tag as Tag
from models.targetapp import TargetApp
from models.targetapplink import TargetAppLink
