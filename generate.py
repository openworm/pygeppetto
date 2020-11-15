from pyecore.resources import ResourceSet
from pyecoregen.ecore import EcoreGenerator
import os
import pyecore.type  # Required by geppettoModel.ecore


def package_qualname(eobject, prefix=''):
    if eobject is pyecore.type.eClass:
        return "pyecore.type"
    def collect_packages(element, packages):
            parent = element.eContainer()
            if parent:
                collect_packages(parent, packages)
            packages.append(element.name)

    packages = []
    collect_packages(eobject, packages)

    return "{}.{}".format(prefix, '.'.join(packages))


class GeppettoGenerator(EcoreGenerator):
    templates_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'generator-templates'
        )

    def create_environment(self, **kwargs):
        environment = super().create_environment(**kwargs)
        environment.filters.update({
            'packagequalname': package_qualname,
        })
        return environment



# We open the metamodel
rset = ResourceSet()
mm_root = rset.get_resource('pygeppetto/ecore/geppettoModel.ecore').contents[0]

# We generate the code using the EcoreGenerator
generator = GeppettoGenerator(auto_register_package=True)

generator.generate(mm_root, outfolder='new_metamodel')
