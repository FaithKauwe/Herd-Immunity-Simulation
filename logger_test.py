import pytest
import os
from logger import Logger

@pytest.fixture
def setup_logger():
    logger = Logger('test_log.txt')
    yield logger  # This will run before each test and provide a hook for cleanup
    os.remove('test_log.txt')  # Cleanup after each test

def test_write_metadata(setup_logger):
    logger = setup_logger
    logger.write_metadata(1000, 0.9, "Ebola", 0.7, 0.25)
    
    with open('test_log.txt', 'r') as f:
        content = f.read()
    
    assert "Population Size: 1000" in content  # Check that the expected content is in the log

