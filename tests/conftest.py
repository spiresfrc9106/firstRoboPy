import pytest
from utils.singleton import destroyAllSingletonInstances
from utils.singleton import noSingletonsAround

@pytest.fixture(scope="function", autouse=True)
def my_fixture(): # pylint: disable=invalid-name
    noSingletonsAround()
    yield
    destroyAllSingletonInstances()
