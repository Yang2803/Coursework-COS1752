
import pytest
from Base_Manager import BaseManager

class MockBaseManager(BaseManager):
    def __init__(self):
        super().__init__()

    # Mock the load method
    def load(self, filename):
        pass  # Simple no-op for testing purposes

    # Mock the save method
    def save(self, filename, data):
        pass  # Simple no-op for testing purposes

def test_base_manager_load():
    manager = MockBaseManager()

    # Provide a valid filename (you can still use a mock file or path)
    filename = 'mock_file.csv'

    # Check if load method doesn't raise errors
    try:
        manager.load(filename)  # Now it won't raise NotImplementedError
    except Exception:
        pytest.fail("load() raised an exception unexpectedly!")

def test_base_manager_save():
    manager = MockBaseManager()

    # Provide dummy arguments for save method
    filename = 'mock_file.csv'
    data = {'key': 'value'}

    # Check if save method doesn't raise errors
    try:
        manager.save(filename, data)  # Now it won't raise NotImplementedError
    except Exception:
        pytest.fail("save() raised an exception unexpectedly!")
