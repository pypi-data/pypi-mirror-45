import pytest
from os import path
from sib.installer import Installer

@pytest.fixture
def init_with_modules(tmp_path):
    modules = [('pkg1', 'dist1'), ('pkg2', 'dist2')]
    folder = path.join(tmp_path,'sibtest')
    return Installer('sibproject', folder, modules)

@pytest.fixture
def init_without_modules(tmp_path):
    modules = []
    folder = path.join(tmp_path,'sibtest')
    return Installer('sibproject', folder, modules)

def test_init_project_with_modules(init_with_modules):
    assert init_with_modules.project_name == 'sibproject'
    assert init_with_modules.packages == ['pkg1', 'pkg2']
    assert init_with_modules.dists == ['dist1', 'dist2', 'djangoldp']

def test_init_project_without_modules(init_without_modules):
    assert init_without_modules.project_name == 'sibproject'
    assert init_without_modules.packages == []
    assert init_without_modules.dists == ['djangoldp']

def test_create_project_for_development():

    # make project persistent for load_project testing
    installer = Installer('sibproject', '/tmp/sib-dev', [])

    installer.create_project(
        site_url='http://localhost:8000',
        allowed_hosts='localhost',
        production=False
    )

    # test djangoldp import
    try:
        import djangoldp
        assert True
    except ImportError:
        assert False

    # FIXME: test template
