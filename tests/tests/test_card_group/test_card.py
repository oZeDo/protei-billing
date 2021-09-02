import allure
import pytest
from lib.errors import *
from lib.utils import Fake, get_result
from tests.conftest import safe_teardown, for_all_methods

fake = Fake()


@pytest.mark.usefixtures('setup_fixture')
@for_all_methods(safe_teardown)
class TestTearDown:
    def test_block_card(self, clients):
        pass