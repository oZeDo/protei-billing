import allure
import pytest
from lib.errors import *
from lib.utils import Fake, get_result
from models.services.card import BaseCard

fake = Fake()

# !TODO: Заблокировать заблокированную, разблокировать разблокированную, комбо бан, комбо разбан


@pytest.mark.usefixtures('setup_fixture')
class TestBlockSimCard:
    def test_block_sim_card_with_correct_msisdn(self, clients):
        with allure.step('Test setup: create base card'):
            existing_bc = clients.DB.base_card.read(self.default_base_card.id)
            existing_c = clients.DB.card.read(self.default_card.id)
            assert existing_bc.id == existing_c.cardid
            existing_bc_model = BaseCard(id=existing_bc.id, cardtype=existing_bc.cardtype,
                                         vgroupid=existing_bc.vgroupid, accfileid=existing_bc.vgroupid,
                                         state=existing_bc.state, cardnumber=existing_bc.cardnumber)
        with allure.step('Block card group via xgate'):
            response = clients.RPC.card.block_sim_card(existing_c.msisdn)
            response = get_result(response, model=BaseCard)
            updated_bc = clients.DB.base_card.read(existing_c.cardid)
            updated_bc_model = BaseCard(id=updated_bc.id, cardtype=updated_bc.cardtype, vgroupid=updated_bc.vgroupid,
                                        accfileid=updated_bc.vgroupid, state=updated_bc.state,
                                        cardnumber=updated_bc.cardnumber)
        with allure.step('Assert base card state changed to 1(admin blocked)'):
            assert existing_bc_model != updated_bc_model
            assert updated_bc_model.state == 1

    def test_unable_to_block_sim_card_with_incorrect_msisdn(self, clients):
        with allure.step('Test setup: create base card'):
            existing_bc = clients.DB.base_card.read(self.default_base_card.id)
            existing_c = clients.DB.card.read(self.default_card.id)
            existing_bc_model = BaseCard(id=existing_bc.id, cardtype=existing_bc.cardtype,
                                         vgroupid=existing_bc.vgroupid, accfileid=existing_bc.vgroupid,
                                         state=existing_bc.state, cardnumber=existing_bc.cardnumber)
        with allure.step('Assert id of existing card matches its base card card_id'):
            assert existing_bc_model.id == existing_c.cardid
        with allure.step('Block card group via xgate'):
            response = clients.RPC.card.block_sim_card(msisdn=True)
            response = get_result(response, model=BaseCard)
        with allure.step('Assert response is equal to NOT_FOUND'):
            assert response == NOT_FOUND

    def test_unable_to_block_sim_card_with_empty_msisdn(self, clients):
        with allure.step('Test setup: create base card'):
            existing_bc = clients.DB.base_card.read(self.default_base_card.id)
            existing_c = clients.DB.card.read(self.default_card.id)
            existing_bc_model = BaseCard(id=existing_bc.id, cardtype=existing_bc.cardtype,
                                         vgroupid=existing_bc.vgroupid, accfileid=existing_bc.vgroupid,
                                         state=existing_bc.state, cardnumber=existing_bc.cardnumber)
        with allure.step('Assert id of existing card matches its base card card_id'):
            assert existing_bc_model.id == existing_c.cardid
        with allure.step('Block card group via xgate'):
            response = clients.RPC.card.block_sim_card(msisdn=None)
            response = get_result(response, model=BaseCard)
        print(response)
        # with allure.step('Assert response is equal to NOT_FOUND'):
        #     assert response == NOT_FOUND


