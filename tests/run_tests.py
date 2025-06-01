import os
import sys
import pytest

# Ensure the root project directory is in sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT_DIR)

if __name__ == "__main__":
    pytest.main(["-v", "tests"])

# To run the tests simply execute this script:
# python tests/run_tests.py