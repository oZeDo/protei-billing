import allure
import pytest
from lib.errors import *
from lib.utils import Fake, get_result
from models.services.card_group import CardGroup
from tests.conftest import safe_teardown, for_all_methods

fake = Fake()


@pytest.mark.usefixtures('setup_fixture')
@for_all_methods(safe_teardown)  # Применить декоратор ко всем тестам в классе
class TestTearDown:
    # Применить декоратор к тесту
    # @safe_teardown
    def test_abcd(self, clients, delete_cardgroup_from_db):
        # В тесте заменить апишки на свои
        with allure.step('Create cardgroup'):
            new_cg_model = CardGroup(clientId=self.default_client.id, info=fake.name())
            parent_cg_model = clients.RPC.card_group.create(model=new_cg_model)
            parent_cg_model = get_result(parent_cg_model, model=CardGroup)
        with allure.step('Create another cardgroup'):
            new_cg_model = CardGroup(clientId=self.default_client.id,
                                     name=fake.name(),
                                     parentGroupId=parent_cg_model.id)
            cg_model = clients.RPC.card_group.create(model=new_cg_model) #
            cg_model = get_result(cg_model, model=CardGroup)
        a = 1/0
        with allure.step('Delete parent cardgroup'):
            response = clients.RPC.card_group.delete(parent_cg_model.id)
            response = get_result(response, model=CardGroup)
        with allure.step('Assert response is FK_CARDGROUP_PARENT'):
            assert response == FK_CARDGROUP_PARENT
        with allure.step('Teardown: delete created cardgroups'):
            delete_cardgroup_from_db(cg_model.id) #
            delete_cardgroup_from_db(parent_cg_model.id) #