@pytest.mark.usefixtures('setup_fixture')
class TestSelfBlockSimCard:
    def test_self_block_sim_card_with_correct_msisdn_and_imsi(self, clients):
        with allure.step('Test setup: create base card'):
            existing_bc = clients.DB.base_card.read(self.default_base_card.id)
            existing_c = clients.DB.card.read(self.default_card.id)
            assert existing_bc.id == existing_c.cardid
            existing_bc_model = BaseCard(id=existing_bc.id, cardtype=existing_bc.cardtype,
                                         vgroupid=existing_bc.vgroupid, accfileid=existing_bc.vgroupid,
                                         state=existing_bc.state, cardnumber=existing_bc.cardnumber)
        with allure.step('Block card group via xgate'):
            response = clients.RPC.card.self_block_sim_card(msisdn=existing_c.msisdn, imsi=existing_c.imsi)
            response = get_result(response, model=BaseCard)  # not necessary
            updated_bc = clients.DB.base_card.read(existing_c.cardid)
            updated_bc_model = BaseCard(id=updated_bc.id, cardtype=updated_bc.cardtype, vgroupid=updated_bc.vgroupid,
                                        accfileid=updated_bc.vgroupid, state=updated_bc.state,
                                        cardnumber=updated_bc.cardnumber)
        with allure.step('Assert base card state changed to 3(user blocked)'):
            assert existing_bc_model != updated_bc_model
            assert updated_bc_model.state == 3

    def test_unable_to_self_block_sim_card_with_incorrect_msisdn_but_correct_imsi(self, clients):
        with allure.step('Test setup: create base card'):
            existing_bc = clients.DB.base_card.read(self.default_base_card.id)
            existing_c = clients.DB.card.read(self.default_card.id)
            existing_bc_model = BaseCard(id=existing_bc.id, cardtype=existing_bc.cardtype,
                                         vgroupid=existing_bc.vgroupid, accfileid=existing_bc.vgroupid,
                                         state=existing_bc.state, cardnumber=existing_bc.cardnumber)
        with allure.step('Assert id of existing card matches its base card card_id'):
            assert existing_bc_model.id == existing_c.cardid
        with allure.step('Block card group via xgate'):
            response = clients.RPC.card.self_block_sim_card(msisdn=True, imsi=existing_c.imsi)
            response = get_result(response, model=BaseCard)
        with allure.step('Assert response is equal to NOT_FOUND'):
            assert response == NOT_FOUND

    def test_unable_to_self_block_sim_card_with_correct_msisdn_but_incorrect_imsi(self, clients):
        with allure.step('Test setup: create base card'):
            existing_bc = clients.DB.base_card.read(self.default_base_card.id)
            existing_c = clients.DB.card.read(self.default_card.id)
            existing_bc_model = BaseCard(id=existing_bc.id, cardtype=existing_bc.cardtype,
                                         vgroupid=existing_bc.vgroupid, accfileid=existing_bc.vgroupid,
                                         state=existing_bc.state, cardnumber=existing_bc.cardnumber)
        with allure.step('Assert id of existing card matches its base card card_id'):
            assert existing_bc_model.id == existing_c.cardid
        with allure.step('Block card group via xgate'):
            response = clients.RPC.card.self_block_sim_card(imsi=True, msisdn=existing_c.msisdn)
            response = get_result(response, model=BaseCard)
        with allure.step('Assert response is equal to NOT_FOUND'):
            assert response == NOT_FOUND

    def test_unable_to_self_block_sim_card_with_correct_msisdn_and_imsi_from_another_card(self, clients):
        with allure.step('Test setup: create base card'):
            existing_bc = clients.DB.base_card.read(self.default_base_card.id)
            existing_c = clients.DB.card.read(self.default_card.id)
            existing_bc_model = BaseCard(id=existing_bc.id, cardtype=existing_bc.cardtype,
                                         vgroupid=existing_bc.vgroupid, accfileid=existing_bc.vgroupid,
                                         state=existing_bc.state, cardnumber=existing_bc.cardnumber)
        with allure.step('Assert id of existing card matches its base card card_id'):
            assert existing_bc_model.id == existing_c.cardid
        with allure.step('Block card group via xgate'):
            response = clients.RPC.card.self_block_sim_card(imsi=True, msisdn=existing_c.msisdn)
            response = get_result(response, model=BaseCard)
        with allure.step('Assert response is equal to NOT_FOUND'):
            assert response == NOT_FOUND

    def test_unable_to_self_block_sim_card_with_empty_msisdn_and_imsi(self, clients):
        with allure.step('Test setup: create base card'):
            existing_bc = clients.DB.base_card.read(self.default_base_card.id)
            existing_c = clients.DB.card.read(self.default_card.id)
            existing_bc_model = BaseCard(id=existing_bc.id, cardtype=existing_bc.cardtype,
                                         vgroupid=existing_bc.vgroupid, accfileid=existing_bc.vgroupid,
                                         state=existing_bc.state, cardnumber=existing_bc.cardnumber)
        with allure.step('Assert id of existing card matches its base card card_id'):
            assert existing_bc_model.id == existing_c.cardid
        with allure.step('Block card group via xgate'):
            response = clients.RPC.card.self_block_sim_card(None, None)
            response = get_result(response, model=BaseCard)
        print(response)
        # with allure.step('Assert response is equal to NOT_FOUND'):
        #     assert response == NOT_FOUND


