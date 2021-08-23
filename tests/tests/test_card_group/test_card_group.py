import allure
import pytest

from lib.errors import *
from lib.utils import Fake, get_result
from models.services.card_group import CardGroup

fake = Fake()


@pytest.mark.usefixtures('setup_fixture')
class TestCreation:
    def test_create_card_group_with_all_params(self, clients, delete_cardgroup_from_db):
        with allure.step('Create card group via xgate'):
            cg_model = CardGroup(self.default_client.id, info=fake.name(), parentGroupId=self.default_cardgroup.id)
            response = clients.RPC.card_group.create(model=cg_model)
            created_cg_model = get_result(response, model=CardGroup)
        with allure.step('Assert created card group and card group from response are equal'):
            assert cg_model == created_cg_model
        with allure.step('Get card group info from db'):
            db_cg = clients.DB.card_group.read(created_cg_model.id)
            db_cg_model = CardGroup(id=db_cg.id, name=db_cg.cg_name,
                                    clientId=db_cg.client_id, info=db_cg.cg_info,
                                    parentGroupId=db_cg.cg_parent)
        with allure.step('Assert card groups from db and response are equal'):
            assert cg_model == db_cg_model
            assert created_cg_model.id == db_cg_model.id
        with allure.step('Teardown: '):
            delete_cardgroup_from_db(created_cg_model.id)

    def test_create_card_group_with_mandatory_params(self, clients, delete_cardgroup_from_db):
        with allure.step('Create card group via xgate'):
            new_cg_model = CardGroup(clientId=self.default_client.id)
            response = clients.RPC.card_group.create(model=new_cg_model)
            created_cg_model = get_result(response, model=CardGroup)
        with allure.step('Assert created card group and card group from response are equal'):
            assert new_cg_model == created_cg_model
        with allure.step('Get card group info from db'):
            cg_from_db = clients.DB.card_group.read(created_cg_model.id)
            cg_from_db_model = CardGroup(id=cg_from_db.id, name=cg_from_db.cg_name,
                                         clientId=cg_from_db.client_id, info=cg_from_db.cg_info,
                                         parentGroupId=cg_from_db.cg_parent)
        with allure.step('Assert card groups from db and response are equal'):
            assert new_cg_model == cg_from_db_model
        with allure.step('Assert id of created card group from response and from db are equal'):
            assert created_cg_model.id == cg_from_db_model.id
        with allure.step('Teardown: '):
            delete_cardgroup_from_db(created_cg_model.id)

    def test_unable_to_create_card_group_without_mandatory_param(self, clients):
        with allure.step('Create card group via xgate without clientId parameter'):
            new_cg_model = CardGroup()
            response = clients.RPC.card_group.create(model=new_cg_model)
            response = get_result(response, model=CardGroup)
        with allure.step('Assert error from response is CLIENT_IS_NULL'):
            assert response == CLIENT_IS_NULL

    def test_unable_to_create_card_group_with_nonexistent_client_id(self, clients, nonexistent_client):
        with allure.step('Create card group with invalid clientId value'):
            new_cg_model = CardGroup(nonexistent_client)
            response = clients.RPC.card_group.create(model=new_cg_model)
            response = get_result(response, model=CardGroup)
        with allure.step('Assert response is equal to INTEGRITY_VIOLATION'):
            assert response == CLIENT_DOES_NOT_EXIST

    def test_unable_to_create_card_group_with_existing_name(self, clients):
        with allure.step('Create card group with existing name'):
            new_cg_model = CardGroup(clientId=self.default_client.id, name=self.default_cardgroup.cg_name)
            response = clients.RPC.card_group.create(model=new_cg_model)
            response = get_result(response, model=CardGroup)
        with allure.step('Assert response is equal to ALREADY_EXIST'):
            assert response == CARDGROUP_NAME_ALREADY_EXIST

    def test_unable_to_create_card_group_with_nonexistent_parent_group_id(self, clients, nonexistent_cardgroup):
        with allure.step('Create card group with invalid parentGroupId'):
            new_cg_model = CardGroup(clientId=self.default_client.id, parentGroupId=nonexistent_cardgroup)
            response = clients.RPC.card_group.create(model=new_cg_model)
            response = get_result(response, model=CardGroup)
        with allure.step('Assert response is equal to NOT_FOUND'):
            assert response == NOT_FOUND

    def test_unable_to_create_card_group_with_parent_group_id_of_another_client(self, clients):
        new_client = self.client_generator()
        new_cg_model = CardGroup(clientId=new_client.id, name=fake.name(),
                                 parentGroupId=self.default_cardgroup.id)
        response = clients.RPC.card_group.create(model=new_cg_model)
        response = get_result(response, model=CardGroup)
        assert response == DIFFERENT_CLIENT


