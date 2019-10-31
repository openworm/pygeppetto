import os

import pytest

from pyecore.resources import ResourceSet, URI

HERE = os.path.dirname(os.path.abspath(__file__))

@pytest.fixture
def rset():
    return ResourceSet()


def filepath(filename):
    return os.path.join(HERE, 'xmi-data', filename)




def test_read_mediumXMI(rset):
    resource = rset.get_resource(URI(filepath('MediumNet.net.nml.xmi')))
    root = resource.contents[0]
    assert root  # The root exists

@pytest.mark.skip('Too slow')
def test_read_BigXMI(rset):
    resource = rset.get_resource(URI(filepath('BigCA1.net.nml.xmi')))
    root = resource.contents[0]
    assert root  # The root exists

@pytest.mark.skip('Too slow')
def test_read_LargeXMI(rset):
    resource = rset.get_resource(URI(filepath('LargeConns.net.nml.xmi')))
    root = resource.contents[0]
    assert root  # The root exists


def test_readwrite_mediumXMI(tmpdir, rset):
    resource = rset.get_resource(URI(filepath('MediumNet.net.nml.xmi')))
    root = resource.contents[0]
    f = tmpdir.mkdir('pyecore-tmp').join('medium.xmi')
    resource.save(output=URI(str(f)))

@pytest.mark.skip('Too slow')
def test_readwrite_BigXMI(tmpdir, rset):
    resource = rset.get_resource(URI(filepath('BigCA1.net.nml.xmi')))
    root = resource.contents[0]
    f = tmpdir.mkdir('pyecore-tmp').join('big.xmi')
    resource.save(output=URI(str(f)))

@pytest.mark.skip('Too slow')
def test_readwrite_LargeXMI(tmpdir, rset):
    resource = rset.get_resource(URI(filepath('LargeConns.net.nml.xmi')))
    root = resource.contents[0]
    f = tmpdir.mkdir('pyecore-tmp').join('large.xmi')
    resource.save(output=URI(str(f)))


def test_roundtrip_mediumXMI(tmpdir, rset):
    resource = rset.get_resource(URI(filepath('MediumNet.net.nml.xmi')))
    root = resource.contents[0]

    # We change the root name
    root.name = 'mediumTestModel'

    # We serialize the modifications
    f = tmpdir.mkdir('pyecore-tmp').join('medium.xmi')
    resource.save(output=URI(str(f)))

    # We read again the file
    resource = rset.get_resource(URI(str(f)))
    root = resource.contents[0]
    assert root
    assert root.name == 'mediumTestModel'

@pytest.mark.skip('Too slow')
def test_roundtrip_BigXMI(tmpdir, rset):
    resource = rset.get_resource(URI(filepath('BigCA1.net.nml.xmi')))
    root = resource.contents[0]

    # We change the root name
    root.name = 'bigTestModel'

    # We serialize the modifications
    f = tmpdir.mkdir('pyecore-tmp').join('big.xmi')
    resource.save(output=URI(str(f)))

    # We read again the file
    resource = rset.get_resource(URI(str(f)))
    root = resource.contents[0]
    assert root
    assert root.name == 'bigTestModel'

@pytest.mark.skip('Too slow')
def test_roundtrip_LargeXMI(tmpdir, rset):
    resource = rset.get_resource(URI(filepath('LargeConns.net.nml.xmi')))
    root = resource.contents[0]

    # We change the root name
    root.name = 'largeTestModel'

    # We serialize the modifications
    f = tmpdir.mkdir('pyecore-tmp').join('large.xmi')
    resource.save(output=URI(str(f)))

    # We read again the file
    resource = rset.get_resource(URI(str(f)))
    root = resource.contents[0]
    assert root
    assert root.name == 'largeTestModel'