@pytest.mark.usefixtures('setup_fixture')
class TestUnblockSimCard:
    def test_unblock_sim_card_with_correct_msisdn(self, clients):
        with allure.step('Test setup: create base card and card'):
            new_bc = self.base_card_generator(virtual_group_id=self.default_virtual_group.id,
                                              accounting_file_id=self.default_accounting_file.id, state=1)
            new_c = self.card_generator(account_id=self.default_account.id, base_card_id=new_bc.id)
        with allure.step('Assert id of existing card matches its base card card_id'):
            assert new_bc.id == new_c.cardid
        with allure.step('Unblock card group via xgate'):
            response = clients.RPC.card.unblock_sim_card(new_c.msisdn)
            response = get_result(response, model=BaseCard)
            updated_bc = clients.DB.base_card.read(new_bc.cardid)
            updated_bc_model = BaseCard(id=updated_bc.id, cardtype=updated_bc.cardtype, vgroupid=updated_bc.vgroupid,
                                        accfileid=updated_bc.vgroupid, state=updated_bc.state,
                                        cardnumber=updated_bc.cardnumber)
        with allure.step('Assert base card state changed to 1(admin blocked)'):
            assert new_bc != updated_bc_model
            assert updated_bc_model.state == 2

    def test_unable_to_unblock_sim_card_with_incorrect_msisdn(self, clients):
        with allure.step('Test setup: create base card and card'):
            new_bc = self.base_card_generator(virtual_group_id=self.default_virtual_group.id,
                                              accounting_file_id=self.default_accounting_file.id, state=1)
            new_c = self.card_generator(account_id=self.default_account.id, base_card_id=new_bc.id)
        with allure.step('Assert id of existing card matches its base card card_id'):
            assert new_bc.id == new_c.cardid
        with allure.step('Unblock card group via xgate'):
            response = clients.RPC.card.unblock_sim_card(msisdn=True)
            response = get_result(response, model=BaseCard)
        with allure.step('Assert response is equal to NOT_FOUND'):
            assert response == NOT_FOUND

    def test_unable_to_unblock_sim_card_with_empty_msisdn(self, clients):
        with allure.step('Test setup: create base card and card'):
            new_bc = self.base_card_generator(virtual_group_id=self.default_virtual_group.id,
                                              accounting_file_id=self.default_accounting_file.id, state=1)
            new_c = self.card_generator(account_id=self.default_account.id, base_card_id=new_bc.id)
        with allure.step('Assert id of existing card matches its base card card_id'):
            assert new_bc.id == new_c.cardid
        with allure.step('Unblock card group via xgate'):
            response = clients.RPC.card.unblock_sim_card(msisdn=None)
            response = get_result(response, model=BaseCard)
        print(response)
        # with allure.step('Assert response is equal to NOT_FOUND'):
        #     assert response == NOT_FOUND


