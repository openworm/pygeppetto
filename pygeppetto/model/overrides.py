from pyecore.ecore import EAttribute, EDouble
from pygeppetto.model import Type, TimeSeries, Pointer, GeppettoModel, Node, Value


# Implement Type.extends_type
def extends_type(self, type):
    return isinstance(self, type.__class__)


Type.extends_type = extends_type

# Fix timeSeries unique attributes check
from pyecore.valuecontainer import EList, EOrderedSet
from pyecore.notification import Notification, Kind


def no_check_eattribute_extend(self, sublist):
    super(EList, self).extend(sublist)
    self.owner.notify(Notification(new=sublist,
                                   feature=self.feature,
                                   kind=Kind.ADD_MANY))
    self.owner._isset.add(self.feature)


TimeSeries.value = value = EAttribute(name='value', eType=EDouble, derived=False, changeable=True, upper=-1,
                                      unique=False)

EList.no_check_eattribute_extend = no_check_eattribute_extend

default_timeseries_init = TimeSeries.__init__


def timeseries_init(self, unit=None, scalingFactor=None, value=None, **kwargs):
    default_timeseries_init(self, unit=unit, scalingFactor=scalingFactor, **kwargs)
    if value:
        self.value.no_check_eattribute_extend(value)


TimeSeries.__init__ = timeseries_init


# Implement method Pointer.get_instance_path
def get_instance_path(self):
    """ generated source for method getInstancePath """
    instance_path = []
    for i, element in enumerate(self.elements):
        instance_path.append(element.variable.id)
        instance_path.append("(" + element.type.id + ")")
        if element.index is not None and element.index > -1:
            instance_path.append("[{0}]".format(element.index))
        if i != len(self.elements) - 1:
            instance_path.append(".")
    return ''.join(instance_path)


Pointer.get_instance_path = Pointer.getInstancePath = get_instance_path


# Implement method Node.getPath
def getPath(self):
    if not (isinstance(self.eContainer(), GeppettoModel)) and isinstance(self.eContainer(), Node):
        container = self.eContainer()
        from pygeppetto.model import Variable  # Must import locally, circular reference otherwise
        if container.eContainer().__class__ == Variable:
            container = container.eContainer()
        return container.getPath() + "." + self.id
    else:
        return self.id


Node.getPath = Node.get_path = getPath
