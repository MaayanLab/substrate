"""Configures substrate's API.
"""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

from models.biocategory import BioCategory
from models.curator import Curator
from models.customdataset import CustomDataset
from models.dataset import Dataset
from models.gene import Gene
from models.genelist import GeneList
from models.genesignature import GeneSignature
from models.geodataset import GeoDataset
from models.heatmap import HeatMap
from models.optionalmetadata import OptionalMetadata
from models.pcaplot import PCAPlot
from models.rankedgene import RankedGene
from models.requiredmetadata import RequiredMetadata
from models.report import Report
from models.resource import Resource
from models.softfile import SoftFile
from models.softfilesample import SoftFileSample
from models.tag import Tag as Tag
from models.targetapp import TargetApp
from models.targetapplink import TargetAppLink
from models.user import User
