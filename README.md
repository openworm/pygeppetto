# pygeppetto

Home of the Geeppetto Python API.
The API allows to create a Geppetto Model from Python.

## Installation

Until pygeppetto is still in development, it is highly recommended to use a
virtualenv in order to deploy it. Once you have a dedicated virtualenv, you can
simply install pygeppetto:

```bash
$ python setup.py install
```

## Pygeppetto API Basic Usage

First, import the pygeppetto API:

```Python
import pygeppetto
```

This will load the pygeppetto API and name it `pygeppetto`. Then, you can create
instances and handle them:

```Python
# We create a new lib
flib = pygeppetto.GeppettoLibrary(name='mylib')
# We create a GeppettoModel instance and we set a name a assign a lib
root = pygeppetto.GeppettoModel(name='MyGeppettoModel', libraries=[flib])
```

The pygeppetto API also allows you to set all attributes in a "classical"
fashion:

```Python
root = pygeppetto.GeppettoModel()  # We create a GeppettoModel instance
root.name = 'MyGeppettoModel'  # We set a name
flib = pygeppetto.GeppettoLibrary()  # We create a new lib
flib.name = 'mylib'
root.libraries.append(flib)  # We add the new lib to the created root
```

If you wan to open an existing XMI, you need to use a ``ResourceSet`` (not
required, but prefered).

```Python
# We import the class that will be used to read the XMI from PyEcore
from pyecore.resources import ResourceSet, URI

# We create a new resource set (not required, but better)
rset = ResourceSet()
```

Using this ``ResourceSet``, we are able to read the Geppetto XMI:

```Python
model_url = URI('tests/xmi-data/MediumNet.net.nml.xmi')  # The model URI
resource = rset.get_resource(model_url)  # We load the model
geppettomodel = resource.contents[0]  # We get the root
```

At the end of this script, `geppettomodel` contains the model root.

In order to serialize a new version of the modified model, there is two options.
The first one is to serialize onto the existing resource (_i.e_: in the same
file), or to serialize in a new one:

```Python
# Using the first option
resource.save()

# Using the second option
resource.save(output=URI('my_new_file.xmi'))
```

## Dependencies

*  Python >= 3.5
* `pyecore`

## Contributions

If the `geppettoModel.ecore` evolves, the static metamodel must be regenerated.
The process of adding a new version is the following:

1. Copy the of the new `geppettoModel.ecore` inside `ecore/` (in order to keep a
version from which the static metamodel is generated).
1. Generate the new version of the static metamodel.
1. Manually merge modifications between the current and the new version (if
there is manual modifications in the current version).
1. Run the tests


### How to Generate a New Version

The pygeppetto API is generated from the
[`geppettoModel.ecore`](https://github.com/openworm/org.geppetto.model/blob/development/src/main/resources/geppettoModel.ecore)
using the PyEcore Acceleo generator
([`ecore2pyecore.mtl`](https://github.com/pyecore/pyecore/blob/master/generator/ecore2pyecore.mtl)).
The `.ecore` is a copy of the `geppettoModel.ecore` from
[org.geppetto.model](https://github.com/openworm/org.geppetto.model/blob/development/src/main/resources/geppettoModel.ecore)
(`development` branch). 

#### Generate the code with pyecoregen (suggested)

Install pyecoregen
```bash
pip install pyecoregen
```

Run the following script:

```python
from pyecore.resources import ResourceSet
from pyecoregen.ecore import EcoreGenerator
import pyecore.type  # We register the XML types (generated by pyecoregen)

# We open the metamodel
rset = ResourceSet()
mm_root = rset.get_resource('pygeppetto/ecore/geppettoModel.ecore').contents[0]

# We generate the code using the EcoreGenerator
EcoreGenerator(auto_register_package=True).generate(mm_root, outfolder='pygeppetto')
```

Then do the following fix replacements: 
* `from model` -> `from pygeppetto.model`
* `from type`  -> `from pyecore.type`

#### Generate the code with Eclipse
The `ecore2pyecore.mtl` script can be directly used in Eclipse as a 
[Acceleo](https://wiki.eclipse.org/Acceleo/Getting_Started) generator.
1. Install the [Acceleo plugin](https://marketplace.eclipse.org/content/acceleo) into eclipse
1. Create a new Acceleo project
1. Add the file `ecore2pyecore.mtl` to the project main package
1. run `ecore2pyecore.mtl` as an acceleo project. The run configuration will popup: specify the `geppettoModel.ecore` 
file to use and the generation path. Generate the code in a path different from pygeppetto and merge the code

#### Patches and Overrides
The model generated from the ecore file contains some code stubs that are implemented manually on Python.
The place to make those implementations is not the files themselves though but the `overrides.py` file.
Writing the overrides there keeps the regeneration process easier as the written code does not actually
need to be merged.

#### Merge conflicts
Manual modifications may have been introduced in the version of the static
Geppetto metamodel (_e.g_: implementation of some methods or technical method
additions). The generated version must be manually merged with the new generated one
(_e.g_: using meld or other tool).

An easy way to do that is by using git.

1 - Generate the code in a in a directory reproducing the pygeppetto structure, say `pygeppetto_new/pygeppetto/model`

2 - Initialize a new git local repo inside our new pygeppetto
```bash
cd pygeppetto_new
git init
```
3 - Add the remote for pygeppetto
```bash
git remote add origin https://github.com/openworm/pygeppetto.git
```
4 - Merge with actual geppetto branch
```bash
git merge --allow-unrelated-histories origin/development
```
5 - Resolve conflicts: use incoming changes for clear overrides and implemented methods



### Run the Tests

Tests are written using `pytest` and are run using `tox`. To launch all the
tests the following command is enough:

```bash
$ tox
```

Or, if you want to avoid using `tox`, you can just:

```bash
$ python -m pytest tests/
```