@pytest.mark.usefixtures('setup_fixture')
class TestSelfUnblockSimCard:
    def test_self_unblock_sim_card_with_correct_msisdn_and_imsi(self, clients):
        with allure.step('Test setup: create base card and card'):
            new_bc = self.base_card_generator(virtual_group_id=self.default_virtual_group.id,
                                              accounting_file_id=self.default_accounting_file.id, state=3)
            new_c = self.card_generator(account_id=self.default_account.id, base_card_id=new_bc.id)
        with allure.step('Assert id of existing card matches its base card card_id'):
            assert new_bc.id == new_c.cardid
        with allure.step('Unblock card group via xgate'):
            response = clients.RPC.card.unblock_self_blocked_sim_card(msisdn=new_c.msisdn, imsi=new_c.imsi)
            response = get_result(response, model=BaseCard)  # not necessary
            updated_bc = clients.DB.base_card.read(new_c.cardid)
            updated_bc_model = BaseCard(id=updated_bc.id, cardtype=updated_bc.cardtype, vgroupid=updated_bc.vgroupid,
                                        accfileid=updated_bc.vgroupid, state=updated_bc.state,
                                        cardnumber=updated_bc.cardnumber)
        with allure.step('Assert base card state changed to 3(user blocked)'):
            assert new_bc != updated_bc_model
            assert updated_bc_model.state == 2

    def test_unable_to_self_unblock_sim_card_with_incorrect_msisdn_but_correct_imsi(self, clients):
        with allure.step('Test setup: create base card and card'):
            new_bc = self.base_card_generator(virtual_group_id=self.default_virtual_group.id,
                                              accounting_file_id=self.default_accounting_file.id, state=3)
            new_c = self.card_generator(account_id=self.default_account.id, base_card_id=new_bc.id)
        with allure.step('Assert id of existing card matches its base card card_id'):
            assert new_bc.id == new_c.cardid
        with allure.step('Block card group via xgate'):
            response = clients.RPC.card.unblock_self_blocked_sim_card(msisdn=True, imsi=new_c.imsi)
            response = get_result(response, model=BaseCard)
        with allure.step('Assert response is equal to NOT_FOUND'):
            assert response == NOT_FOUND

    def test_unable_to_self_unblock_sim_card_with_correct_msisdn_but_incorrect_imsi(self, clients):
        with allure.step('Test setup: create base card and card'):
            new_bc = self.base_card_generator(virtual_group_id=self.default_virtual_group.id,
                                              accounting_file_id=self.default_accounting_file.id, state=1)
            new_c = self.card_generator(account_id=self.default_account.id, base_card_id=new_bc.id)
        with allure.step('Assert id of existing card matches its base card card_id'):
            assert new_bc.id == new_c.cardid
        with allure.step('Block card group via xgate'):
            response = clients.RPC.card.unblock_self_blocked_sim_card(imsi=True, msisdn=new_c.msisdn)
            response = get_result(response, model=BaseCard)
        with allure.step('Assert response is equal to NOT_FOUND'):
            assert response == NOT_FOUND

    def test_unable_to_self_unblock_sim_card_with_correct_msisdn_and_imsi_from_another_card(self, clients):
        with allure.step('Test setup: create base card and card'):
            new_bc = self.base_card_generator(virtual_group_id=self.default_virtual_group.id,
                                              accounting_file_id=self.default_accounting_file.id, state=1)
            new_c = self.card_generator(account_id=self.default_account.id, base_card_id=new_bc.id)
        with allure.step('Assert id of existing card matches its base card card_id'):
            assert new_bc.id == new_c.cardid
        with allure.step('Block card group via xgate'):
            response = clients.RPC.card.unblock_self_blocked_sim_card(imsi=True, msisdn=self.default_card.msisdn)
            response = get_result(response, model=BaseCard)
        with allure.step('Assert response is equal to NOT_FOUND'):
            assert response == NOT_FOUND

    def test_unable_to_self_unblock_sim_card_with_empty_msisdn_and_imsi(self, clients):
        with allure.step('Test setup: create base card and card'):
            new_bc = self.base_card_generator(virtual_group_id=self.default_virtual_group.id,
                                              accounting_file_id=self.default_accounting_file.id, state=1)
            new_c = self.card_generator(account_id=self.default_account.id, base_card_id=new_bc.id)
        with allure.step('Assert id of existing card matches its base card card_id'):
            assert new_bc.id == new_c.cardid
        with allure.step('Block card group via xgate'):
            response = clients.RPC.card.unblock_self_blocked_sim_card(None, None)
            response = get_result(response, model=BaseCard)
        print(response)
        # with allure.step('Assert response is equal to NOT_FOUND'):
        #     assert response == NOT_FOUND
