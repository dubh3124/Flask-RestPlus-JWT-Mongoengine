import pytest
from .. import create_app
from ..script import PopulateDB, ResetDB


@pytest.fixture
def client():
    testapp = create_app(config_name="testing")
    client = testapp.test_client()
    ResetDB().drop_collections()
    PopulateDB().pop

    ctx = testapp.app_context()
    ctx.push()
    yield client
    ctx.pop()
