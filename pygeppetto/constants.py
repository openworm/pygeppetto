from enum import Enum, unique

from pyecore.ecore import EPackage


@unique
class GeppettoErrorCodes(Enum):
    """ generated source for enum GeppettoErrorCodes """
    INITIALIZATION = u'INITIALIZATION'
    EXCEPTION = u'EXCEPTION'
    MODEL_INTERPRETER = u'MODEL_INTERPRETER'
    SIMULATOR = u'SIMULATOR'
    SIMULATION = u'SIMULATION'
    GENERIC = u'GENERIC'


@unique
class UserPrivileges(Enum):
    READ_PROJECT = 'READ_PROJECT'
    WRITE_PROJECT = 'WRITE_PROJECT'
    RUN_EXPERIMENT = 'RUN_EXPERIMENT'
    DROPBOX_INTEGRATION = 'DROPBOX_INTEGRATION'
    DOWNLOAD = 'DOWNLOAD'
    ADMIN = 'ADMIN'


@unique
class ExperimentStatus(Enum):
    DESIGN = 'DESIGN'
    QUEUED = 'QUEUED'
    RUNNING = 'RUNNING'
    ERROR = 'ERROR'
    COMPLETED = 'COMPLETED'
    DELETED = 'DELETED'
    CANCELED = 'CANCELED'


@unique
class GeppettoFeature(Enum):
    """ generated source for enum GeppettoFeature """
    SET_PARAMETERS_FEATURE = u'SET_PARAMETERS_FEATURE'
    DEFAULT_VIEW_CUSTOMISER_FEATURE = u'DEFAULT_VIEW_CUSTOMISER_FEATURE'


class GeppettoPackage(EPackage):
    # FIXME GeppettoPackage should be generated by eCore?

    eNAME = "model"
    eNS_URI = "https://raw.githubusercontent.com/openworm/org.geppetto.model/master/src/main/resources/geppettoModel.ecore"

    eNS_URI_TEMPLATE = "https://raw.githubusercontent.com/openworm/org.geppetto.model/$VERSION$/src/main/resources/geppettoModel.ecore"

    eNS_PREFIX = "gep"

    eINSTANCE = None  # TODO no instance of GeppettoPackage yet implemented

    GEPPETTO_MODEL = 0

    GEPPETTO_MODEL__VARIABLES = 0

    GEPPETTO_MODEL__LIBRARIES = 1

    GEPPETTO_MODEL__TAGS = 2

    GEPPETTO_MODEL__ID = 3

    GEPPETTO_MODEL__NAME = 4

    GEPPETTO_MODEL__DATA_SOURCES = 5

    GEPPETTO_MODEL__QUERIES = 6

    GEPPETTO_MODEL_FEATURE_COUNT = 7

    GEPPETTO_MODEL_OPERATION_COUNT = 0

    ISYNCHABLE = 11

    ISYNCHABLE__SYNCHED = 0

    ISYNCHABLE_FEATURE_COUNT = 1

    ISYNCHABLE_OPERATION_COUNT = 0

    NODE = 1

    NODE__SYNCHED = ISYNCHABLE__SYNCHED

    NODE__ID = ISYNCHABLE_FEATURE_COUNT + 0

    NODE__NAME = ISYNCHABLE_FEATURE_COUNT + 1

    NODE__TAGS = ISYNCHABLE_FEATURE_COUNT + 2

    NODE_FEATURE_COUNT = ISYNCHABLE_FEATURE_COUNT + 3

    NODE___GET_PATH = ISYNCHABLE_OPERATION_COUNT + 0

    NODE_OPERATION_COUNT = ISYNCHABLE_OPERATION_COUNT + 1

    GEPPETTO_LIBRARY = 2

    GEPPETTO_LIBRARY__SYNCHED = NODE__SYNCHED

    GEPPETTO_LIBRARY__ID = NODE__ID

    GEPPETTO_LIBRARY__NAME = NODE__NAME

    GEPPETTO_LIBRARY__TAGS = NODE__TAGS

    GEPPETTO_LIBRARY__TYPES = NODE_FEATURE_COUNT + 0

    GEPPETTO_LIBRARY__SHARED_TYPES = NODE_FEATURE_COUNT + 1

    GEPPETTO_LIBRARY_FEATURE_COUNT = NODE_FEATURE_COUNT + 2

    GEPPETTO_LIBRARY___GET_PATH = NODE___GET_PATH

    GEPPETTO_LIBRARY___GET_TYPE_BY_ID = NODE_OPERATION_COUNT + 0

    GEPPETTO_LIBRARY_OPERATION_COUNT = NODE_OPERATION_COUNT + 1

    LIBRARY_MANAGER = 3

    LIBRARY_MANAGER__LIBRARIES = 0

    LIBRARY_MANAGER_FEATURE_COUNT = 1