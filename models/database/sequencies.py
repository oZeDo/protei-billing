from sqlalchemy import Sequence

# Client
client_id_seq = Sequence('S_CLIENT')
# CardGroup
cardgroup_id_seq = Sequence('S_CARDGROUP')
# Card
virtual_group_id_seq = Sequence("S_VIRTGROUP")
company_id_seq = Sequence("S_COMPANY")
company2role_id_seq = Sequence("S_COMPANY2ROLE")
currency_id_seq = Sequence("S_CURRENCY")
accounting_file_id_seq = Sequence("S_ACCOUNTINGFULE")
simcard_id_seq = Sequence("S_SIMCARD")

