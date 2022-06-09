import pytest

import os

@pytest.fixture
def api_key():
    return os.environ["REBRANDLY_KEY"]