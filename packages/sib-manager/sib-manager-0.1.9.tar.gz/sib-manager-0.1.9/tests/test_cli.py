import pytest
import click
from click.testing import CliRunner
from os import path
from sib.cli import main as cli


"""Test the process of project creation"""

def test_startproject_by_folder(tmp_path):

    result = CliRunner().invoke(cli, ['startproject', 'sibtest', path.join(tmp_path, 'sibtest')])
    assert result.exit_code == 0
