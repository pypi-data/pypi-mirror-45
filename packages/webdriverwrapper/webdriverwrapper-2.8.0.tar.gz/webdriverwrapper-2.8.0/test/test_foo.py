import pytest
from webdriverwrapper import Chrome
from pyvirtualdisplay import Display



@pytest.yield_fixture(scope='session', autouse=True)
def display():
    d = Display(visible=0, size=(1280, 700))
    d.start()
    yield
    d.stop()


@pytest.fixture
def _driver():
    d = Chrome()
    d.go_to("https://seznam.cz")
    return d


@pytest.fixture
def foo(driver):
    1/0


def test_foo(driver, foo):
    driver.go_to("https://google.com")
