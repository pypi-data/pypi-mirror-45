import pytest
from sib.installer import Installer

def test_load_project_for_development():

    # load project from previous testing phase
    installer = Installer('sibproject', '/tmp/sib-dev', [])

    assert installer.load_project('test', 'test', 'test@test.io')
