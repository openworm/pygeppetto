import pytest
from pygeppetto.model import GeppettoModel, GeppettoLibrary, Tag


def test_create_pygeppetto_model():
    root = GeppettoModel()
    assert root.name is None


def test_create_pygeppetto_model_name():
    root = GeppettoModel(name='model1')
    assert root.name == 'model1'


def test_create_pygeppetto_readme_test():
    flib = GeppettoLibrary(name='mylib')
    root = GeppettoModel(name='MyGeppettoModel', libraries=[flib])
    assert flib in root.libraries
    assert flib.name == 'mylib'
    assert root.name == 'MyGeppettoModel'


def test_create_pygeppetto_model_tag():
    tag = Tag()
    model = GeppettoModel()
    model.tags.append(tag)
    assert tag in model.tags
