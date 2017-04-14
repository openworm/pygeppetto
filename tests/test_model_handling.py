import pytest
import model as pygeppetto


def test_create_pygeppetto_model():
    root = pygeppetto.GeppettoModel()
    assert root.name is None


def test_create_pygeppetto_model_name():
    root = pygeppetto.GeppettoModel(name='model1')
    assert root.name == 'model1'


def test_create_pygeppetto_readme_test():
    flib = pygeppetto.GeppettoLibrary(name='mylib')
    root = pygeppetto.GeppettoModel(name='MyGeppettoModel', libraries=[flib])
    assert flib in root.libraries
    assert flib.name == 'mylib'
    assert root.name == 'MyGeppettoModel'