@pytest.mark.usefixtures('setup_fixture')
class TestReading:

    def test_read_card_group(self, clients):
        # arrange
        with allure.step('Test setup: create card group'):
            existing_cg = clients.DB.card_group.read(self.default_cardgroup.id)
            existing_cg_model = CardGroup(existing_cg.client_id, existing_cg.cg_name, existing_cg.cg_info,
                                          existing_cg.id, existing_cg.cg_parent)
        # act
        with allure.step('Get card group info via xgate'):
            requested_cg_model = clients.RPC.card_group.read(existing_cg_model.id)
            requested_cg_model = get_result(requested_cg_model, model=CardGroup)
        # assert
        with allure.step('Request data about card group from DB'):
            cg_from_db = clients.DB.card_group.read(existing_cg_model.id)
            cg_from_db_model = CardGroup(id=cg_from_db.id, name=cg_from_db.cg_name,
                                         clientId=cg_from_db.client_id, info=cg_from_db.cg_info,
                                         parentGroupId=cg_from_db.cg_parent)
        with allure.step('Assert data from DB and xgate is equal'):
            assert existing_cg_model == requested_cg_model
            assert requested_cg_model == cg_from_db_model

    def test_unable_to_read_card_group_by_nonexistent_id(self, clients, nonexistent_cardgroup):
        with allure.step('Get card group info via xgate'):
            response = clients.RPC.card_group.read(nonexistent_cardgroup)
            response = get_result(response, model=CardGroup)
        with allure.step('Assert xgate responses with error NOT_FOUND'):
            assert response == NOT_FOUND


@pytest.mark.usefixtures('setup_fixture')
class TestsUpdating:
    def test_update_card_group_with_all_params(self, clients):
        # arrange
        with allure.step('Test setup: create card group'):
            existing_cg = clients.DB.card_group.read(self.default_cardgroup.id)
            print("\n", CardGroup(existing_cg.client_id, existing_cg.cg_name, existing_cg.cg_info,
                                         existing_cg.id, existing_cg.cg_parent))
            updated_cg_model = CardGroup(existing_cg.client_id, fake.name(), fake.name(),
                                         existing_cg.id, existing_cg.cg_parent)
        # act
        with allure.step('Update card group via xgate'):
            clients.RPC.card_group.update(model=updated_cg_model)
        # assert
        with allure.step('Get card group info from db'):
            updated_cg = clients.DB.card_group.read(updated_cg_model.id)
            cg_from_db_model = CardGroup(id=updated_cg_model.id, name=updated_cg.cg_name,
                                         clientId=updated_cg.client_id, info=updated_cg.cg_info,
                                         parentGroupId=updated_cg.cg_parent)
            print(cg_from_db_model)
        with allure.step('Assert card group name and info have been changed'):
            assert cg_from_db_model.name == updated_cg_model.name
            assert cg_from_db_model.info == updated_cg_model.info

    def test_unable_to_update_card_group_with_invalid_client_id(self, clients):
        # arrange
        new_client = self.client_generator()
        with allure.step('Test setup: create card group'):
            existing_cg = clients.DB.card_group.read(self.default_cardgroup.id)
            updated_cg_model = CardGroup(new_client.id, fake.name(), fake.name(),
                                         existing_cg.id, existing_cg.cg_parent)
        # # act
        with allure.step('Update card group via xgate'):
            response = clients.RPC.card_group.update(model=updated_cg_model)
            response = get_result(response, model=CardGroup)
        # assert
        with allure.step('Assert error from response is DIFFERENT_CLIENTS'):
            assert response == DIFFERENT_CLIENTS

    def test_unable_to_update_card_group_with_nonexistent_client_id(self, clients, nonexistent_client):
        # arrange
        with allure.step('Test setup: create card group'):
            existing_cg = clients.DB.card_group.read(self.default_cardgroup.id)
            updated_cg_model = CardGroup(nonexistent_client, fake.name(), fake.name(),
                                         existing_cg.id, existing_cg.cg_parent)
        # act
        with allure.step('Update card group via xgate'):
            response = clients.RPC.card_group.update(model=updated_cg_model)
            response = get_result(response, model=CardGroup)
        # assert
        with allure.step('Assert error from response is DIFFERENT_CLIENTS'):
            assert response == DIFFERENT_CLIENTS

    def test_unable_to_update_nonexistent_card_group(self, clients, nonexistent_cardgroup):
        # arrange
        cg_to_update_model = CardGroup(id=nonexistent_cardgroup,
                                       name=fake.name(),
                                       info=fake.name(),
                                       clientId=self.default_client.id)
        # act
        with allure.step('Update card group via xgate'):
            response = clients.RPC.card_group.update(model=cg_to_update_model)
            response = get_result(response, model=CardGroup)
        # assert
        with allure.step('Assert error from response is NOT_FOUND'):
            assert response == NOT_FOUND


