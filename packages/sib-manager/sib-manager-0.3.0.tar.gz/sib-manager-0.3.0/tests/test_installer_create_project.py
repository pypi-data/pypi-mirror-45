import pytest
from os import path
from sib.installer import Installer

@pytest.fixture
def init_with_fake_modules(tmp_path):
    modules = [('pkg1', 'dist1'), ('pkg2', 'dist2')]
    folder = path.join(tmp_path,'sibtest')
    return Installer('sibproject', folder, modules)

@pytest.fixture
def init_without_modules(tmp_path):
    modules = []
    folder = path.join(tmp_path,'sibtest')
    return Installer('sibproject', folder, modules)

def test_init_project_with_fake_modules(init_with_fake_modules):
    assert init_with_fake_modules.project_name == 'sibproject'
    assert init_with_fake_modules.packages == ['pkg1', 'pkg2']
    assert init_with_fake_modules.dists == ['dist1', 'dist2', 'djangoldp']

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

def test_create_project_with_private_module(tmp_path):
    modules = [('siblab', 'git+https://git.happy-dev.fr/startinblox/devops/siblab-python')]
    folder = path.join(tmp_path, 'sibtest')
    installer = Installer('sibproject', folder, modules)

    installer.create_project(
        site_url='http://localhost:8000',
        allowed_hosts='localhost',
        production=False
    )

    # test to import private test repository
    try:
        import myapp
        assert True
    except ImportError:
        assert False
