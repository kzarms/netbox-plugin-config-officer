# Test fop conf_manager.py
import pytest
#import os
#import sys

#sys.path.insert(1, os.path.join(sys.path[0], '..'))
#from config_officer.conf_manager import conf_manager

from config_manager import *
#import config_manager

#@pytest.fixture()
#def config():
#    return "Config example"

#@pytest.fixture()
#def section():
#    return "Section example"
#section = "example"

#config = ["yo", "example", "^ yo2"]


testCaseses = [
    ('example', 'Section example', []), # Any values
    ('', '', [])                        # Test empty values
]

# Define tests for first function
@pytest.mark.parametrize('config, section, result', testCaseses)
def test_get_lines_in_section(config, section, result):
    assert get_lines_in_section(config, section) == result