@pytest.mark.usefixtures('setup_fixture')
class TestDelete:

    def test_delete_card_group_by_id(self, clients):
        # arrange
        with allure.step('Test setup: create card group'):
            new_cg_model = CardGroup(clientId=self.default_client.id, info=fake.name())
            cg_to_delete_model = clients.RPC.card_group.create(model=new_cg_model)
            cg_to_delete_model = get_result(cg_to_delete_model, model=CardGroup)
        # act
        with allure.step('Delete card group via xgate'):
            clients.RPC.card_group.delete(cg_to_delete_model.id)
        # assert
        with allure.step('Request data about deleted card group from DB '):
            cg_from_db = clients.DB.card_group.read(cg_to_delete_model.id)
        with allure.step('Assert that there is no data about deleted card group in DB '):
            assert cg_from_db is None

    def test_unable_to_delete_card_group_by_nonexistent_id(self, clients, nonexistent_cardgroup):
        with allure.step('Delete card group via xgate'):
            response = clients.RPC.card_group.delete(nonexistent_cardgroup)
            response = get_result(response, model=CardGroup)
        with allure.step('Assert response is NOT_FOUND '):
            assert response == NOT_FOUND

    def test_unable_to_delete_parent_cardgroup(self, clients, delete_cardgroup_from_db):
        with allure.step('Create cardgroup'):
            new_cg_model = CardGroup(clientId=self.default_client.id, info=fake.name())
            parent_cg_model = clients.RPC.card_group.create(model=new_cg_model)
            parent_cg_model = get_result(parent_cg_model, model=CardGroup)
        with allure.step('Create another cardgroup'):
            new_cg_model = CardGroup(clientId=self.default_client.id,
                                     name=fake.name(),
                                     parentGroupId=parent_cg_model.id)
            cg_model = clients.RPC.card_group.create(model=new_cg_model)
            cg_model = get_result(cg_model, model=CardGroup)
        with allure.step('Delete parent cardgroup'):
            response = clients.RPC.card_group.delete(parent_cg_model.id)
            response = get_result(response, model=CardGroup)
        with allure.step('Assert response is FK_CARDGROUP_PARENT'):
            assert response == FK_CARDGROUP_PARENT
        with allure.step('Teardown: delete created cardgroups'):
            delete_cardgroup_from_db(cg_model.id)
            delete_cardgroup_from_db(parent_cg_model.id)



#from tests.conftest import safe_teardown, for_all_methods
#
# @pytest.mark.usefixtures('setup_fixture')
# @for_all_methods(safe_teardown)
# class TestTearDown:
#     def test_abcd(self, clients, delete_cardgroup_from_db):
#         with allure.step('Create cardgroup'):
#             new_cg_model = CardGroup(clientId=self.default_client.id, info=fake.name())
#             parent_cg_model = clients.RPC.card_group.create(model=new_cg_model)
#             parent_cg_model = get_result(parent_cg_model, model=CardGroup)
#         with allure.step('Create another cardgroup'):
#             new_cg_model = CardGroup(clientId=self.default_client.id,
#                                      name=fake.name(),
#                                      parentGroupId=parent_cg_model.id)
#             cg_model = clients.RPC.card_group.create(model=new_cg_model)
#             cg_model = get_result(cg_model, model=CardGroup)
#         a = 1/0
#         with allure.step('Delete parent cardgroup'):
#             response = clients.RPC.card_group.delete(parent_cg_model.id)
#             response = get_result(response, model=CardGroup)
#         with allure.step('Assert response is FK_CARDGROUP_PARENT'):
#             assert response == FK_CARDGROUP_PARENT
#         with allure.step('Teardown: delete created cardgroups'):
#             delete_cardgroup_from_db(cg_model.id)
#             delete_cardgroup_from_db(parent_cg_model.id)
#
#     def test_abcd2(self, clients):
#         for i in clients.DB.company2role.read(300):
#             print(i)
#         assert 1 == 1
