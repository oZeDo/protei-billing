# coding: utf-8
from sqlalchemy import CHAR, CheckConstraint, Column, DateTime, ForeignKey, ForeignKeyConstraint, Index, Integer, LargeBinary, TIMESTAMP, Table, Text, VARCHAR, text
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Accfilestate(Base):
    __tablename__ = 'accfilestate'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    afs_code = Column(VARCHAR(32), nullable=False, unique=True)
    afs_info = Column(VARCHAR(1024))


class Account(Base):
    __tablename__ = 'account'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    created = Column(DateTime, nullable=False, server_default=text("sysdate "))
    contractid = Column(ForeignKey('contract.id', ondelete='CASCADE'), index=True)
    client = Column(ForeignKey('client.id'), index=True)
    acctype = Column(ForeignKey('accounttype.id'), nullable=False)
    external_id = Column(VARCHAR(64), unique=True, server_default=text("NULL"))
    appsubtype = Column(VARCHAR(32))
    balance = Column(NUMBER(asdecimal=False), nullable=False)
    limit = Column(NUMBER(asdecimal=False), nullable=False)
    currency = Column(ForeignKey('currency.id'), nullable=False)
    firsttr_date = Column(TIMESTAMP)
    lasttr_date = Column(TIMESTAMP)
    vgroupid = Column(ForeignKey('virtualgroup.id'), nullable=False, index=True)
    last_charge_date = Column(TIMESTAMP)
    stbalanceday = Column(NUMBER(asdecimal=False))
    stbalancemonth = Column(NUMBER(asdecimal=False))
    state_id = Column(ForeignKey('accountstate.id'), nullable=False)
    last_recharge_date = Column(TIMESTAMP)
    nextbillattempt = Column(DateTime, index=True)
    lastbillattempt = Column(DateTime)
    billing_mode = Column(NUMBER(asdecimal=False), nullable=False)
    external_contract = Column(VARCHAR(125))
    contract_date = Column(DateTime)
    personal_manager = Column(VARCHAR(125))
    spending_limit = Column(NUMBER(asdecimal=False))
    limit_notify = Column(NUMBER(asdecimal=False))
    last_activity_date = Column(DateTime)
    change_version = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    without_lock = Column(NUMBER(asdecimal=False))
    joint_state = Column(VARCHAR(600))
    limit_shift = Column(NUMBER(asdecimal=False))

    accounttype = relationship('Accounttype')
    client1 = relationship('Client', primaryjoin='Account.client == Client.id')
    contract = relationship('Contract')
    currency1 = relationship('Currency')
    state = relationship('Accountstate')
    virtualgroup = relationship('Virtualgroup')


class AccountMlt(Account):
    __tablename__ = 'account_mlt'

    id = Column(ForeignKey('account.id', ondelete='CASCADE'), primary_key=True)
    created = Column(DateTime, nullable=False, server_default=text("current_date "))
    init_card_id = Column(ForeignKey('basecard.id', ondelete='SET NULL'), index=True)
    creator_login = Column(VARCHAR(128))
    info = Column(VARCHAR(1000))
    dealer_id = Column(ForeignKey('company.id'), index=True)

    dealer = relationship('Company')
    init_card = relationship('Basecard')


class Accountingfile(Base):
    __tablename__ = 'accountingfile'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    created = Column(DateTime, nullable=False, server_default=text("sysdate "))
    state = Column(ForeignKey('accfilestate.id'), nullable=False)
    vgroupid = Column(ForeignKey('virtualgroup.id'))
    name = Column(VARCHAR(128), nullable=False)
    code = Column(VARCHAR(32), nullable=False)
    info = Column(VARCHAR(1024))
    currencyid = Column(ForeignKey('currency.id'), nullable=False)
    entercost = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    rarechargentfthreshold = Column(NUMBER(asdecimal=False))
    billing_mode = Column(NUMBER(asdecimal=False))
    harechargentfthreshold = Column(NUMBER(asdecimal=False))

    currency = relationship('Currency')
    accfilestate = relationship('Accfilestate')
    virtualgroup = relationship('Virtualgroup', primaryjoin='Accountingfile.vgroupid == Virtualgroup.id')


class Accountstate(Base):
    __tablename__ = 'accountstate'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    state_code = Column(VARCHAR(32), nullable=False, unique=True)
    state_info = Column(VARCHAR(512))


class Accounttype(Base):
    __tablename__ = 'accounttype'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    at_code = Column(VARCHAR(64), unique=True)
    at_info = Column(VARCHAR(1024))


class Adminstate(Base):
    __tablename__ = 'adminstate'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    state_code = Column(VARCHAR(32), nullable=False, unique=True)
    state_info = Column(VARCHAR(200))


class Auditeventtype(Base):
    __tablename__ = 'auditeventtype'

    event_type = Column(VARCHAR(32), primary_key=True)
    event_info = Column(VARCHAR(1024))


class Baseservicetype(Base):
    __tablename__ = 'baseservicetype'
    __table_args__ = {'comment': 'Основные типы сервисов (Голосовой вызов, SMS, GPRS, MMS, парковка)'}

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    sname = Column(VARCHAR(256))
    code = Column(VARCHAR(64), nullable=False, unique=True)
    info = Column(VARCHAR(1024))


class Billdirtype(Base):
    __tablename__ = 'billdirtype'
    __table_args__ = {'comment': 'Inbound, Outbound, Outbound-extra, etc'}

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    cdirname = Column(VARCHAR(64), nullable=False, unique=True)
    cdirinfo = Column(VARCHAR(2000))


class Billingaction(Base):
    __tablename__ = 'billingaction'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    code = Column(VARCHAR(32), nullable=False, unique=True)
    info = Column(VARCHAR(512))


class Billingmode(Base):
    __tablename__ = 'billingmode'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    mode_name = Column(VARCHAR(16), nullable=False, unique=True)


t_billingparameters = Table(
    'billingparameters', metadata,
    Column('name', VARCHAR(128), nullable=False, unique=True),
    Column('varchar_value', VARCHAR(2048)),
    Column('clob_value', Text),
    Column('description', VARCHAR(512), server_default=text("NULL")),
    Column('group_code', VARCHAR(32)),
    Column('editor', VARCHAR(256)),
    Column('version', VARCHAR(256))
)


class Billingscript(Base):
    __tablename__ = 'billingscripts'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    script_name = Column(VARCHAR(128))
    file_name = Column(VARCHAR(128))
    version = Column(VARCHAR(256))
    value = Column(Text)
    created = Column(DateTime, nullable=False, server_default=text("sysdate "))


class Billingtype(Base):
    __tablename__ = 'billingtype'
    __table_args__ = {'comment': 'Retail, Wholesale, Purchase, etc..'}

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    billtypename = Column(VARCHAR(128))
    billtypecode = Column(VARCHAR(32))


class Billservicecategory(Base):
    __tablename__ = 'billservicecategory'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    bsc_code = Column(VARCHAR(32), unique=True)
    bsc_info = Column(VARCHAR(512))


class BilltrafficclassPrefix(Base):
    __tablename__ = 'billtrafficclass_prefix'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    classid = Column(NUMBER(asdecimal=False), nullable=False)
    prefix = Column(VARCHAR(32), nullable=False, unique=True)
    info = Column(VARCHAR(500))


class BsJobtask(Base):
    __tablename__ = 'bs_jobtask'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    ip = Column(VARCHAR(64))
    login = Column(VARCHAR(128))
    started = Column(DateTime, index=True)
    stopped = Column(DateTime)
    created = Column(DateTime, nullable=False, index=True, server_default=text("sysdate "))
    state = Column(Integer, nullable=False, server_default=text("0 "))
    taskclass = Column(VARCHAR(512), nullable=False)
    jobtype = Column(VARCHAR(128), nullable=False)
    progress = Column(Integer, nullable=False, server_default=text("0 "))
    errcount = Column(Integer, nullable=False, server_default=text("0 "))
    jobtitle = Column(VARCHAR(512))
    serviceid = Column(VARCHAR(64))
    jsontaskview = Column(VARCHAR(4000))
    completion_info = Column(VARCHAR(2000))


class Cardcheckstate(Base):
    __tablename__ = 'cardcheckstate'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    name = Column(VARCHAR(80), nullable=False)
    verify = Column(NUMBER(asdecimal=False), nullable=False)


class Cardstate(Base):
    __tablename__ = 'cardstate'
    __table_args__ = (
        Index('uq_cardstate', 'cardtype', 'state_code', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    cardtype = Column(NUMBER(asdecimal=False), nullable=False)
    state_code = Column(VARCHAR(32), nullable=False)
    state_info = Column(VARCHAR(512))
    state_rules = Column(VARCHAR(1000))
    deleted = Column(NUMBER(asdecimal=False), server_default=text("0"))


class Cardtype(Base):
    __tablename__ = 'cardtype'
    __table_args__ = {'comment': 'SimCard, Recharge Card (VoMS), Parking Card'}

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    cardtype = Column(VARCHAR(64), nullable=False, unique=True)
    info = Column(VARCHAR(1024))


class Client(Base):
    __tablename__ = 'client'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    clienttypeid = Column(ForeignKey('clienttype.id'), nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("sysdate "))
    dname = Column(VARCHAR(200), nullable=False, index=True)
    personid = Column(ForeignKey('personinfo.id', ondelete='SET NULL'))
    passport = Column(VARCHAR(128), index=True)
    regdoctypeid = Column(ForeignKey('client_regdoctype.id'))
    regdoc_issued = Column(DateTime)
    regdoc_issue_place = Column(VARCHAR(500))
    bank_details = Column(VARCHAR(2000))
    vgroupid = Column(ForeignKey('virtualgroup.id'), nullable=False)
    regdoctype_info = Column(VARCHAR(256))
    regdoc_series = Column(VARCHAR(16))
    regdoc_number = Column(VARCHAR(32))
    regaddress_json = Column(VARCHAR(4000))
    dejureaddress_json = Column(VARCHAR(4000))
    letter_of_attorney = Column(VARCHAR(256))
    dname_up = Column(VARCHAR(200), index=True)
    apptype = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    company_id = Column(ForeignKey('company.id'), index=True)
    ntf_method = Column(VARCHAR(18), nullable=False, server_default=text("'sms' "))
    assoc = Column(ForeignKey('client_association.id'))
    primaccountid = Column(ForeignKey('account.id', ondelete='SET NULL'), index=True)
    billmode_id = Column(ForeignKey('billingmode.id'), nullable=False)
    external_id = Column(VARCHAR(64), unique=True, server_default=text("NULL"))
    second_regdoctypeid = Column(ForeignKey('client_regdoctype.id'))
    second_regdoctype_info = Column(VARCHAR(256))
    second_regdoc_series = Column(VARCHAR(32))
    second_regdoc_number = Column(VARCHAR(32))
    second_regdoc_issued = Column(DateTime)
    second_regdoc_expired = Column(DateTime)
    maxageoflocation = Column(NUMBER(asdecimal=False))
    ccomment = Column(VARCHAR(125))
    cinfo = Column(VARCHAR(4000))
    invoice_delivery_settings = Column(VARCHAR(128))

    client_association = relationship('ClientAssociation')
    billmode = relationship('Billingmode')
    clienttype = relationship('Clienttype')
    company = relationship('Company')
    personinfo = relationship('Personinfo')
    account = relationship('Account', primaryjoin='Client.primaccountid == Account.id')
    client_regdoctype = relationship('ClientRegdoctype', primaryjoin='Client.regdoctypeid == ClientRegdoctype.id')
    client_regdoctype1 = relationship('ClientRegdoctype', primaryjoin='Client.second_regdoctypeid == ClientRegdoctype.id')
    virtualgroup = relationship('Virtualgroup')


class ClientInvoice(Base):
    __tablename__ = 'client_invoice'
    __table_args__ = (
        Index('ix_client_invoice', 'client_id', 'bill_from'),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    created = Column(DateTime, nullable=False, server_default=text("sysdate "))
    invoice_id = Column(VARCHAR(64), nullable=False, unique=True)
    client_id = Column(NUMBER(asdecimal=False), nullable=False)
    account_id = Column(NUMBER(asdecimal=False), nullable=False, index=True)
    bill_from = Column(DateTime, nullable=False, index=True)
    bill_to = Column(DateTime, nullable=False, index=True)
    bill_value = Column(NUMBER(asdecimal=False), nullable=False)
    invoice_currency = Column(NUMBER(asdecimal=False), nullable=False)
    payment_due = Column(DateTime)
    payoff_value = Column(NUMBER(asdecimal=False))
    documents_number = Column(NUMBER(asdecimal=False), server_default=text("0"))
    documents_created = Column(DateTime)
    paid_value = Column(NUMBER(asdecimal=False))
    closed = Column(DateTime)
    bill_service_data = Column(Text)


t_client_invoice_backup = Table(
    'client_invoice_backup', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('created', DateTime, nullable=False),
    Column('invoice_id', VARCHAR(64), nullable=False),
    Column('client_id', NUMBER(asdecimal=False), nullable=False),
    Column('account_id', NUMBER(asdecimal=False), nullable=False),
    Column('bill_from', DateTime, nullable=False),
    Column('bill_to', DateTime, nullable=False),
    Column('bill_value', NUMBER(asdecimal=False), nullable=False),
    Column('invoice_currency', NUMBER(asdecimal=False), nullable=False),
    Column('payment_due', DateTime),
    Column('payoff_value', NUMBER(asdecimal=False)),
    Column('documents_number', NUMBER(asdecimal=False)),
    Column('documents_created', DateTime),
    Column('paid_value', NUMBER(asdecimal=False)),
    Column('closed', DateTime),
    Column('bill_service_data', Text)
)


class ClientRegdoctype(Base):
    __tablename__ = 'client_regdoctype'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    typename = Column(VARCHAR(256), nullable=False, unique=True)
    typeinfo = Column(VARCHAR(2000))


class Clienttype(Base):
    __tablename__ = 'clienttype'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    cltypename = Column(VARCHAR(128), nullable=False, unique=True)
    cltypeinfo = Column(VARCHAR(2000))


class Company(Base):
    __tablename__ = 'company'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    comp_name = Column(VARCHAR(256), nullable=False, unique=True)
    comp_info = Column(VARCHAR(4000))
    address = Column(VARCHAR(2000))
    comp_email = Column(VARCHAR(256))
    zipcode = Column(VARCHAR(16))
    phone = Column(VARCHAR(20))
    fax = Column(VARCHAR(20))
    website = Column(VARCHAR(256))
    dejureaddress = Column(VARCHAR(2000))
    comp_code = Column(VARCHAR(256), nullable=False, unique=True)


class Companyrole(Base):
    __tablename__ = 'companyrole'
    __table_args__ = {'comment': 'Дилер, поставщик, производитель, транспортная компания, etc'}

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    rolename = Column(VARCHAR(256), nullable=False, unique=True)
    roleinfo = Column(VARCHAR(1024))


class ConfigDef(Base):
    __tablename__ = 'config_defs'

    acfsupportemail = Column(VARCHAR(512))
    acfsendersmsaddr = Column(VARCHAR(256))
    acfsenderemailaddr = Column(VARCHAR(256))
    id = Column(NUMBER(asdecimal=False), primary_key=True, server_default=text("1 "))


class Contract(Base):
    __tablename__ = 'contract'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    created = Column(DateTime, nullable=False, server_default=text("sysdate "))
    signed = Column(DateTime)
    expired = Column(DateTime)
    contract_no = Column(VARCHAR(64), nullable=False, unique=True)
    contract_info = Column(VARCHAR(2048))
    contract_file = Column(LargeBinary)
    contract_person = Column(VARCHAR(512))
    signer = Column(ForeignKey('client.id', ondelete='CASCADE'), nullable=False, index=True)
    promotion_code = Column(VARCHAR(64))
    contract_file_size = Column(NUMBER(asdecimal=False))
    contract_type = Column(ForeignKey('contracttype.id'))
    contract_file_name = Column(VARCHAR(256))
    dealercompanyid = Column(ForeignKey('company.id'))
    point_of_sale = Column(VARCHAR(200))
    sellerlogin = Column(VARCHAR(64), index=True)

    contracttype = relationship('Contracttype')
    company = relationship('Company')
    client = relationship('Client')


class Contractsubject(Base):
    __tablename__ = 'contractsubject'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    ctscode = Column(VARCHAR(32), nullable=False, unique=True)
    ctsinfo = Column(VARCHAR(2000))


class Country(Base):
    __tablename__ = 'country'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    cname = Column(VARCHAR(200), nullable=False, unique=True)
    iso3166_1_alpha2 = Column(VARCHAR(4))
    mcc = Column(VARCHAR(3), nullable=False, unique=True)
    iseurozone = Column(NUMBER(asdecimal=False))
    prefix = Column(VARCHAR(32))
    iso3166_1_alpha3 = Column(VARCHAR(6))


class Currency(Base):
    __tablename__ = 'currency'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    code = Column(VARCHAR(3), nullable=False, unique=True)
    name = Column(VARCHAR(128), nullable=False)
    baserate = Column(NUMBER(asdecimal=False), nullable=False)
    precision = Column(NUMBER(asdecimal=False), nullable=False)
    displayorder = Column(NUMBER(asdecimal=False), nullable=False)


class Daytype(Base):
    __tablename__ = 'daytype'
    __table_args__ = {'comment': 'System Dictionary of day-types (Day of week, day of month, holidays, workdays, strict date)\n'}

    id = Column(NUMBER(asdecimal=False), primary_key=True, comment='0=any day, 1=Sunday, 2=Monday,...7=Saturday')
    code = Column(VARCHAR(32), nullable=False)
    name = Column(VARCHAR(200), nullable=False)


class Departmentcode(Base):
    __tablename__ = 'departmentcode'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    code = Column(VARCHAR(64), nullable=False, unique=True)
    name = Column(VARCHAR(2000), nullable=False)


class EspRuruCatalog(Base):
    __tablename__ = 'esp_ruru_catalog'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    created = Column(DateTime, nullable=False, server_default=text("sysdate "))
    service_code = Column(VARCHAR(64), nullable=False, unique=True)
    service_name = Column(VARCHAR(500), index=True)
    service_cat = Column(VARCHAR(500))
    tsp_id = Column(NUMBER(asdecimal=False), index=True)
    tsp_name = Column(VARCHAR(500))
    fee_oper_fix = Column(NUMBER(asdecimal=False))
    fee_oper_perc = Column(NUMBER(asdecimal=False))
    fee_kfl_fix = Column(NUMBER(asdecimal=False))
    fee_kfl_perc = Column(NUMBER(asdecimal=False))
    aoc_flag = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    price_min = Column(NUMBER(asdecimal=False))
    price_max = Column(NUMBER(asdecimal=False))
    request_msg = Column(VARCHAR(4000))
    complete_msg = Column(VARCHAR(4000))
    confirm_text = Column(VARCHAR(4000))


class EspRuruConfig(Base):
    __tablename__ = 'esp_ruru_config'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    confirm_text = Column(VARCHAR(4000))
    request_msg = Column(VARCHAR(4000))
    complete_msg = Column(VARCHAR(4000))
    inn = Column(VARCHAR(32))
    last_report_ts = Column(TIMESTAMP)


class Fincorrtype(Base):
    __tablename__ = 'fincorrtype'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    code = Column(VARCHAR(16), nullable=False, unique=True)
    info = Column(VARCHAR(256))
    displayorder = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    billconfig = Column(VARCHAR(4000))
    built_in = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    internal_use = Column(NUMBER(asdecimal=False))


class Gateway(Base):
    __tablename__ = 'gateways'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    gate_id = Column(NUMBER(asdecimal=False), nullable=False)
    begin_time = Column(DateTime)
    end_time = Column(DateTime)
    description = Column(VARCHAR(256))
    gate_type = Column(NUMBER(asdecimal=False))
    address_type_id = Column(NUMBER(asdecimal=False))
    address_type = Column(NUMBER(asdecimal=False))
    zip = Column(VARCHAR(32))
    country = Column(VARCHAR(128))
    region = Column(VARCHAR(128))
    zone = Column(VARCHAR(128))
    city = Column(VARCHAR(128))
    street = Column(VARCHAR(128))
    building = Column(VARCHAR(128))
    build_sect = Column(VARCHAR(128))
    apartment = Column(VARCHAR(128))
    unstruct_info = Column(VARCHAR(1024))
    region_id = Column(NUMBER(asdecimal=False))


class Georegionsize(Base):
    __tablename__ = 'georegionsize'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    qname = Column(VARCHAR(200), nullable=False)
    qinfo = Column(VARCHAR(2000))
    weight = Column(NUMBER(asdecimal=False), nullable=False)


class GprsAp(Base):
    __tablename__ = 'gprs_ap'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    apcode = Column(VARCHAR(32), nullable=False, unique=True)
    apinfo = Column(VARCHAR(2000))


class GprsService(Base):
    __tablename__ = 'gprs_service'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    code = Column(VARCHAR(64), nullable=False, unique=True)
    info = Column(VARCHAR(512))
    externalid = Column(VARCHAR(16), unique=True)
    ratinggroup = Column(VARCHAR(64), unique=True)


class IcTfbundle(Base):
    __tablename__ = 'ic_tfbundle'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    tfbundle_name = Column(VARCHAR(128), nullable=False, unique=True)


class IpAddressPoolType(Base):
    __tablename__ = 'ip_address_pool_type'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    pt_code = Column(VARCHAR(64), nullable=False, unique=True)
    info = Column(VARCHAR(4000))


class IpDataPoint(Base):
    __tablename__ = 'ip_data_points'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    begin_time = Column(DateTime)
    end_time = Column(DateTime)
    description = Column(VARCHAR(256))
    region_id = Column(NUMBER(asdecimal=False))


class IpGateway(Base):
    __tablename__ = 'ip_gateway'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    gate_id = Column(NUMBER(asdecimal=False), nullable=False)
    ip_type = Column(NUMBER(asdecimal=False))
    ipv4 = Column(VARCHAR(16))
    ipv6 = Column(VARCHAR(256))
    ip_port = Column(VARCHAR(8))
    region_id = Column(NUMBER(asdecimal=False))


class IpPlan(Base):
    __tablename__ = 'ip_plan'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    description = Column(VARCHAR(256))
    ip_type = Column(NUMBER(asdecimal=False))
    ipv4 = Column(VARCHAR(16))
    ipv6 = Column(VARCHAR(256))
    ip_mask_type = Column(NUMBER(asdecimal=False))
    ipv4_mask = Column(VARCHAR(16))
    ipv6_mask = Column(VARCHAR(256))
    begin_time = Column(DateTime)
    end_time = Column(DateTime)
    region_id = Column(NUMBER(asdecimal=False))


class Lang(Base):
    __tablename__ = 'lang'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    lang_name = Column(VARCHAR(128), nullable=False, unique=True)
    lang_info = Column(VARCHAR(128))
    lang_code = Column(VARCHAR(3), nullable=False, unique=True)


class LockState(Base):
    __tablename__ = 'lock_state'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    state_code = Column(VARCHAR(32), nullable=False, unique=True)
    state_info = Column(VARCHAR(512))


class Maptileslayer(Base):
    __tablename__ = 'maptileslayer'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    name = Column(VARCHAR(64), nullable=False, unique=True)
    tilesurl = Column(VARCHAR(256))


class Mcellset(Base):
    __tablename__ = 'mcellset'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    created = Column(DateTime, nullable=False, server_default=text("sysdate "))
    csname = Column(VARCHAR(200), nullable=False, index=True)
    csinfo = Column(VARCHAR(2000))


class Measureunit(Base):
    __tablename__ = 'measureunit'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    code = Column(VARCHAR(32), nullable=False, unique=True)
    name = Column(VARCHAR(200), nullable=False)
    info = Column(VARCHAR(1000))


t_message_cdr = Table(
    'message_cdr', metadata,
    Column('record_num', NUMBER(asdecimal=False), nullable=False),
    Column('record_date', TIMESTAMP, nullable=False, index=True),
    Column('event_date', TIMESTAMP, nullable=False),
    Column('client_id', NUMBER(asdecimal=False)),
    Column('message_id', NUMBER(asdecimal=False), nullable=False),
    Column('subject', VARCHAR(255)),
    Column('text', VARCHAR(1024)),
    Index('ix_message_cdr_client', 'client_id', 'record_date')
)


class MobilePlan(Base):
    __tablename__ = 'mobile_plan'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    mcc = Column(VARCHAR(3))
    mnc = Column(VARCHAR(3))
    area_code = Column(VARCHAR(10))
    capacity_from = Column(VARCHAR(11))
    capacity_to = Column(VARCHAR(11))
    capacity_size = Column(NUMBER(asdecimal=False))
    description = Column(VARCHAR(256))
    region = Column(VARCHAR(128))
    city = Column(VARCHAR(128))
    begin_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(VARCHAR(128))
    region_id = Column(NUMBER(asdecimal=False))


class Msgstatecategory(Base):
    __tablename__ = 'msgstatecategory'

    cat_code = Column(VARCHAR(16), primary_key=True)
    cat_info = Column(VARCHAR(1024))


class Notificationmedia(Base):
    __tablename__ = 'notificationmedia'
    __table_args__ = {'comment': 'SMS, URL, MAIL, etc'}

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    mediatype = Column(VARCHAR(32), nullable=False, unique=True)
    info = Column(VARCHAR(1024))


class OcsTransaction(Base):
    __tablename__ = 'ocs_transaction'
    __table_args__ = (
        Index('uq_ocs_transaction', 'tx_system', 'tx_ext_id', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    tx_type = Column(NUMBER(asdecimal=False), nullable=False)
    tx_date = Column(TIMESTAMP, nullable=False, server_default=text("systimestamp "))
    tx_system = Column(VARCHAR(64), nullable=False)
    tx_ext_id = Column(VARCHAR(64), nullable=False)
    tx_value = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    tx_data = Column(VARCHAR(4000))
    account_id = Column(NUMBER(asdecimal=False), nullable=False)
    client = Column(VARCHAR(128))


class Packagepaymode(Base):
    __tablename__ = 'packagepaymode'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    code = Column(VARCHAR(32), nullable=False, unique=True)
    info = Column(VARCHAR(1024))


class Parkingtype(Base):
    __tablename__ = 'parkingtype'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    ptcode = Column(VARCHAR(32), nullable=False, unique=True)
    ptinfo = Column(VARCHAR(1000))


class Parkprivilegetype(Base):
    __tablename__ = 'parkprivilegetype'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    pvtname = Column(VARCHAR(200), nullable=False, unique=True)
    pvtinfo = Column(VARCHAR(1000))


class Parkvehicleregtype(Base):
    __tablename__ = 'parkvehicleregtype'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    vrt_code = Column(VARCHAR(32), nullable=False, unique=True)
    vrt_info = Column(VARCHAR(1000))


class Paymentregistration(Base):
    __tablename__ = 'paymentregistration'
    __table_args__ = (
        Index('uq_paymentregistration', 'payment_system', 'transaction_id', 'trans_type', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    payment_date = Column(DateTime, nullable=False, server_default=text("sysdate "))
    payment_system = Column(VARCHAR(64), nullable=False)
    transaction_id = Column(VARCHAR(64), nullable=False)
    transaction_value = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    account_id = Column(NUMBER(asdecimal=False), nullable=False)
    payer = Column(VARCHAR(128))
    trans_type = Column(NUMBER(asdecimal=False), nullable=False)
    state = Column(NUMBER(asdecimal=False), nullable=False)


class Paymentschemamode(Base):
    __tablename__ = 'paymentschemamode'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    code = Column(VARCHAR(32), nullable=False, unique=True)


class Paymentsystemtype(Base):
    __tablename__ = 'paymentsystemtype'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    pscode = Column(VARCHAR(32), nullable=False, unique=True)
    psname = Column(VARCHAR(256), nullable=False)


t_pbill_accfilecreateprofile = Table(
    'pbill_accfilecreateprofile', metadata,
    Column('c1', Text),
    Column('c2', Text),
    Column('c3', Text),
    Column('c4', Text),
    Column('c5', Text),
    Column('c6', Text),
    Column('c7', Text),
    Column('c8', Text),
    Column('c9', Text),
    Column('c10', NUMBER(asdecimal=False)),
    Column('c11', NUMBER(asdecimal=False)),
    Column('c12', Text),
    Column('c13', Text),
    Column('c14', NUMBER(asdecimal=False)),
    Column('c15', Text),
    Column('c16', NUMBER(asdecimal=False)),
    Column('c17', Text)
)


class Personinfo(Base):
    __tablename__ = 'personinfo'
    __table_args__ = (
        CheckConstraint("sex in ('M','F')"),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    firstname = Column(VARCHAR(256))
    lastname = Column(VARCHAR(64))
    secondname = Column(VARCHAR(64))
    displayname = Column(VARCHAR(200), index=True)
    phone = Column(VARCHAR(80))
    email = Column(VARCHAR(256))
    address = Column(VARCHAR(512))
    dob = Column(DateTime, comment='Date Of Bithrday')
    sex = Column(CHAR(1))
    displayname_up = Column(VARCHAR(200), index=True)
    pob = Column(VARCHAR(512))
    citizenship = Column(VARCHAR(80))
    risklevelid = Column(NUMBER(asdecimal=False))
    departmentcode = Column(VARCHAR(64))


class PhonePlan(Base):
    __tablename__ = 'phone_plan'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    iso_3166_apha_2 = Column(VARCHAR(2))
    iso_3166_apha_3 = Column(VARCHAR(3))
    country_code = Column(VARCHAR(3))
    number_prefix = Column(VARCHAR(14))
    area_code_length = Column(NUMBER(asdecimal=False))
    min_number_length = Column(NUMBER(asdecimal=False))
    max_number_length = Column(NUMBER(asdecimal=False))
    utc_min = Column(NUMBER(asdecimal=False))
    utc_max = Column(NUMBER(asdecimal=False))
    country_dest = Column(VARCHAR(255))
    network_type = Column(NUMBER(asdecimal=False))
    capacity_from = Column(VARCHAR(15))
    capacity_to = Column(VARCHAR(15))
    capacity_size = Column(NUMBER(asdecimal=False))
    location = Column(VARCHAR(255))
    operator_name = Column(VARCHAR(255))
    begin_time = Column(DateTime)
    end_time = Column(DateTime)
    mcc = Column(VARCHAR(3))
    mnc = Column(VARCHAR(3))
    status = Column(VARCHAR(128))
    description = Column(VARCHAR(256))
    operator_code = Column(VARCHAR(4))
    region_id = Column(NUMBER(asdecimal=False))


class PhoneSpecial(Base):
    __tablename__ = 'phone_special'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    phone_number = Column(VARCHAR(32))
    description = Column(VARCHAR(256))
    begin_time = Column(DateTime)
    end_time = Column(DateTime)
    ip_type = Column(NUMBER(asdecimal=False))
    ipv4 = Column(VARCHAR(16))
    ipv6 = Column(VARCHAR(256))
    region_id = Column(NUMBER(asdecimal=False))


class Productactivationcodestate(Base):
    __tablename__ = 'productactivationcodestate'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    state_code = Column(VARCHAR(200), nullable=False)
    description = Column(VARCHAR(1000))


t_productsubscription_ob42_back = Table(
    'productsubscription_ob42_back', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('orderdate', DateTime, nullable=False),
    Column('order_no', VARCHAR(32), nullable=False),
    Column('product_id', NUMBER(asdecimal=False), nullable=False),
    Column('order_cost', NUMBER(asdecimal=False), nullable=False),
    Column('currencyid', NUMBER(asdecimal=False), nullable=False),
    Column('startbilldate', DateTime),
    Column('account_id', NUMBER(asdecimal=False), nullable=False),
    Column('client_id', NUMBER(asdecimal=False)),
    Column('targetdesc', VARCHAR(512)),
    Column('payment_schema_id', NUMBER(asdecimal=False), nullable=False),
    Column('nextbilldate', DateTime, nullable=False),
    Column('lastbillamount', NUMBER(asdecimal=False), nullable=False),
    Column('totalbillamount', NUMBER(asdecimal=False), nullable=False),
    Column('lastbillattempt', DateTime),
    Column('lastattempnumber', NUMBER(asdecimal=False)),
    Column('nextbillattempt', DateTime, nullable=False),
    Column('payruleid', NUMBER(asdecimal=False)),
    Column('payrulestart', DateTime),
    Column('state', NUMBER(asdecimal=False), nullable=False),
    Column('cardid', NUMBER(asdecimal=False)),
    Column('accfileid', NUMBER(asdecimal=False)),
    Column('lastbilldate', DateTime),
    Column('last_error', VARCHAR(64)),
    Column('nextperiodcost', NUMBER(asdecimal=False)),
    Column('provisioning', NUMBER(asdecimal=False), nullable=False),
    Column('uservars', VARCHAR(4000))
)


class Productsubsstate(Base):
    __tablename__ = 'productsubsstate'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    statecode = Column(VARCHAR(32), nullable=False, unique=True)
    stateinfo = Column(VARCHAR(512))


class Producttype(Base):
    __tablename__ = 'producttype'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    prodtypename = Column(VARCHAR(512), nullable=False)
    prodtypeinfo = Column(VARCHAR(4000))


class Risklevel(Base):
    __tablename__ = 'risklevel'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    lvl = Column(VARCHAR(100), nullable=False, unique=True)


class Routeschema(Base):
    __tablename__ = 'routeschema'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    rsname = Column(VARCHAR(256), nullable=False)
    rsinfo = Column(VARCHAR(2000))


class RuruCrosscheckFile(Base):
    __tablename__ = 'ruru_crosscheck_files'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    created = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    rep_from = Column(TIMESTAMP)
    rep_till = Column(TIMESTAMP)
    file_content = Column(Text)


class Rurutransaction(Base):
    __tablename__ = 'rurutransaction'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    created = Column(TIMESTAMP, nullable=False)
    state = Column(NUMBER(asdecimal=False), nullable=False, index=True)
    actual_timeout = Column(TIMESTAMP, index=True)
    msisdn = Column(VARCHAR(32), nullable=False, index=True)
    params = Column(VARCHAR(4000))
    closed = Column(TIMESTAMP)


t_schema_patches = Table(
    'schema_patches', metadata,
    Column('installed', DateTime),
    Column('patch_name', VARCHAR(256), unique=True)
)


class Sendermessage(Base):
    __tablename__ = 'sendermessage'
    __table_args__ = (
        Index('ix_message_main', 'send_time', 'direction_name', 'processed'),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    direction_name = Column(VARCHAR(128), nullable=False)
    url = Column(VARCHAR(512))
    source_address = Column(VARCHAR(128))
    destination_address = Column(VARCHAR(128))
    body = Column(VARCHAR(1024))
    attempt_count = Column(NUMBER(asdecimal=False))
    processed = Column(NUMBER(1, 0, False), nullable=False)
    send_time = Column(TIMESTAMP, nullable=False)
    is_immediate = Column(NUMBER(1, 0, False))
    validity_time = Column(TIMESTAMP)
    subject_message = Column(VARCHAR(255))
    http_headers = Column(VARCHAR(2000))
    params = Column(VARCHAR(500))
    schedule = Column(VARCHAR(100))


class Servicecommand(Base):
    __tablename__ = 'servicecommand'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    code = Column(VARCHAR(32), nullable=False, unique=True)
    required_tags = Column(VARCHAR(512))
    info = Column(VARCHAR(1024))
    message_tags = Column(VARCHAR(512))


class Simnumberstate(Base):
    __tablename__ = 'simnumberstate'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    ns_code = Column(VARCHAR(16), nullable=False, unique=True)
    ns_info = Column(VARCHAR(1000))


class Simnumbertype(Base):
    __tablename__ = 'simnumbertype'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    numtype = Column(VARCHAR(32), nullable=False, unique=True)


class Timeunit(Base):
    __tablename__ = 'timeunit'
    __table_args__ = (
        CheckConstraint('(DSINTERVAL IS NULL AND YMINTERVAL IS NOT NULL) OR\n                                          (DSINTERVAL IS NOT NULL AND YMINTERVAL IS NULL)'),
        CheckConstraint('(DSINTERVAL IS NULL AND YMINTERVAL IS NOT NULL) OR\n                                          (DSINTERVAL IS NOT NULL AND YMINTERVAL IS NULL)')
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    unitcode = Column(VARCHAR(5), nullable=False, unique=True)
    unitname = Column(VARCHAR(128), nullable=False)
    multiplier = Column(NUMBER(asdecimal=False), nullable=False)
    dsinterval = Column(VARCHAR(6))
    yminterval = Column(VARCHAR(5))


class TmDataprocjournal(Base):
    __tablename__ = 'tm_dataprocjournal'
    __table_args__ = (
        Index('uk_dataprocjournal_recidjid', 'nrecordid', 'strjournalid', unique=True),
    )

    nid = Column(NUMBER(asdecimal=False), primary_key=True)
    nrecordid = Column(NUMBER(asdecimal=False), nullable=False)
    strjournalid = Column(VARCHAR(128), nullable=False, index=True)
    strkey = Column(VARCHAR(256))
    bdata = Column(LargeBinary)


class TmImportsequence(Base):
    __tablename__ = 'tm_importsequences'

    strsequence = Column(VARCHAR(64), primary_key=True, comment='Идентификатор последовательности')
    nvalue = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "), comment='Кэшированное значение последовательности')


class TmReportfile(Base):
    __tablename__ = 'tm_reportfile'

    nid = Column(NUMBER(asdecimal=False), primary_key=True)
    dcreated = Column(DateTime, nullable=False, server_default=text("sysdate "))
    fullpath = Column(VARCHAR(1024), nullable=False)
    displayname = Column(VARCHAR(256))
    reportid = Column(NUMBER(asdecimal=False), nullable=False)
    filetitle = Column(VARCHAR(256))
    filesize = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))


t_tmp_ob443_op = Table(
    'tmp_ob443_op', metadata,
    Column('operatorid', NUMBER(asdecimal=False), nullable=False),
    Column('locid', Integer)
)


t_tmp_ob443_sgsn = Table(
    'tmp_ob443_sgsn', metadata,
    Column('sgsngroupid', NUMBER(asdecimal=False), nullable=False),
    Column('locid', Integer)
)


t_tmp_patch_f16974 = Table(
    'tmp_patch_f16974', metadata,
    Column('planid', NUMBER(asdecimal=False), nullable=False),
    Column('destvgroup', NUMBER(asdecimal=False))
)


class TrgActiontype(Base):
    __tablename__ = 'trg_actiontype'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    act_type = Column(VARCHAR(64), nullable=False, unique=True)
    description = Column(VARCHAR(500))


class TrgEventtype(Base):
    __tablename__ = 'trg_eventtype'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    evt_type = Column(VARCHAR(64), nullable=False, unique=True)
    description = Column(VARCHAR(500))


class Userrole(Base):
    __tablename__ = 'userrole'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    rolename = Column(VARCHAR(200), nullable=False, unique=True)
    roleinfo = Column(VARCHAR(2000))
    ca_role_account = Column(VARCHAR(64))
    ca_role_pwd = Column(VARCHAR(128))
    requiretargetcompany = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))


t_v_qosp = Table(
    'v_qosp', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('code', VARCHAR(32), nullable=False),
    Column('servicetype', NUMBER(asdecimal=False)),
    Column('name', VARCHAR(128), nullable=False),
    Column('extid', VARCHAR(32), nullable=False),
    Column('classid', NUMBER(asdecimal=False)),
    Column('dspeed', NUMBER(asdecimal=False), nullable=False),
    Column('uspeed', NUMBER(asdecimal=False), nullable=False)
)


class VadService(Base):
    __tablename__ = 'vad_service'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    service_code = Column(VARCHAR(64), nullable=False, unique=True)
    service_info = Column(VARCHAR(1024))


t_view_accfile_products = Table(
    'view_accfile_products', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('accfileid', NUMBER(asdecimal=False), nullable=False),
    Column('prodid', NUMBER(asdecimal=False), nullable=False),
    Column('ordercode', VARCHAR(64), nullable=False),
    Column('info', VARCHAR(1024)),
    Column('activefrom', DateTime, nullable=False),
    Column('expired', DateTime),
    Column('autoorderflag', NUMBER(asdecimal=False), nullable=False),
    Column('actonfirstusage', NUMBER(asdecimal=False), nullable=False),
    Column('ussdcontrol', NUMBER(asdecimal=False), nullable=False),
    Column('systemcontrol', NUMBER(asdecimal=False), nullable=False),
    Column('webcontrol', NUMBER(asdecimal=False), nullable=False),
    Column('config', VARCHAR(4000)),
    Column('currencyid', NUMBER(asdecimal=False), nullable=False),
    Column('prodtypeid', NUMBER(asdecimal=False), nullable=False),
    Column('prodcode', VARCHAR(64), nullable=False),
    Column('prodinfo', VARCHAR(1024)),
    Column('prodname', VARCHAR(256), nullable=False),
    Column('smprodnumber', NUMBER(asdecimal=False), nullable=False),
    Column('initprovstate', NUMBER(asdecimal=False), nullable=False),
    Column('provrequired', NUMBER(asdecimal=False), nullable=False),
    Column('prodtypename', VARCHAR(512), nullable=False),
    Column('prodtypeinfo', VARCHAR(4000)),
    Column('servicecode', VARCHAR(64)),
    Column('serviceinfo', VARCHAR(1024)),
    Column('currcode', VARCHAR(3), nullable=False),
    Column('ordercost', NUMBER(asdecimal=False), nullable=False),
    Column('noordercostonacfchange', NUMBER(asdecimal=False))
)


t_view_accfileplanshedule = Table(
    'view_accfileplanshedule', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('accfileid', NUMBER(asdecimal=False), nullable=False),
    Column('billtype', NUMBER(asdecimal=False)),
    Column('activefrom', DateTime, nullable=False),
    Column('activetill', DateTime),
    Column('planid', NUMBER(asdecimal=False), nullable=False),
    Column('entryinfo', VARCHAR(1000)),
    Column('priority', NUMBER(asdecimal=False), nullable=False),
    Column('destaccfile', NUMBER(asdecimal=False)),
    Column('billtypecode', VARCHAR(32)),
    Column('billtypename', VARCHAR(128)),
    Column('planname', VARCHAR(256)),
    Column('destacfname', VARCHAR(128))
)


t_view_accfiles = Table(
    'view_accfiles', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('created', DateTime, nullable=False),
    Column('state', NUMBER(asdecimal=False), nullable=False),
    Column('vgroupid', NUMBER(asdecimal=False)),
    Column('name', VARCHAR(128), nullable=False),
    Column('code', VARCHAR(32), nullable=False),
    Column('info', VARCHAR(1024)),
    Column('currencyid', NUMBER(asdecimal=False), nullable=False),
    Column('entercost', NUMBER(asdecimal=False), nullable=False),
    Column('rarechargentfthreshold', NUMBER(asdecimal=False)),
    Column('billing_mode', NUMBER(asdecimal=False)),
    Column('harechargentfthreshold', NUMBER(asdecimal=False)),
    Column('currname', VARCHAR(3), nullable=False),
    Column('groupname', VARCHAR(200), nullable=False),
    Column('ownercompid', NUMBER(asdecimal=False), nullable=False),
    Column('ownercompname', VARCHAR(256), nullable=False)
)


t_view_accfilestate = Table(
    'view_accfilestate', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('simexists', NUMBER(asdecimal=False)),
    Column('pinexists', NUMBER(asdecimal=False)),
    Column('corpgroupexists', NUMBER(asdecimal=False))
)


t_view_account = Table(
    'view_account', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('created', DateTime, nullable=False),
    Column('contractid', NUMBER(asdecimal=False)),
    Column('client', NUMBER(asdecimal=False)),
    Column('acctype', NUMBER(asdecimal=False), nullable=False),
    Column('external_id', VARCHAR(64)),
    Column('appsubtype', VARCHAR(32)),
    Column('balance', NUMBER(asdecimal=False), nullable=False),
    Column('limit', NUMBER(asdecimal=False), nullable=False),
    Column('currency', NUMBER(asdecimal=False), nullable=False),
    Column('firsttr_date', TIMESTAMP),
    Column('lasttr_date', TIMESTAMP),
    Column('vgroupid', NUMBER(asdecimal=False), nullable=False),
    Column('last_charge_date', TIMESTAMP),
    Column('stbalanceday', NUMBER(asdecimal=False)),
    Column('stbalancemonth', NUMBER(asdecimal=False)),
    Column('state_id', NUMBER(asdecimal=False), nullable=False),
    Column('last_recharge_date', TIMESTAMP),
    Column('nextbillattempt', DateTime),
    Column('lastbillattempt', DateTime),
    Column('billing_mode', NUMBER(asdecimal=False), nullable=False),
    Column('external_contract', VARCHAR(125)),
    Column('contract_date', DateTime),
    Column('personal_manager', VARCHAR(125)),
    Column('spending_limit', NUMBER(asdecimal=False)),
    Column('limit_notify', NUMBER(asdecimal=False)),
    Column('last_activity_date', DateTime),
    Column('change_version', NUMBER(asdecimal=False), nullable=False),
    Column('without_lock', NUMBER(asdecimal=False)),
    Column('joint_state', VARCHAR(600)),
    Column('limit_shift', NUMBER(asdecimal=False)),
    Column('currcode', VARCHAR(3), nullable=False),
    Column('dname', VARCHAR(200)),
    Column('dname_up', VARCHAR(200)),
    Column('init_card_id', NUMBER(asdecimal=False)),
    Column('ma_id', NUMBER(asdecimal=False))
)


t_view_account_mlt = Table(
    'view_account_mlt', metadata,
    Column('account_id', NUMBER(asdecimal=False), nullable=False),
    Column('acctype', NUMBER(asdecimal=False), nullable=False),
    Column('balance', NUMBER(asdecimal=False), nullable=False),
    Column('limit', NUMBER(asdecimal=False), nullable=False),
    Column('client_id', NUMBER(asdecimal=False)),
    Column('currency_id', NUMBER(asdecimal=False), nullable=False),
    Column('last_charge_date', TIMESTAMP),
    Column('last_recharge_date', TIMESTAMP),
    Column('state_id', NUMBER(asdecimal=False), nullable=False),
    Column('vgroupid', NUMBER(asdecimal=False), nullable=False),
    Column('currcode', VARCHAR(3), nullable=False),
    Column('dname', VARCHAR(200), nullable=False),
    Column('dname_up', VARCHAR(200)),
    Column('macreatorlogin', VARCHAR(128)),
    Column('mainfo', VARCHAR(1000)),
    Column('madealerid', NUMBER(asdecimal=False)),
    Column('simcardnumber', NUMBER(asdecimal=False))
)


t_view_account_mlt_sim = Table(
    'view_account_mlt_sim', metadata,
    Column('account_id', NUMBER(asdecimal=False), nullable=False),
    Column('madealerid', NUMBER(asdecimal=False)),
    Column('balance', NUMBER(asdecimal=False), nullable=False),
    Column('limit', NUMBER(asdecimal=False), nullable=False),
    Column('client_id', NUMBER(asdecimal=False)),
    Column('currency_id', NUMBER(asdecimal=False), nullable=False),
    Column('last_charge_date', TIMESTAMP),
    Column('last_recharge_date', TIMESTAMP),
    Column('state_id', NUMBER(asdecimal=False), nullable=False),
    Column('vgroupid', NUMBER(asdecimal=False), nullable=False),
    Column('currcode', VARCHAR(3), nullable=False),
    Column('dname', VARCHAR(200), nullable=False),
    Column('dname_up', VARCHAR(200)),
    Column('macreatorlogin', VARCHAR(128)),
    Column('mainfo', VARCHAR(1000)),
    Column('simcard_id', NUMBER(asdecimal=False), nullable=False),
    Column('iccid', VARCHAR(32), nullable=False),
    Column('imsi', VARCHAR(64), nullable=False),
    Column('msisdn', VARCHAR(32)),
    Column('dealerid', NUMBER(asdecimal=False)),
    Column('factsellerid', NUMBER(asdecimal=False)),
    Column('activated', DateTime)
)


t_view_adm_anonymous_cards = Table(
    'view_adm_anonymous_cards', metadata,
    Column('cardid', NUMBER(asdecimal=False), nullable=False),
    Column('accfileid', NUMBER(asdecimal=False), nullable=False),
    Column('shipped', DateTime),
    Column('actdate', DateTime),
    Column('msisdn', VARCHAR(32)),
    Column('d_msisdn', VARCHAR(32)),
    Column('iccid', VARCHAR(32), nullable=False),
    Column('account_id', NUMBER(asdecimal=False), nullable=False),
    Column('acfname', VARCHAR(128), nullable=False),
    Column('vgroupid', NUMBER(asdecimal=False)),
    Column('dealerid', NUMBER(asdecimal=False)),
    Column('operstate', NUMBER(asdecimal=False))
)


t_view_bs_jobtask = Table(
    'view_bs_jobtask', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('vgroupid', NUMBER(asdecimal=False)),
    Column('ip', VARCHAR(64)),
    Column('login', VARCHAR(128)),
    Column('started', DateTime),
    Column('stopped', DateTime),
    Column('created', DateTime, nullable=False),
    Column('state', Integer, nullable=False),
    Column('taskclass', VARCHAR(512), nullable=False),
    Column('jobtype', VARCHAR(128), nullable=False),
    Column('progress', Integer, nullable=False),
    Column('errcount', Integer, nullable=False),
    Column('txstate', VARCHAR(20)),
    Column('jobtitle', VARCHAR(512)),
    Column('txstarted', VARCHAR(19)),
    Column('txstopped', VARCHAR(19)),
    Column('txcreated', VARCHAR(19)),
    Column('serviceid', VARCHAR(64)),
    Column('completion_info', VARCHAR(2000))
)


t_view_bs_jobtasklog = Table(
    'view_bs_jobtasklog', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('taskid', NUMBER(asdecimal=False), nullable=False),
    Column('msgcreated', DateTime, nullable=False),
    Column('msglevel', NUMBER(asdecimal=False), nullable=False),
    Column('msgtext', VARCHAR(1024), nullable=False),
    Column('stacktraceinfo', VARCHAR(2048)),
    Column('txmsgcreated', VARCHAR(19)),
    Column('txlevel', VARCHAR(15))
)


t_view_cardseries = Table(
    'view_cardseries', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('name', VARCHAR(256), nullable=False),
    Column('generated', DateTime, nullable=False),
    Column('cardamount', NUMBER(asdecimal=False), nullable=False),
    Column('cardtype', NUMBER(asdecimal=False), nullable=False),
    Column('seriesprefix', VARCHAR(64), nullable=False),
    Column('info', VARCHAR(2000)),
    Column('cardfacevalue', NUMBER(asdecimal=False)),
    Column('isdeleted', NUMBER(asdecimal=False), nullable=False),
    Column('accfileid', NUMBER(asdecimal=False), nullable=False),
    Column('currencyid', NUMBER(asdecimal=False), nullable=False),
    Column('cardtypename', VARCHAR(64), nullable=False),
    Column('currcode', VARCHAR(3), nullable=False)
)


t_view_cells = Table(
    'view_cells', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('cellsetid', NUMBER(asdecimal=False), nullable=False),
    Column('lac', NUMBER(asdecimal=False), nullable=False),
    Column('cellid', NUMBER(asdecimal=False), nullable=False),
    Column('csname', VARCHAR(200), nullable=False),
    Column('csinfo', VARCHAR(2000))
)


t_view_client = Table(
    'view_client', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('clienttypeid', NUMBER(asdecimal=False), nullable=False),
    Column('created', DateTime, nullable=False),
    Column('dname', VARCHAR(200), nullable=False),
    Column('personid', NUMBER(asdecimal=False)),
    Column('passport', VARCHAR(128)),
    Column('regdoctypeid', NUMBER(asdecimal=False)),
    Column('regdoc_issued', DateTime),
    Column('regdoc_issue_place', VARCHAR(500)),
    Column('bank_details', VARCHAR(2000)),
    Column('vgroupid', NUMBER(asdecimal=False), nullable=False),
    Column('regdoctype_info', VARCHAR(256)),
    Column('regdoc_series', VARCHAR(16)),
    Column('regdoc_number', VARCHAR(32)),
    Column('regaddress_json', VARCHAR(4000)),
    Column('dejureaddress_json', VARCHAR(4000)),
    Column('letter_of_attorney', VARCHAR(256)),
    Column('dname_up', VARCHAR(200)),
    Column('apptype', NUMBER(asdecimal=False), nullable=False),
    Column('company_id', NUMBER(asdecimal=False)),
    Column('ntf_method', VARCHAR(18), nullable=False),
    Column('assoc', NUMBER(asdecimal=False)),
    Column('primaccountid', NUMBER(asdecimal=False)),
    Column('billmode_id', NUMBER(asdecimal=False), nullable=False),
    Column('external_id', VARCHAR(64)),
    Column('second_regdoctypeid', NUMBER(asdecimal=False)),
    Column('second_regdoctype_info', VARCHAR(256)),
    Column('second_regdoc_series', VARCHAR(32)),
    Column('second_regdoc_number', VARCHAR(32)),
    Column('second_regdoc_issued', DateTime),
    Column('second_regdoc_expired', DateTime),
    Column('maxageoflocation', NUMBER(asdecimal=False)),
    Column('ccomment', VARCHAR(125)),
    Column('cinfo', VARCHAR(4000)),
    Column('invoice_delivery_settings', VARCHAR(128)),
    Column('bill_mode_name', VARCHAR(16), nullable=False),
    Column('cltypeinfo', VARCHAR(2000)),
    Column('isprepaid', NUMBER(asdecimal=False)),
    Column('regdoctypename', VARCHAR(256)),
    Column('vgroupname', VARCHAR(200), nullable=False),
    Column('contactname', VARCHAR(200)),
    Column('contactname_up', VARCHAR(200)),
    Column('contactdob', DateTime),
    Column('simcardsnumber', NUMBER(asdecimal=False))
)


t_view_client_accbalance = Table(
    'view_client_accbalance', metadata,
    Column('client_id', NUMBER(asdecimal=False)),
    Column('currcode', VARCHAR(3), nullable=False),
    Column('num', NUMBER(asdecimal=False)),
    Column('money', NUMBER(asdecimal=False))
)


t_view_client_account_stat = Table(
    'view_client_account_stat', metadata,
    Column('client_id', NUMBER(asdecimal=False)),
    Column('acc_count', NUMBER(asdecimal=False)),
    Column('acc_act_count', NUMBER(asdecimal=False)),
    Column('acc_inact_count', NUMBER(asdecimal=False))
)


t_view_client_card_stat = Table(
    'view_client_card_stat', metadata,
    Column('client_id', NUMBER(asdecimal=False)),
    Column('sim_count', NUMBER(asdecimal=False)),
    Column('sim_act_count', NUMBER(asdecimal=False)),
    Column('sim_finblock_count', NUMBER(asdecimal=False)),
    Column('sim_del_count', NUMBER(asdecimal=False)),
    Column('sim_no_user_count', NUMBER(asdecimal=False))
)


t_view_client_invoice = Table(
    'view_client_invoice', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('created', DateTime, nullable=False),
    Column('invoice_id', VARCHAR(64), nullable=False),
    Column('client_id', NUMBER(asdecimal=False), nullable=False),
    Column('account_id', NUMBER(asdecimal=False), nullable=False),
    Column('bill_from', DateTime, nullable=False),
    Column('bill_to', DateTime, nullable=False),
    Column('bill_value', NUMBER(asdecimal=False), nullable=False),
    Column('currency_code', VARCHAR(3), nullable=False),
    Column('currency_id', NUMBER(asdecimal=False), nullable=False),
    Column('payment_due', DateTime),
    Column('payoff_value', NUMBER(asdecimal=False)),
    Column('documents_number', NUMBER(asdecimal=False)),
    Column('documents_created', DateTime),
    Column('paid_value', NUMBER(asdecimal=False)),
    Column('closed', DateTime)
)


t_view_client_person = Table(
    'view_client_person', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('apptype', NUMBER(asdecimal=False), nullable=False),
    Column('clienttypeid', NUMBER(asdecimal=False), nullable=False),
    Column('company_id', NUMBER(asdecimal=False)),
    Column('created', DateTime, nullable=False),
    Column('dname', VARCHAR(200), nullable=False),
    Column('dname_up', VARCHAR(200)),
    Column('vgroupid', NUMBER(asdecimal=False), nullable=False),
    Column('ntf_method', VARCHAR(18), nullable=False),
    Column('billmode_id', NUMBER(asdecimal=False), nullable=False),
    Column('bill_mode_name', VARCHAR(16), nullable=False),
    Column('cltypeinfo', VARCHAR(2000)),
    Column('isprepaid', NUMBER(asdecimal=False)),
    Column('vgroupname', VARCHAR(200), nullable=False),
    Column('contactemail', VARCHAR(256)),
    Column('contactphone', VARCHAR(80)),
    Column('contactdob', DateTime),
    Column('simcardsnumber', NUMBER(asdecimal=False)),
    Column('accountsnumber', NUMBER(asdecimal=False))
)


t_view_client_vpn = Table(
    'view_client_vpn', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('client_id', NUMBER(asdecimal=False), nullable=False),
    Column('vpn_type', NUMBER(asdecimal=False), nullable=False),
    Column('description', VARCHAR(1000)),
    Column('vt_code', VARCHAR(64), nullable=False),
    Column('vt_info', VARCHAR(4000)),
    Column('pool_count', NUMBER(asdecimal=False))
)


t_view_companies = Table(
    'view_companies', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('comp_name', VARCHAR(256), nullable=False),
    Column('comp_info', VARCHAR(4000)),
    Column('address', VARCHAR(2000)),
    Column('comp_email', VARCHAR(256)),
    Column('zipcode', VARCHAR(16)),
    Column('phone', VARCHAR(20)),
    Column('fax', VARCHAR(20)),
    Column('website', VARCHAR(256)),
    Column('dejureaddress', VARCHAR(2000)),
    Column('comp_code', VARCHAR(256), nullable=False),
    Column('comproles', VARCHAR(4000))
)


t_view_comproles_agg = Table(
    'view_comproles_agg', metadata,
    Column('companyid', NUMBER(asdecimal=False), nullable=False),
    Column('comproles', VARCHAR(4000))
)


t_view_curr_prod_stat = Table(
    'view_curr_prod_stat', metadata,
    Column('product_id', NUMBER(asdecimal=False), nullable=False),
    Column('accfileid', NUMBER(asdecimal=False)),
    Column('orderscount', NUMBER(asdecimal=False)),
    Column('activecount', NUMBER(asdecimal=False)),
    Column('cancelcount', NUMBER(asdecimal=False)),
    Column('currid', NUMBER(asdecimal=False), nullable=False),
    Column('currcode', VARCHAR(3), nullable=False),
    Column('billserviceid', NUMBER(asdecimal=False)),
    Column('prodname', VARCHAR(256), nullable=False),
    Column('vgroupid', NUMBER(asdecimal=False), nullable=False)
)


t_view_discountautoorder = Table(
    'view_discountautoorder', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('accfileid', NUMBER(asdecimal=False), nullable=False),
    Column('active_from', DateTime, nullable=False),
    Column('active_till', DateTime, nullable=False),
    Column('rule_info', VARCHAR(1024)),
    Column('client_type', NUMBER(asdecimal=False)),
    Column('paym_system', NUMBER(asdecimal=False), nullable=False),
    Column('min_paym_value', NUMBER(asdecimal=False), nullable=False),
    Column('prod_to_order', NUMBER(asdecimal=False), nullable=False),
    Column('cltypename', VARCHAR(128)),
    Column('cltypeinfo', VARCHAR(2000)),
    Column('psname', VARCHAR(256), nullable=False),
    Column('pscode', VARCHAR(32), nullable=False),
    Column('prodname', VARCHAR(256), nullable=False)
)


t_view_drep_anonymous_cards = Table(
    'view_drep_anonymous_cards', metadata,
    Column('shipped', DateTime),
    Column('actdate', DateTime),
    Column('msisdn', VARCHAR(32)),
    Column('d_msisdn', VARCHAR(32)),
    Column('iccid', VARCHAR(32), nullable=False),
    Column('acfname', VARCHAR(128), nullable=False),
    Column('dealerid', NUMBER(asdecimal=False))
)


t_view_drep_registered_cards = Table(
    'view_drep_registered_cards', metadata,
    Column('shipped', DateTime),
    Column('regdate', DateTime, nullable=False),
    Column('clientname', VARCHAR(200), nullable=False),
    Column('contract_no', VARCHAR(64), nullable=False),
    Column('msisdn', VARCHAR(32)),
    Column('d_msisdn', VARCHAR(32)),
    Column('iccid', VARCHAR(32), nullable=False),
    Column('tariffplanname', VARCHAR(128), nullable=False),
    Column('startbalance', NUMBER(asdecimal=False)),
    Column('sellercompany', VARCHAR(256), nullable=False),
    Column('agentcode', VARCHAR(64)),
    Column('agentname', VARCHAR(200)),
    Column('sellerlogin', VARCHAR(64)),
    Column('sellercompanyid', NUMBER(asdecimal=False)),
    Column('sellerloginid', NUMBER(asdecimal=False))
)


t_view_drep_sales_cards = Table(
    'view_drep_sales_cards', metadata,
    Column('shipped', DateTime),
    Column('actdate', DateTime),
    Column('contract_no', VARCHAR(64)),
    Column('msisdn', VARCHAR(32)),
    Column('d_msisdn', VARCHAR(32)),
    Column('iccid', VARCHAR(32), nullable=False),
    Column('acfname', VARCHAR(128), nullable=False),
    Column('cardfacevalue', NUMBER(asdecimal=False)),
    Column('regdate', DateTime),
    Column('clientname', VARCHAR(200)),
    Column('dealerid', NUMBER(asdecimal=False))
)


t_view_drep_waiting_cards = Table(
    'view_drep_waiting_cards', metadata,
    Column('shipped', DateTime),
    Column('msisdn', VARCHAR(32)),
    Column('d_msisdn', VARCHAR(32)),
    Column('iccid', VARCHAR(32), nullable=False),
    Column('acfname', VARCHAR(128), nullable=False),
    Column('dealerid', NUMBER(asdecimal=False))
)


t_view_extservice = Table(
    'view_extservice', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('code', VARCHAR(32), nullable=False),
    Column('companyid', NUMBER(asdecimal=False)),
    Column('info', VARCHAR(1024)),
    Column('comp_name', VARCHAR(256), nullable=False),
    Column('comp_info', VARCHAR(4000)),
    Column('comp_code', VARCHAR(256), nullable=False)
)


t_view_ic_operator = Table(
    'view_ic_operator', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('oper_name', VARCHAR(200), nullable=False),
    Column('conn_date', DateTime),
    Column('upd_date', DateTime),
    Column('contract_no', VARCHAR(64), nullable=False),
    Column('currency_id', NUMBER(asdecimal=False)),
    Column('curr_name', VARCHAR(128))
)


t_view_ic_operconn = Table(
    'view_ic_operconn', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('conn_ip', VARCHAR(32), nullable=False),
    Column('conn_port', NUMBER(asdecimal=False), nullable=False),
    Column('sgunit_name', VARCHAR(128), nullable=False),
    Column('point_code', NUMBER(asdecimal=False), nullable=False),
    Column('operator_id', NUMBER(asdecimal=False), nullable=False),
    Column('conn_type', CHAR(1), nullable=False),
    Column('tfbundle_id', NUMBER(asdecimal=False), nullable=False),
    Column('channel_range', VARCHAR(1000)),
    Column('oper_name', VARCHAR(200), nullable=False),
    Column('tfbundle_name', VARCHAR(128), nullable=False)
)


t_view_ic_schedule = Table(
    'view_ic_schedule', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('operator_id', NUMBER(asdecimal=False), nullable=False),
    Column('date_from', DateTime, nullable=False),
    Column('date_till', DateTime),
    Column('sched_comment', VARCHAR(512)),
    Column('oper_name', VARCHAR(200), nullable=False)
)


t_view_ic_tariff = Table(
    'view_ic_tariff', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('sched_id', NUMBER(asdecimal=False), nullable=False),
    Column('conn_type', CHAR(1), nullable=False),
    Column('tfbundle_id', NUMBER(asdecimal=False)),
    Column('ext_dir_id', NUMBER(asdecimal=False)),
    Column('mb_cost', NUMBER(asdecimal=False)),
    Column('date_from', DateTime, nullable=False),
    Column('date_till', DateTime),
    Column('sched_comment', VARCHAR(512)),
    Column('operator_id', NUMBER(asdecimal=False), nullable=False),
    Column('dir_name', VARCHAR(256), nullable=False),
    Column('dir_index', VARCHAR(64), nullable=False),
    Column('tfbundle_name', VARCHAR(128), nullable=False),
    Column('currcode', VARCHAR(3), nullable=False),
    Column('oper_name', VARCHAR(200), nullable=False)
)


t_view_location = Table(
    'view_location', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('locname', VARCHAR(200), nullable=False),
    Column('locinfo', VARCHAR(2000)),
    Column('locsize', NUMBER(asdecimal=False), nullable=False),
    Column('locsizename', VARCHAR(200), nullable=False),
    Column('locsizeinfo', VARCHAR(2000))
)


t_view_mn_operators = Table(
    'view_mn_operators', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('created', DateTime, nullable=False),
    Column('opname', VARCHAR(200), nullable=False),
    Column('opinfo', VARCHAR(2000)),
    Column('mcc', VARCHAR(3), nullable=False),
    Column('mnc', VARCHAR(3), nullable=False),
    Column('countryid', NUMBER(asdecimal=False)),
    Column('countryname', VARCHAR(200))
)


t_view_parkabon = Table(
    'view_parkabon', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('created', DateTime, nullable=False),
    Column('client_id', NUMBER(asdecimal=False), nullable=False),
    Column('regnum', VARCHAR(32), nullable=False),
    Column('vehicenum', VARCHAR(16), nullable=False),
    Column('activefrom', DateTime, nullable=False),
    Column('activetill', DateTime, nullable=False),
    Column('period_id', NUMBER(asdecimal=False), nullable=False),
    Column('periodname', VARCHAR(128), nullable=False)
)


t_view_parkbillzone = Table(
    'view_parkbillzone', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('pzonename', VARCHAR(200), nullable=False),
    Column('pzoneinfo', VARCHAR(1000)),
    Column('defaultcost', NUMBER(asdecimal=False), nullable=False),
    Column('defcurrencyid', NUMBER(asdecimal=False)),
    Column('currcode', VARCHAR(3), nullable=False)
)


t_view_parkcardquery = Table(
    'view_parkcardquery', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('client_id', NUMBER(asdecimal=False), nullable=False),
    Column('account_id', NUMBER(asdecimal=False), nullable=False),
    Column('face_number', VARCHAR(64)),
    Column('info', VARCHAR(1000)),
    Column('rec_code_assigned', DateTime),
    Column('cardtype', NUMBER(asdecimal=False), nullable=False),
    Column('cardtypecode', VARCHAR(64), nullable=False),
    Column('state', NUMBER(asdecimal=False), nullable=False),
    Column('accfileid', NUMBER(asdecimal=False), nullable=False),
    Column('vgroupid', NUMBER(asdecimal=False), nullable=False),
    Column('activated', DateTime),
    Column('opstate', NUMBER(asdecimal=False)),
    Column('state_code', VARCHAR(32), nullable=False),
    Column('state_info', VARCHAR(512)),
    Column('balance', NUMBER(asdecimal=False), nullable=False),
    Column('currcode', VARCHAR(3), nullable=False),
    Column('clientname', VARCHAR(200)),
    Column('clientnameup', VARCHAR(200)),
    Column('acfname', VARCHAR(128), nullable=False),
    Column('groupname', VARCHAR(200), nullable=False)
)


t_view_parking = Table(
    'view_parking', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('vgroupid', NUMBER(asdecimal=False), nullable=False),
    Column('externalid', VARCHAR(64), nullable=False),
    Column('parkname', VARCHAR(512)),
    Column('parkaddress', VARCHAR(1024)),
    Column('parkspace', NUMBER(asdecimal=False)),
    Column('parktypeid', NUMBER(asdecimal=False), nullable=False),
    Column('contactpersonid', NUMBER(asdecimal=False)),
    Column('workschedule', VARCHAR(1024)),
    Column('parkbillzoneid', NUMBER(asdecimal=False), nullable=False),
    Column('rentcost', NUMBER(asdecimal=False)),
    Column('ptcode', VARCHAR(32), nullable=False),
    Column('ptinfo', VARCHAR(1000)),
    Column('pzonename', VARCHAR(200), nullable=False),
    Column('defaultcost', NUMBER(asdecimal=False), nullable=False),
    Column('defcurrencyid', NUMBER(asdecimal=False)),
    Column('currcode', VARCHAR(3), nullable=False)
)


t_view_parkprivclient = Table(
    'view_parkprivclient', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('created', DateTime, nullable=False),
    Column('registrant', VARCHAR(200), nullable=False),
    Column('ownerdname', VARCHAR(200), nullable=False),
    Column('regdocinfo', VARCHAR(200), nullable=False),
    Column('vehiclenumber', VARCHAR(16), nullable=False),
    Column('orderdocno', VARCHAR(64), nullable=False),
    Column('expired', DateTime),
    Column('info', VARCHAR(1000)),
    Column('ownerdnameup', VARCHAR(200), nullable=False),
    Column('privtypeid', NUMBER(asdecimal=False), nullable=False),
    Column('privpersonid', NUMBER(asdecimal=False)),
    Column('reppersonid', NUMBER(asdecimal=False)),
    Column('insurancenumber', VARCHAR(32)),
    Column('vehiclemodel', VARCHAR(128)),
    Column('vehiclecolor', VARCHAR(128)),
    Column('lastupdate', DateTime),
    Column('prolongdate', DateTime),
    Column('canceldate', DateTime),
    Column('disperiodstart', DateTime),
    Column('disperiodend', DateTime),
    Column('disreview', DateTime),
    Column('pvtname', VARCHAR(200), nullable=False)
)


t_view_pms_company = Table(
    'view_pms_company', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('companyid', NUMBER(asdecimal=False), nullable=False),
    Column('vgroupid', NUMBER(asdecimal=False), nullable=False),
    Column('code', VARCHAR(32), nullable=False),
    Column('accountid', NUMBER(asdecimal=False), nullable=False),
    Column('daylimit', NUMBER(asdecimal=False), nullable=False),
    Column('workmode', CHAR(1), nullable=False),
    Column('onexcessaction', CHAR(1), nullable=False),
    Column('pstypeid', NUMBER(asdecimal=False), nullable=False),
    Column('billconfig', VARCHAR(2000)),
    Column('isalarm', NUMBER(asdecimal=False)),
    Column('commissionprc', NUMBER(asdecimal=False), nullable=False),
    Column('commissionflag', NUMBER(asdecimal=False), nullable=False),
    Column('pstypecode', VARCHAR(32), nullable=False),
    Column('pstypename', VARCHAR(256), nullable=False),
    Column('comp_name', VARCHAR(256), nullable=False),
    Column('comp_info', VARCHAR(4000)),
    Column('vgroupname', VARCHAR(200), nullable=False),
    Column('accountbalance', NUMBER(asdecimal=False), nullable=False),
    Column('currcode', VARCHAR(3), nullable=False)
)


t_view_prodpack_usage = Table(
    'view_prodpack_usage', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('subsid', NUMBER(asdecimal=False), nullable=False),
    Column('packageid', NUMBER(asdecimal=False), nullable=False),
    Column('corpitem', NUMBER(asdecimal=False), nullable=False),
    Column('cardid', NUMBER(asdecimal=False)),
    Column('usagestart', DateTime),
    Column('usagevalue', NUMBER(asdecimal=False), nullable=False),
    Column('lastusagereset', DateTime),
    Column('totalvalue', NUMBER(asdecimal=False), nullable=False),
    Column('usageresetnumber', NUMBER(asdecimal=False), nullable=False),
    Column('measureunit', NUMBER(asdecimal=False), nullable=False),
    Column('measureunitcode', VARCHAR(32), nullable=False),
    Column('billvolname', VARCHAR(200), nullable=False),
    Column('packagename', VARCHAR(128), nullable=False),
    Column('billservice', NUMBER(asdecimal=False), nullable=False),
    Column('totalvolume', NUMBER(asdecimal=False)),
    Column('billvolumeid', NUMBER(asdecimal=False), nullable=False),
    Column('bname', VARCHAR(256))
)


t_view_product_activation_code = Table(
    'view_product_activation_code', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('activation_code', VARCHAR(200), nullable=False),
    Column('partition', VARCHAR(1000), nullable=False),
    Column('productid', NUMBER(asdecimal=False), nullable=False),
    Column('generated_dt', DateTime, nullable=False),
    Column('expired_dt', DateTime),
    Column('used_dt', DateTime),
    Column('state', NUMBER(asdecimal=False), nullable=False),
    Column('iteration_num', NUMBER(asdecimal=False), nullable=False),
    Column('state_code', VARCHAR(200), nullable=False),
    Column('prodname', VARCHAR(256), nullable=False),
    Column('vgroupid', NUMBER(asdecimal=False), nullable=False)
)


t_view_product_using = Table(
    'view_product_using', metadata,
    Column('product_id', NUMBER(asdecimal=False), nullable=False),
    Column('accfileid', NUMBER(asdecimal=False)),
    Column('name', VARCHAR(128), nullable=False),
    Column('ordered', NUMBER(asdecimal=False)),
    Column('active', NUMBER(asdecimal=False)),
    Column('ended', NUMBER(asdecimal=False)),
    Column('vgroupid', NUMBER(asdecimal=False))
)


t_view_products = Table(
    'view_products', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('vgroupid', NUMBER(asdecimal=False), nullable=False),
    Column('prodcode', VARCHAR(64), nullable=False),
    Column('ordercode', VARCHAR(64)),
    Column('prodname', VARCHAR(256), nullable=False),
    Column('prodinfo', VARCHAR(1024)),
    Column('prodtypeid', NUMBER(asdecimal=False), nullable=False),
    Column('currencyid', NUMBER(asdecimal=False), nullable=False),
    Column('payment_schema_id', NUMBER(asdecimal=False)),
    Column('smprodnumber', NUMBER(asdecimal=False), nullable=False),
    Column('billserviceid', NUMBER(asdecimal=False)),
    Column('initprovstate', NUMBER(asdecimal=False), nullable=False),
    Column('provrequired', NUMBER(asdecimal=False), nullable=False),
    Column('config', VARCHAR(4000)),
    Column('userstatementflag', NUMBER(asdecimal=False), nullable=False),
    Column('incomeaccreport', NUMBER(asdecimal=False), nullable=False),
    Column('enable_on_restricted_card', NUMBER(asdecimal=False)),
    Column('change_prov_on_restricted', NUMBER(asdecimal=False)),
    Column('autorenewwithtrafficend', NUMBER(asdecimal=False)),
    Column('deleted', DateTime),
    Column('provifcardnotactivated', NUMBER(asdecimal=False)),
    Column('prodtypename', VARCHAR(512), nullable=False),
    Column('prodtypeinfo', VARCHAR(4000)),
    Column('servicecode', VARCHAR(64)),
    Column('serviceinfo', VARCHAR(1024)),
    Column('currcode', VARCHAR(3), nullable=False),
    Column('ordercost', NUMBER(asdecimal=False), nullable=False),
    Column('noordercostonacfchange', NUMBER(asdecimal=False))
)


t_view_reportfiles = Table(
    'view_reportfiles', metadata,
    Column('nid', NUMBER(asdecimal=False), nullable=False),
    Column('dcreated', DateTime, nullable=False),
    Column('fullpath', VARCHAR(1024), nullable=False),
    Column('displayname', VARCHAR(256)),
    Column('reportid', NUMBER(asdecimal=False), nullable=False),
    Column('filetitle', VARCHAR(256)),
    Column('filesize', NUMBER(asdecimal=False), nullable=False),
    Column('txcreated', VARCHAR(19))
)


t_view_sgsn = Table(
    'view_sgsn', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('created', DateTime, nullable=False),
    Column('operid', NUMBER(asdecimal=False), nullable=False),
    Column('sgsn', VARCHAR(128), nullable=False),
    Column('netmask', NUMBER(asdecimal=False), nullable=False),
    Column('subnet', NUMBER(asdecimal=False), nullable=False),
    Column('minip', NUMBER(asdecimal=False), nullable=False),
    Column('maxip', NUMBER(asdecimal=False), nullable=False),
    Column('info', VARCHAR(2048)),
    Column('opname', VARCHAR(200), nullable=False),
    Column('mcc', VARCHAR(3), nullable=False),
    Column('mnc', VARCHAR(3), nullable=False),
    Column('countryname', VARCHAR(200))
)


t_view_sgsngroup = Table(
    'view_sgsngroup', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('grname', VARCHAR(200), nullable=False),
    Column('grinfo', VARCHAR(2000)),
    Column('grsize', NUMBER(asdecimal=False), nullable=False),
    Column('locsizename', VARCHAR(200), nullable=False),
    Column('locsizeinfo', VARCHAR(2000))
)


t_view_simact_detailed_report = Table(
    'view_simact_detailed_report', metadata,
    Column('cardid', NUMBER(asdecimal=False), nullable=False),
    Column('actdate', DateTime),
    Column('firsttransaction', DateTime),
    Column('dealerid', NUMBER(asdecimal=False)),
    Column('factsellerid', NUMBER(asdecimal=False)),
    Column('saled', DateTime),
    Column('shipped', DateTime),
    Column('cardfacevalue', NUMBER(asdecimal=False)),
    Column('accfileid', NUMBER(asdecimal=False), nullable=False),
    Column('cardnumber', VARCHAR(64), nullable=False),
    Column('iccid', VARCHAR(32), nullable=False),
    Column('account_id', NUMBER(asdecimal=False), nullable=False),
    Column('msisdn', VARCHAR(32)),
    Column('d_msisdn', VARCHAR(32)),
    Column('imsi', VARCHAR(64), nullable=False),
    Column('clientname', VARCHAR(200)),
    Column('dealercompany', VARCHAR(256), nullable=False),
    Column('sellercompany', VARCHAR(256)),
    Column('acfname', VARCHAR(128), nullable=False),
    Column('vgroupid', NUMBER(asdecimal=False)),
    Column('regdate', DateTime)
)


t_view_simcard_all = Table(
    'view_simcard_all', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('imsi', VARCHAR(64), nullable=False),
    Column('account', NUMBER(asdecimal=False), nullable=False),
    Column('client', NUMBER(asdecimal=False)),
    Column('contract', NUMBER(asdecimal=False)),
    Column('pin1', VARCHAR(16)),
    Column('pin2', VARCHAR(16)),
    Column('puk1', VARCHAR(16)),
    Column('puk2', VARCHAR(16)),
    Column('iccid', VARCHAR(32), nullable=False),
    Column('imei', VARCHAR(32)),
    Column('cardid', NUMBER(asdecimal=False), nullable=False),
    Column('corpgroupid', NUMBER(asdecimal=False)),
    Column('msisdn', VARCHAR(32)),
    Column('old_msisdn', VARCHAR(32)),
    Column('immortal', NUMBER(asdecimal=False)),
    Column('user_name', VARCHAR(300)),
    Column('clientchangedate', DateTime),
    Column('tariff_version', NUMBER(asdecimal=False)),
    Column('cust_private_num', VARCHAR(64)),
    Column('sim_type', VARCHAR(32)),
    Column('sim_vendor', VARCHAR(64)),
    Column('sim_espec', VARCHAR(32)),
    Column('app_vendor', VARCHAR(64)),
    Column('app_version', VARCHAR(64)),
    Column('sim_actcode', VARCHAR(256)),
    Column('d_msisdn', VARCHAR(32)),
    Column('cardtype', NUMBER(asdecimal=False), nullable=False),
    Column('vgroupid', NUMBER(asdecimal=False), nullable=False),
    Column('accfileid', NUMBER(asdecimal=False), nullable=False),
    Column('cardstate', NUMBER(asdecimal=False), nullable=False),
    Column('opcardstate', NUMBER(asdecimal=False)),
    Column('opcardstatecode', VARCHAR(32), nullable=False),
    Column('opcardstateinfo', VARCHAR(512)),
    Column('activefrom', DateTime),
    Column('expired', DateTime),
    Column('activated', DateTime),
    Column('firsttransaction', DateTime),
    Column('lang', NUMBER(asdecimal=False)),
    Column('seriesid', NUMBER(asdecimal=False)),
    Column('lastacfchangedate', DateTime),
    Column('basecard_info', VARCHAR(1024)),
    Column('vgroupname', VARCHAR(200), nullable=False),
    Column('accfilename', VARCHAR(128), nullable=False),
    Column('accfilecode', VARCHAR(32), nullable=False),
    Column('clientname', VARCHAR(200)),
    Column('billmode_id', NUMBER(asdecimal=False)),
    Column('bill_mode_name', VARCHAR(16)),
    Column('clienttypename', VARCHAR(128)),
    Column('clientprepaid', NUMBER(asdecimal=False)),
    Column('deleted', NUMBER(asdecimal=False)),
    Column('ip_address', NUMBER(asdecimal=False)),
    Column('vpn_id', NUMBER(asdecimal=False)),
    Column('group_id', NUMBER(asdecimal=False))
)


t_view_simcard_base = Table(
    'view_simcard_base', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('imsi', VARCHAR(64), nullable=False),
    Column('account', NUMBER(asdecimal=False), nullable=False),
    Column('client', NUMBER(asdecimal=False)),
    Column('contract', NUMBER(asdecimal=False)),
    Column('pin1', VARCHAR(16)),
    Column('pin2', VARCHAR(16)),
    Column('puk1', VARCHAR(16)),
    Column('puk2', VARCHAR(16)),
    Column('iccid', VARCHAR(32), nullable=False),
    Column('imei', VARCHAR(32)),
    Column('cardid', NUMBER(asdecimal=False), nullable=False),
    Column('corpgroupid', NUMBER(asdecimal=False)),
    Column('msisdn', VARCHAR(32)),
    Column('old_msisdn', VARCHAR(32)),
    Column('immortal', NUMBER(asdecimal=False)),
    Column('user_name', VARCHAR(300)),
    Column('clientchangedate', DateTime),
    Column('tariff_version', NUMBER(asdecimal=False)),
    Column('cust_private_num', VARCHAR(64)),
    Column('sim_type', VARCHAR(32)),
    Column('sim_vendor', VARCHAR(64)),
    Column('sim_espec', VARCHAR(32)),
    Column('app_vendor', VARCHAR(64)),
    Column('app_version', VARCHAR(64)),
    Column('sim_actcode', VARCHAR(256)),
    Column('d_msisdn', VARCHAR(32)),
    Column('cardtype', NUMBER(asdecimal=False), nullable=False),
    Column('vgroupid', NUMBER(asdecimal=False), nullable=False),
    Column('accfileid', NUMBER(asdecimal=False), nullable=False),
    Column('cardstate', NUMBER(asdecimal=False), nullable=False),
    Column('opcardstate', NUMBER(asdecimal=False)),
    Column('opcardstatecode', VARCHAR(32), nullable=False),
    Column('opcardstateinfo', VARCHAR(512)),
    Column('activefrom', DateTime),
    Column('expired', DateTime),
    Column('activated', DateTime),
    Column('firsttransaction', DateTime),
    Column('lang', NUMBER(asdecimal=False)),
    Column('seriesid', NUMBER(asdecimal=False)),
    Column('lastacfchangedate', DateTime),
    Column('basecard_info', VARCHAR(1024)),
    Column('vgroupname', VARCHAR(200), nullable=False),
    Column('accfilename', VARCHAR(128), nullable=False),
    Column('accfilecode', VARCHAR(32), nullable=False),
    Column('clientname', VARCHAR(200)),
    Column('billmode_id', NUMBER(asdecimal=False)),
    Column('bill_mode_name', VARCHAR(16)),
    Column('clienttypename', VARCHAR(128)),
    Column('clientprepaid', NUMBER(asdecimal=False)),
    Column('deleted', NUMBER(asdecimal=False)),
    Column('ip_address', NUMBER(asdecimal=False)),
    Column('vpn_id', NUMBER(asdecimal=False)),
    Column('group_id', NUMBER(asdecimal=False))
)


t_view_simcard_by_number = Table(
    'view_simcard_by_number', metadata,
    Column('pnumber', VARCHAR(32), nullable=False),
    Column('numbertype', NUMBER(asdecimal=False), nullable=False),
    Column('numstate', NUMBER(asdecimal=False)),
    Column('simcardid', NUMBER(asdecimal=False)),
    Column('imsi', VARCHAR(64), nullable=False),
    Column('msisdn', VARCHAR(32)),
    Column('d_msisdn', VARCHAR(32)),
    Column('account', NUMBER(asdecimal=False), nullable=False),
    Column('client', NUMBER(asdecimal=False)),
    Column('iccid', VARCHAR(32), nullable=False),
    Column('immortal', NUMBER(asdecimal=False)),
    Column('cardtype', NUMBER(asdecimal=False), nullable=False),
    Column('opcardstate', NUMBER(asdecimal=False)),
    Column('opcardstatecode', VARCHAR(32), nullable=False),
    Column('vgroupid', NUMBER(asdecimal=False), nullable=False),
    Column('accfileid', NUMBER(asdecimal=False), nullable=False),
    Column('cardstate', NUMBER(asdecimal=False), nullable=False),
    Column('activefrom', DateTime),
    Column('expired', DateTime),
    Column('activated', DateTime),
    Column('firsttransaction', DateTime),
    Column('lang', NUMBER(asdecimal=False)),
    Column('lastacfchangedate', DateTime)
)


t_view_simcard_cab = Table(
    'view_simcard_cab', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('imsi', VARCHAR(64), nullable=False),
    Column('imei', VARCHAR(32)),
    Column('account', NUMBER(asdecimal=False), nullable=False),
    Column('client', NUMBER(asdecimal=False)),
    Column('contract', NUMBER(asdecimal=False)),
    Column('msisdn', VARCHAR(32)),
    Column('user_name', VARCHAR(300)),
    Column('d_msisdn', VARCHAR(32)),
    Column('iccid', VARCHAR(32), nullable=False),
    Column('balance', NUMBER(asdecimal=False), nullable=False),
    Column('currcode', VARCHAR(3), nullable=False),
    Column('cardtype', NUMBER(asdecimal=False), nullable=False),
    Column('vgroupid', NUMBER(asdecimal=False), nullable=False),
    Column('accfileid', NUMBER(asdecimal=False), nullable=False),
    Column('cardstate', NUMBER(asdecimal=False), nullable=False),
    Column('opcardstate', NUMBER(asdecimal=False)),
    Column('opcardstatecode', VARCHAR(32), nullable=False),
    Column('opcardstateinfo', VARCHAR(512)),
    Column('vgroupname', VARCHAR(200), nullable=False),
    Column('accfilename', VARCHAR(128), nullable=False),
    Column('clientname', VARCHAR(200), nullable=False),
    Column('deleted', NUMBER(asdecimal=False)),
    Column('cardgroupname', VARCHAR(200)),
    Column('card_group_id', NUMBER(asdecimal=False)),
    Column('last_activity', DateTime),
    Column('avg_time_minutes', NUMBER(asdecimal=False)),
    Column('ip_address', NUMBER(asdecimal=False)),
    Column('vpn_id', NUMBER(asdecimal=False))
)


t_view_simcard_deleted = Table(
    'view_simcard_deleted', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('imsi', VARCHAR(64), nullable=False),
    Column('account', NUMBER(asdecimal=False), nullable=False),
    Column('client', NUMBER(asdecimal=False)),
    Column('contract', NUMBER(asdecimal=False)),
    Column('pin1', VARCHAR(16)),
    Column('pin2', VARCHAR(16)),
    Column('puk1', VARCHAR(16)),
    Column('puk2', VARCHAR(16)),
    Column('iccid', VARCHAR(32), nullable=False),
    Column('imei', VARCHAR(32)),
    Column('cardid', NUMBER(asdecimal=False), nullable=False),
    Column('corpgroupid', NUMBER(asdecimal=False)),
    Column('msisdn', VARCHAR(32)),
    Column('old_msisdn', VARCHAR(32)),
    Column('immortal', NUMBER(asdecimal=False)),
    Column('user_name', VARCHAR(300)),
    Column('clientchangedate', DateTime),
    Column('tariff_version', NUMBER(asdecimal=False)),
    Column('cust_private_num', VARCHAR(64)),
    Column('sim_type', VARCHAR(32)),
    Column('sim_vendor', VARCHAR(64)),
    Column('sim_espec', VARCHAR(32)),
    Column('app_vendor', VARCHAR(64)),
    Column('app_version', VARCHAR(64)),
    Column('sim_actcode', VARCHAR(256)),
    Column('d_msisdn', VARCHAR(32)),
    Column('cardtype', NUMBER(asdecimal=False), nullable=False),
    Column('vgroupid', NUMBER(asdecimal=False), nullable=False),
    Column('accfileid', NUMBER(asdecimal=False), nullable=False),
    Column('cardstate', NUMBER(asdecimal=False), nullable=False),
    Column('opcardstate', NUMBER(asdecimal=False)),
    Column('opcardstatecode', VARCHAR(32), nullable=False),
    Column('opcardstateinfo', VARCHAR(512)),
    Column('activefrom', DateTime),
    Column('expired', DateTime),
    Column('activated', DateTime),
    Column('firsttransaction', DateTime),
    Column('lang', NUMBER(asdecimal=False)),
    Column('seriesid', NUMBER(asdecimal=False)),
    Column('lastacfchangedate', DateTime),
    Column('basecard_info', VARCHAR(1024)),
    Column('vgroupname', VARCHAR(200), nullable=False),
    Column('accfilename', VARCHAR(128), nullable=False),
    Column('accfilecode', VARCHAR(32), nullable=False),
    Column('clientname', VARCHAR(200)),
    Column('billmode_id', NUMBER(asdecimal=False)),
    Column('bill_mode_name', VARCHAR(16)),
    Column('clienttypename', VARCHAR(128)),
    Column('clientprepaid', NUMBER(asdecimal=False)),
    Column('deleted', NUMBER(asdecimal=False)),
    Column('ip_address', NUMBER(asdecimal=False)),
    Column('vpn_id', NUMBER(asdecimal=False)),
    Column('group_id', NUMBER(asdecimal=False))
)


t_view_simcard_search = Table(
    'view_simcard_search', metadata,
    Column('simcardid', NUMBER(asdecimal=False), nullable=False),
    Column('imsi', VARCHAR(64), nullable=False),
    Column('msisdn', VARCHAR(32)),
    Column('d_msisdn', VARCHAR(32)),
    Column('account', NUMBER(asdecimal=False), nullable=False),
    Column('client', NUMBER(asdecimal=False)),
    Column('iccid', VARCHAR(32), nullable=False),
    Column('cardtype', NUMBER(asdecimal=False), nullable=False),
    Column('opcardstate', NUMBER(asdecimal=False)),
    Column('opcardstatecode', VARCHAR(32), nullable=False),
    Column('vgroupid', NUMBER(asdecimal=False), nullable=False),
    Column('accfileid', NUMBER(asdecimal=False), nullable=False),
    Column('cardstate', NUMBER(asdecimal=False), nullable=False),
    Column('activefrom', DateTime),
    Column('expired', DateTime),
    Column('activated', DateTime),
    Column('firsttransaction', DateTime),
    Column('lang', NUMBER(asdecimal=False)),
    Column('lastacfchangedate', DateTime)
)


t_view_simnumber = Table(
    'view_simnumber', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('pnumber', VARCHAR(32), nullable=False),
    Column('simcardid', NUMBER(asdecimal=False)),
    Column('numbertype', NUMBER(asdecimal=False), nullable=False),
    Column('norder', NUMBER(asdecimal=False), nullable=False),
    Column('nstate', NUMBER(asdecimal=False)),
    Column('released', DateTime),
    Column('rate_id', NUMBER(asdecimal=False), nullable=False),
    Column('vgroup_id', NUMBER(asdecimal=False), nullable=False),
    Column('own_type', CHAR(3), nullable=False),
    Column('operstate', NUMBER(asdecimal=False), nullable=False),
    Column('last_update', DateTime),
    Column('numtypecode', VARCHAR(32), nullable=False),
    Column('rate_name', VARCHAR(100), nullable=False),
    Column('rate_level', NUMBER(asdecimal=False), nullable=False),
    Column('rate_cost', NUMBER(asdecimal=False), nullable=False),
    Column('currency_id', NUMBER(asdecimal=False), nullable=False),
    Column('currcode', VARCHAR(3), nullable=False),
    Column('groupname', VARCHAR(200), nullable=False),
    Column('numstatecode', VARCHAR(16), nullable=False)
)


t_view_simnumberrate = Table(
    'view_simnumberrate', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('vgroup_id', NUMBER(asdecimal=False), nullable=False),
    Column('created', DateTime, nullable=False),
    Column('rate_level', NUMBER(asdecimal=False), nullable=False),
    Column('rate_name', VARCHAR(100), nullable=False),
    Column('rate_info', VARCHAR(1000)),
    Column('rate_cost', NUMBER(asdecimal=False), nullable=False),
    Column('currency_id', NUMBER(asdecimal=False), nullable=False),
    Column('currcode', VARCHAR(3), nullable=False)
)


t_view_simreplacementpool = Table(
    'view_simreplacementpool', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('vgroupid', NUMBER(asdecimal=False), nullable=False),
    Column('imsi', VARCHAR(64), nullable=False),
    Column('icc', VARCHAR(64), nullable=False),
    Column('created', DateTime, nullable=False),
    Column('userid', NUMBER(asdecimal=False), nullable=False),
    Column('pin1', VARCHAR(16)),
    Column('pin2', VARCHAR(16)),
    Column('puk1', VARCHAR(16)),
    Column('puk2', VARCHAR(16)),
    Column('client_id', NUMBER(asdecimal=False)),
    Column('clientname', VARCHAR(200)),
    Column('clientname_up', VARCHAR(200))
)


t_view_tariff_call = Table(
    'view_tariff_call', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('planscheduleid', NUMBER(asdecimal=False), nullable=False),
    Column('locid', NUMBER(asdecimal=False), nullable=False),
    Column('bzoneid', NUMBER(asdecimal=False), nullable=False),
    Column('billserviceid', NUMBER(asdecimal=False), nullable=False),
    Column('modrulea', VARCHAR(64)),
    Column('modruleb', VARCHAR(64)),
    Column('tariffid', NUMBER(asdecimal=False), nullable=False),
    Column('redirectmode', CHAR(1), nullable=False),
    Column('homesubsmode', CHAR(1), nullable=False),
    Column('vgschedid', NUMBER(asdecimal=False)),
    Column('dirname', VARCHAR(64), nullable=False),
    Column('locname', VARCHAR(200), nullable=False),
    Column('locsizeinfo', VARCHAR(2000)),
    Column('bzonename', VARCHAR(256), nullable=False),
    Column('vgschedname', VARCHAR(200)),
    Column('adminstate', NUMBER(asdecimal=False)),
    Column('basevolumecost', NUMBER(asdecimal=False)),
    Column('billservice', NUMBER(asdecimal=False), nullable=False),
    Column('basevolname', VARCHAR(200), nullable=False),
    Column('currcode', VARCHAR(3), nullable=False),
    Column('tariffname', VARCHAR(256)),
    Column('tariffdata', VARCHAR(4000))
)


t_view_tariff_extsrv = Table(
    'view_tariff_extsrv', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('planscheduleid', NUMBER(asdecimal=False), nullable=False),
    Column('extserviceid', NUMBER(asdecimal=False), nullable=False),
    Column('tariffid', NUMBER(asdecimal=False), nullable=False),
    Column('adminstate', NUMBER(asdecimal=False)),
    Column('basevolumecost', NUMBER(asdecimal=False)),
    Column('billservice', NUMBER(asdecimal=False), nullable=False),
    Column('basevolname', VARCHAR(200), nullable=False),
    Column('currcode', VARCHAR(3), nullable=False),
    Column('tariffname', VARCHAR(256)),
    Column('esrvcode', VARCHAR(32), nullable=False),
    Column('esrvinfo', VARCHAR(1024)),
    Column('escompany', VARCHAR(256)),
    Column('companyid', NUMBER(asdecimal=False))
)


t_view_tariff_gprs = Table(
    'view_tariff_gprs', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('planscheduleid', NUMBER(asdecimal=False), nullable=False),
    Column('accpointid', NUMBER(asdecimal=False), nullable=False),
    Column('operatorid', NUMBER(asdecimal=False), nullable=False),
    Column('sgsngroupid', NUMBER(asdecimal=False), nullable=False),
    Column('tariffid', NUMBER(asdecimal=False), nullable=False),
    Column('vgschedid', NUMBER(asdecimal=False)),
    Column('adminstate', NUMBER(asdecimal=False)),
    Column('basevolumecost', NUMBER(asdecimal=False)),
    Column('billservice', NUMBER(asdecimal=False), nullable=False),
    Column('apcode', VARCHAR(32), nullable=False),
    Column('opname', VARCHAR(200), nullable=False),
    Column('grname', VARCHAR(200), nullable=False),
    Column('grsizeinfo', VARCHAR(2000)),
    Column('vgschedname', VARCHAR(200)),
    Column('basevolname', VARCHAR(200), nullable=False),
    Column('currcode', VARCHAR(3), nullable=False),
    Column('tariffname', VARCHAR(256))
)


t_view_tariff_gprs2 = Table(
    'view_tariff_gprs2', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('planscheduleid', NUMBER(asdecimal=False), nullable=False),
    Column('accpointid', NUMBER(asdecimal=False), nullable=False),
    Column('locid', NUMBER(asdecimal=False), nullable=False),
    Column('tariffid', NUMBER(asdecimal=False), nullable=False),
    Column('vgschedid', NUMBER(asdecimal=False)),
    Column('adminstate', NUMBER(asdecimal=False)),
    Column('basevolumecost', NUMBER(asdecimal=False)),
    Column('billservice', NUMBER(asdecimal=False), nullable=False),
    Column('apcode', VARCHAR(32), nullable=False),
    Column('locname', VARCHAR(200), nullable=False),
    Column('sizeinfo', VARCHAR(2000)),
    Column('vgschedname', VARCHAR(200)),
    Column('basevolname', VARCHAR(200), nullable=False),
    Column('currcode', VARCHAR(3), nullable=False),
    Column('tariffname', VARCHAR(256))
)


t_view_tariff_location = Table(
    'view_tariff_location', metadata,
    Column('locid', NUMBER(asdecimal=False), nullable=False),
    Column('operid', NUMBER(asdecimal=False), nullable=False),
    Column('vlrid', NUMBER(asdecimal=False), nullable=False),
    Column('countryid', NUMBER(asdecimal=False), nullable=False)
)


t_view_tariff_park = Table(
    'view_tariff_park', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('planscheduleid', NUMBER(asdecimal=False), nullable=False),
    Column('parkzoneid', NUMBER(asdecimal=False), nullable=False),
    Column('tariffid', NUMBER(asdecimal=False), nullable=False),
    Column('pzonename', VARCHAR(200), nullable=False),
    Column('adminstate', NUMBER(asdecimal=False)),
    Column('basevolumecost', NUMBER(asdecimal=False)),
    Column('billservice', NUMBER(asdecimal=False), nullable=False),
    Column('basevolname', VARCHAR(200), nullable=False),
    Column('currcode', VARCHAR(3), nullable=False),
    Column('tariffname', VARCHAR(256)),
    Column('defzonecost', NUMBER(asdecimal=False), nullable=False),
    Column('defzonecurrcode', VARCHAR(3), nullable=False)
)


t_view_tariff_sms = Table(
    'view_tariff_sms', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('planscheduleid', NUMBER(asdecimal=False), nullable=False),
    Column('locid', NUMBER(asdecimal=False), nullable=False),
    Column('bzoneid', NUMBER(asdecimal=False), nullable=False),
    Column('tariffid', NUMBER(asdecimal=False), nullable=False),
    Column('homesubsmode', CHAR(1), nullable=False),
    Column('vgschedid', NUMBER(asdecimal=False)),
    Column('locname', VARCHAR(200), nullable=False),
    Column('locsizeinfo', VARCHAR(2000)),
    Column('bzonename', VARCHAR(256), nullable=False),
    Column('vgschedname', VARCHAR(200)),
    Column('adminstate', NUMBER(asdecimal=False)),
    Column('basevolumecost', NUMBER(asdecimal=False)),
    Column('billservice', NUMBER(asdecimal=False), nullable=False),
    Column('basevolname', VARCHAR(200), nullable=False),
    Column('currcode', VARCHAR(3), nullable=False),
    Column('tariffname', VARCHAR(256))
)


t_view_tariff_zone = Table(
    'view_tariff_zone', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('schemaid', NUMBER(asdecimal=False), nullable=False),
    Column('tzname', VARCHAR(256), nullable=False),
    Column('tzinfo', VARCHAR(2000)),
    Column('rsname', VARCHAR(256), nullable=False)
)


t_view_tariff_zone_directions = Table(
    'view_tariff_zone_directions', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('zoneid', NUMBER(asdecimal=False)),
    Column('schemaid', NUMBER(asdecimal=False), nullable=False),
    Column('prefix', VARCHAR(64), nullable=False),
    Column('numlength', NUMBER(asdecimal=False), nullable=False),
    Column('adminstate', NUMBER(asdecimal=False), nullable=False),
    Column('dirname', VARCHAR(200), nullable=False),
    Column('created', DateTime, nullable=False),
    Column('isexclude', NUMBER(asdecimal=False)),
    Column('rsname', VARCHAR(256), nullable=False),
    Column('tzname', VARCHAR(256))
)


t_view_tariffplan = Table(
    'view_tariffplan', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('billtype', NUMBER(asdecimal=False), nullable=False),
    Column('planname', VARCHAR(256)),
    Column('planinfo', VARCHAR(1024)),
    Column('created', DateTime),
    Column('plancode', VARCHAR(64)),
    Column('currencyid', NUMBER(asdecimal=False)),
    Column('vgroupid', NUMBER(asdecimal=False)),
    Column('billtypename', VARCHAR(128)),
    Column('currcode', VARCHAR(3), nullable=False),
    Column('vgname', VARCHAR(200)),
    Column('acfnumber', NUMBER(asdecimal=False)),
    Column('prodpckgsnumber', NUMBER(asdecimal=False)),
    Column('planservices', VARCHAR(4000))
)


t_view_tplan_services = Table(
    'view_tplan_services', metadata,
    Column('planid', NUMBER(asdecimal=False), nullable=False),
    Column('billservice', NUMBER(asdecimal=False), nullable=False),
    Column('code', VARCHAR(64))
)


t_view_userlogin = Table(
    'view_userlogin', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('login', VARCHAR(64), nullable=False),
    Column('userrole', NUMBER(asdecimal=False), nullable=False),
    Column('vgroupid', NUMBER(asdecimal=False)),
    Column('personid', NUMBER(asdecimal=False)),
    Column('state', NUMBER(asdecimal=False), nullable=False),
    Column('created', DateTime, nullable=False),
    Column('info', VARCHAR(2000)),
    Column('targetcompanyid', NUMBER(asdecimal=False)),
    Column('rolename', VARCHAR(200), nullable=False),
    Column('roleinfo', VARCHAR(2000)),
    Column('state_code', VARCHAR(32), nullable=False),
    Column('userdisplayname', VARCHAR(200)),
    Column('userfullname', VARCHAR(386)),
    Column('useremail', VARCHAR(256)),
    Column('groupname', VARCHAR(200)),
    Column('targetcompanyname', VARCHAR(256))
)


t_view_ussdcommands = Table(
    'view_ussdcommands', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('commandid', NUMBER(asdecimal=False), nullable=False),
    Column('ussdmask', VARCHAR(128), nullable=False),
    Column('smsanswer', NUMBER(asdecimal=False), nullable=False),
    Column('vgroupid', NUMBER(asdecimal=False), nullable=False),
    Column('msgtext', VARCHAR(4000)),
    Column('defvalues', VARCHAR(1024)),
    Column('code', VARCHAR(32), nullable=False),
    Column('required_tags', VARCHAR(512)),
    Column('commandinfo', VARCHAR(1024)),
    Column('message_tags', VARCHAR(512))
)


t_view_virtualgroup = Table(
    'view_virtualgroup', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('created', DateTime, nullable=False),
    Column('groupname', VARCHAR(200), nullable=False),
    Column('groupinfo', VARCHAR(4000)),
    Column('registrant', VARCHAR(512)),
    Column('ownercompany', NUMBER(asdecimal=False), nullable=False),
    Column('alignsubstime', NUMBER(asdecimal=False)),
    Column('denyfreeacfchangeperiod', NUMBER(asdecimal=False)),
    Column('simnumberreldays', NUMBER(asdecimal=False)),
    Column('lfeepredictioninterval', NUMBER(asdecimal=False)),
    Column('smssenderaddress', VARCHAR(64)),
    Column('defaultaccfileid', NUMBER(asdecimal=False)),
    Column('defcurrencyid', NUMBER(asdecimal=False)),
    Column('emailsenderaddress', VARCHAR(255)),
    Column('percentdurationforalignlicfee', NUMBER(asdecimal=False)),
    Column('carddeletionmode', NUMBER(asdecimal=False), nullable=False),
    Column('sms_schedule', VARCHAR(100)),
    Column('ntfbsnomoneycooldowntime', VARCHAR(200)),
    Column('ntfppackpercentthrshlds', VARCHAR(200)),
    Column('ownercompname', VARCHAR(256), nullable=False),
    Column('currcode', VARCHAR(3), nullable=False)
)


t_view_vlr = Table(
    'view_vlr', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('created', DateTime, nullable=False),
    Column('operid', NUMBER(asdecimal=False), nullable=False),
    Column('vlrprefix', VARCHAR(32), nullable=False),
    Column('vlrinfo', VARCHAR(1000)),
    Column('opname', VARCHAR(200), nullable=False)
)


t_view_voucher_card = Table(
    'view_voucher_card', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('cardtype', NUMBER(asdecimal=False), nullable=False),
    Column('vgroupid', NUMBER(asdecimal=False), nullable=False),
    Column('accfileid', NUMBER(asdecimal=False), nullable=False),
    Column('created', DateTime, nullable=False),
    Column('state', NUMBER(asdecimal=False), nullable=False),
    Column('dealerid', NUMBER(asdecimal=False)),
    Column('comp_name', VARCHAR(256)),
    Column('emitentid', NUMBER(asdecimal=False)),
    Column('activefrom', DateTime),
    Column('expired', DateTime),
    Column('saled', DateTime),
    Column('activated', DateTime),
    Column('firsttransaction', DateTime),
    Column('seriesid', NUMBER(asdecimal=False)),
    Column('seriesnumber', NUMBER(asdecimal=False)),
    Column('cardnumber', VARCHAR(64), nullable=False),
    Column('opstate', NUMBER(asdecimal=False)),
    Column('opstatechangedate', DateTime),
    Column('factsellerid', NUMBER(asdecimal=False)),
    Column('shipped', DateTime),
    Column('shipmentuserid', NUMBER(asdecimal=False)),
    Column('shipmentuserinfo', VARCHAR(200)),
    Column('secret_code', VARCHAR(64), nullable=False),
    Column('money', NUMBER(asdecimal=False), nullable=False),
    Column('currency_id', NUMBER(asdecimal=False), nullable=False),
    Column('target_account_id', NUMBER(asdecimal=False)),
    Column('target_card_id', NUMBER(asdecimal=False)),
    Column('target_number', VARCHAR(64)),
    Column('currcode', VARCHAR(3), nullable=False),
    Column('opstatecode', VARCHAR(32), nullable=False),
    Column('is_deleted', NUMBER(asdecimal=False))
)


t_view_weblogin = Table(
    'view_weblogin', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('created', DateTime, nullable=False),
    Column('login', VARCHAR(32), nullable=False),
    Column('passwd', VARCHAR(64), nullable=False),
    Column('ext_role', NUMBER(asdecimal=False)),
    Column('client_id', NUMBER(asdecimal=False)),
    Column('approved', NUMBER(asdecimal=False), nullable=False),
    Column('last_change', DateTime),
    Column('last_passwd', VARCHAR(64)),
    Column('clientname', VARCHAR(200), nullable=False),
    Column('clientnameup', VARCHAR(200)),
    Column('cltypeinfo', VARCHAR(2000))
)


t_view_xgatelogin = Table(
    'view_xgatelogin', metadata,
    Column('id', NUMBER(asdecimal=False), nullable=False),
    Column('login', VARCHAR(64)),
    Column('groupid', NUMBER(asdecimal=False), nullable=False),
    Column('state', NUMBER(asdecimal=False)),
    Column('created', DateTime),
    Column('info', VARCHAR(2000)),
    Column('targetcompanyid', NUMBER(asdecimal=False)),
    Column('profileid', NUMBER(asdecimal=False)),
    Column('client_id', NUMBER(asdecimal=False)),
    Column('login_lcase', VARCHAR(64), nullable=False),
    Column('role_name', VARCHAR(128), nullable=False),
    Column('role_class', VARCHAR(64), nullable=False),
    Column('clientname', VARCHAR(200)),
    Column('clientname_up', VARCHAR(200)),
    Column('state_code', VARCHAR(32), nullable=False),
    Column('groupname', VARCHAR(200)),
    Column('profilename', VARCHAR(200)),
    Column('targetcompanyname', VARCHAR(256)),
    Column('role_scope_id', NUMBER(asdecimal=False)),
    Column('role_scope_code', VARCHAR(16))
)


class Virtualgroup(Base):
    __tablename__ = 'virtualgroup'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    created = Column(DateTime, nullable=False, server_default=text("sysdate "))
    groupname = Column(VARCHAR(200), nullable=False, unique=True)
    groupinfo = Column(VARCHAR(4000))
    registrant = Column(VARCHAR(512))
    ownercompany = Column(ForeignKey('company.id'), nullable=False, index=True)
    alignsubstime = Column(NUMBER(asdecimal=False), server_default=text("10800"))
    denyfreeacfchangeperiod = Column(NUMBER(asdecimal=False), server_default=text("30"))
    simnumberreldays = Column(NUMBER(asdecimal=False), server_default=text("180"))
    lfeepredictioninterval = Column(NUMBER(asdecimal=False))
    smssenderaddress = Column(VARCHAR(64))
    defaultaccfileid = Column(ForeignKey('accountingfile.id', ondelete='SET NULL'))
    defcurrencyid = Column(ForeignKey('currency.id'))
    emailsenderaddress = Column(VARCHAR(255))
    percentdurationforalignlicfee = Column(NUMBER(asdecimal=False))
    carddeletionmode = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    sms_schedule = Column(VARCHAR(100))
    ntfbsnomoneycooldowntime = Column(VARCHAR(200))
    ntfppackpercentthrshlds = Column(VARCHAR(200))

    accountingfile = relationship('Accountingfile', primaryjoin='Virtualgroup.defaultaccfileid == Accountingfile.id')
    currency = relationship('Currency')
    company = relationship('Company')


class VlanId(Base):
    __tablename__ = 'vlan_ids'

    id = Column(NUMBER(asdecimal=False), primary_key=True)


class VpnType(Base):
    __tablename__ = 'vpn_type'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    vt_code = Column(VARCHAR(64), nullable=False, unique=True)
    info = Column(VARCHAR(4000))


t_x_maint = Table(
    'x_maint', metadata,
    Column('created', DateTime),
    Column('msg', VARCHAR(4000))
)


t_xgate_job_params = Table(
    'xgate_job_params', metadata,
    Column('invoice_build_date', DateTime),
    Column('invoice_send_date', DateTime),
    Column('client_id', NUMBER(asdecimal=False), nullable=False, unique=True)
)


class Xgatecommand(Base):
    __tablename__ = 'xgatecommand'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    cmd_code = Column(VARCHAR(64), nullable=False, unique=True)
    cmd_info = Column(VARCHAR(1024))


class Xgatescope(Base):
    __tablename__ = 'xgatescope'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    scope_code = Column(VARCHAR(16), nullable=False, unique=True)
    scope_info = Column(VARCHAR(500))


t_accfile_billparams = Table(
    'accfile_billparams', metadata,
    Column('accfile_id', ForeignKey('accountingfile.id'), nullable=False),
    Column('name', VARCHAR(128), nullable=False),
    Column('varchar_value', VARCHAR(128), nullable=False),
    Index('uq_accfile_billparams', 'accfile_id', 'name', unique=True)
)


class Accfilecreateprofile(Base):
    __tablename__ = 'accfilecreateprofile'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    vgroupid = Column(ForeignKey('virtualgroup.id', ondelete='CASCADE'), nullable=False, unique=True)
    currencyid = Column(ForeignKey('currency.id', ondelete='SET NULL'))

    currency = relationship('Currency')
    virtualgroup = relationship('Virtualgroup')


class Accfilerelation(Base):
    __tablename__ = 'accfilerelation'
    __table_args__ = (
        Index('uq_accfilerelation', 'vgroup_id', 'src_accfile_id', 'dst_accfile_id', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    vgroup_id = Column(ForeignKey('virtualgroup.id'), nullable=False)
    src_accfile_id = Column(ForeignKey('accountingfile.id'), nullable=False)
    dst_accfile_id = Column(ForeignKey('accountingfile.id'), nullable=False)
    relation = Column(CHAR(1), server_default=text("'>'"))

    dst_accfile = relationship('Accountingfile', primaryjoin='Accfilerelation.dst_accfile_id == Accountingfile.id')
    src_accfile = relationship('Accountingfile', primaryjoin='Accfilerelation.src_accfile_id == Accountingfile.id')
    vgroup = relationship('Virtualgroup')


class Billservice(Base):
    __tablename__ = 'billservice'
    __table_args__ = {'comment': 'Тарифицируемые варианты сервисов (Входящий голосовой вызов, Исходящий вызов, Переадресация)'}

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    baseserviceid = Column(ForeignKey('baseservicetype.id'))
    bname = Column(VARCHAR(256))
    code = Column(VARCHAR(64))
    info = Column(VARCHAR(1024))
    billdirtype = Column(NUMBER(asdecimal=False))
    allowpackages = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    category_id = Column(ForeignKey('billservicecategory.id'), nullable=False, server_default=text("1 "))
    prodnumber = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    rquservarclass = Column(VARCHAR(500))
    blocked = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    srvconfig = Column(VARCHAR(4000))
    external_id = Column(VARCHAR(128))
    viewindict = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))

    baseservicetype = relationship('Baseservicetype')
    category = relationship('Billservicecategory')


class Billvolume(Base):
    __tablename__ = 'billvolume'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    measureunit = Column(ForeignKey('measureunit.id'), nullable=False)
    name = Column(VARCHAR(200), nullable=False)
    basevolume = Column(NUMBER(asdecimal=False), nullable=False)

    measureunit1 = relationship('Measureunit')


class BsJobtasklog(Base):
    __tablename__ = 'bs_jobtasklog'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    taskid = Column(ForeignKey('bs_jobtask.id', ondelete='CASCADE'), nullable=False, index=True)
    msgcreated = Column(DateTime, nullable=False, server_default=text("SYSDATE "))
    msglevel = Column(NUMBER(asdecimal=False), nullable=False)
    msgtext = Column(VARCHAR(1024), nullable=False)
    stacktraceinfo = Column(VARCHAR(2048))

    bs_jobtask = relationship('BsJobtask')


class Cardgroup(Base):
    __tablename__ = 'cardgroup'
    __table_args__ = (
        Index('uq_cardgroup_name', 'client_id', 'cg_name', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    cg_name = Column(VARCHAR(200))
    cg_info = Column(VARCHAR(1000))
    cg_parent = Column(ForeignKey('cardgroup.id'), index=True)
    cg_path = Column(VARCHAR(200), unique=True)
    client_id = Column(ForeignKey('client.id', ondelete='CASCADE'), nullable=False, index=True)

    parent = relationship('Cardgroup', remote_side=[id])
    client = relationship('Client')



class Cardsery(Base):
    __tablename__ = 'cardseries'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    name = Column(VARCHAR(256), nullable=False)
    generated = Column(DateTime, nullable=False, server_default=text("sysdate "))
    cardamount = Column(NUMBER(asdecimal=False), nullable=False)
    cardtype = Column(NUMBER(asdecimal=False), nullable=False)
    seriesprefix = Column(VARCHAR(64), nullable=False, unique=True)
    info = Column(VARCHAR(2000))
    cardfacevalue = Column(NUMBER(asdecimal=False), server_default=text("0"))
    isdeleted = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    accfileid = Column(ForeignKey('accountingfile.id', ondelete='CASCADE'), nullable=False, index=True)
    currencyid = Column(ForeignKey('currency.id'), nullable=False, server_default=text("1 "))

    accountingfile = relationship('Accountingfile')
    currency = relationship('Currency')


class ClientAssociation(Base):
    __tablename__ = 'client_association'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    vgroupid = Column(ForeignKey('virtualgroup.id'), nullable=False)
    name = Column(VARCHAR(256), nullable=False)
    info = Column(VARCHAR(1024))

    virtualgroup = relationship('Virtualgroup')


class ClientDataFile(Base):
    __tablename__ = 'client_data_file'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    client_id = Column(ForeignKey('client.id', ondelete='CASCADE'), nullable=False, index=True)
    data_key = Column(VARCHAR(64), nullable=False)
    data_info = Column(VARCHAR(200))
    data_content = Column(LargeBinary)
    data_size = Column(NUMBER(asdecimal=False))
    file_name = Column(VARCHAR(200))
    content_type = Column(VARCHAR(64))

    client = relationship('Client')


class ClientInvoiceDoc(Base):
    __tablename__ = 'client_invoice_docs'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    created = Column(DateTime, nullable=False, server_default=text("sysdate "))
    client_id = Column(ForeignKey('client.id', ondelete='CASCADE'), nullable=False, index=True)
    invoice_id = Column(ForeignKey('client_invoice.id', ondelete='CASCADE'), nullable=False, index=True)
    file_name = Column(VARCHAR(256))
    file_size = Column(NUMBER(asdecimal=False))
    file_id = Column(VARCHAR(256), nullable=False, unique=True)

    client = relationship('Client')
    invoice = relationship('ClientInvoice')


class ClientUiConfig(Base):
    __tablename__ = 'client_ui_config'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    client_id = Column(ForeignKey('client.id', ondelete='CASCADE'), nullable=False, unique=True)
    theme_name = Column(VARCHAR(200))
    custom_logo = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    form_settings = Column(VARCHAR(256))

    client = relationship('Client')


class ClientUiMsg(Base):
    __tablename__ = 'client_ui_msg'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    msg_time = Column(TIMESTAMP, nullable=False, index=True, server_default=text("current_timestamp "))
    client_id = Column(ForeignKey('client.id', ondelete='CASCADE'), nullable=False, index=True)
    subject = Column(VARCHAR(512))
    message = Column(Text)

    client = relationship('Client')


class ClientUrlNtf(Base):
    __tablename__ = 'client_url_ntf'
    __table_args__ = (
        CheckConstraint('NVL2(VGROUP_ID, 1, 0) + NVL2(CLIENT_ID, 1, 0) = 1'),
        CheckConstraint('NVL2(VGROUP_ID, 1, 0) + NVL2(CLIENT_ID, 1, 0) = 1')
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    lang_id = Column(ForeignKey('lang.id'), nullable=False)
    client_id = Column(ForeignKey('client.id', ondelete='CASCADE'))
    http_url_template = Column(VARCHAR(4000), nullable=False)
    http_body_template = Column(VARCHAR(4000))
    msg_state_codes = Column(VARCHAR(2000), nullable=False)
    http_headers = Column(VARCHAR(2000))
    vgroup_id = Column(ForeignKey('virtualgroup.id'))

    client = relationship('Client')
    lang = relationship('Lang')
    vgroup = relationship('Virtualgroup')


class Clientvehicle(Base):
    __tablename__ = 'clientvehicle'
    __table_args__ = (
        Index('uq_clientvehicle', 'client_id', 'vehicle_number', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    created = Column(DateTime, nullable=False, server_default=text("sysdate "))
    client_id = Column(ForeignKey('client.id'), nullable=False)
    vehicle_number = Column(VARCHAR(16), nullable=False)
    info = Column(VARCHAR(1000))

    client = relationship('Client')


class Company2role(Base):
    __tablename__ = 'company2role'
    __table_args__ = (
        Index('uq_comp2role', 'companyid', 'roleid', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    companyid = Column(ForeignKey('company.id', ondelete='CASCADE'), nullable=False)
    roleid = Column(ForeignKey('companyrole.id'), nullable=False)

    company = relationship('Company')
    companyrole = relationship('Companyrole')


class Companypm(Base):
    __tablename__ = 'companypms'
    __table_args__ = (
        CheckConstraint('commissionPrc between 0 and 100'),
        CheckConstraint("onExcessAction in ('D','B','I')"),
        CheckConstraint("workMode in ('T','P')"),
        Index('uq_pms_type', 'vgroupid', 'pstypeid', unique=True)
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    companyid = Column(ForeignKey('company.id'), nullable=False)
    vgroupid = Column(NUMBER(asdecimal=False), nullable=False)
    code = Column(VARCHAR(32), nullable=False, unique=True)
    accountid = Column(ForeignKey('account.id'), nullable=False, index=True)
    daylimit = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    workmode = Column(CHAR(1), nullable=False)
    onexcessaction = Column(CHAR(1), nullable=False, server_default=text("'D' "))
    pstypeid = Column(ForeignKey('paymentsystemtype.id'), nullable=False, server_default=text("0 "))
    billconfig = Column(VARCHAR(2000))
    isalarm = Column(NUMBER(asdecimal=False), server_default=text("0"))
    commissionprc = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    commissionflag = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))

    account = relationship('Account')
    company = relationship('Company')
    paymentsystemtype = relationship('Paymentsystemtype')


class Configbilling(Base):
    __tablename__ = 'configbilling'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    nationalcurrency = Column(ForeignKey('currency.id'))
    sysprecision = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("5 "))
    currlist = Column(VARCHAR(4000))
    defaultvgroupid = Column(NUMBER(asdecimal=False))

    currency = relationship('Currency')


class Contracttype(Base):
    __tablename__ = 'contracttype'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    ctcode = Column(VARCHAR(32), nullable=False, unique=True)
    ctname = Column(VARCHAR(200), nullable=False)
    ctinfo = Column(VARCHAR(4000))
    contractfile = Column(LargeBinary)
    contractfilesize = Column(NUMBER(asdecimal=False))
    ctsubjectid = Column(ForeignKey('contractsubject.id'), nullable=False)

    contractsubject = relationship('Contractsubject')


class Externalservice(Base):
    __tablename__ = 'externalservice'
    __table_args__ = (
        Index('uq_externalservice', 'code', 'companyid', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    code = Column(VARCHAR(32), nullable=False)
    companyid = Column(ForeignKey('company.id'))
    info = Column(VARCHAR(1024))

    company = relationship('Company')


class Fincorraccount(Base):
    __tablename__ = 'fincorraccount'
    __table_args__ = (
        Index('uq_fincorraccount', 'vgroupid', 'corrtypeid', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    vgroupid = Column(ForeignKey('virtualgroup.id', ondelete='CASCADE'), nullable=False)
    corrtypeid = Column(ForeignKey('fincorrtype.id'), nullable=False)
    accountid = Column(ForeignKey('account.id'), nullable=False, index=True)
    daylimit = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    weeklimit = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    monthlimit = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    lastday = Column(DateTime)
    lastweek = Column(DateTime)
    lastmonth = Column(DateTime)
    lastdayvalue = Column(NUMBER(asdecimal=False))
    lastweekvalue = Column(NUMBER(asdecimal=False))
    lastmonthvalue = Column(NUMBER(asdecimal=False))

    account = relationship('Account')
    fincorrtype = relationship('Fincorrtype')
    virtualgroup = relationship('Virtualgroup')


class GeoArea(Base):
    __tablename__ = 'geo_area'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    name = Column(VARCHAR(100), nullable=False)
    description = Column(VARCHAR(150))
    circle = Column(NUMBER(asdecimal=False))
    radius = Column(NUMBER(asdecimal=False))
    points = Column(VARCHAR(1000))
    client = Column(ForeignKey('client.id', ondelete='CASCADE'))

    client1 = relationship('Client')
    cards = relationship('Basecard', secondary='card_geo_area')


class IcOperator(Base):
    __tablename__ = 'ic_operator'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    oper_name = Column(VARCHAR(200), nullable=False, unique=True)
    conn_date = Column(DateTime)
    upd_date = Column(DateTime)
    contract_no = Column(VARCHAR(64), nullable=False, unique=True)
    currency_id = Column(ForeignKey('currency.id'))

    currency = relationship('Currency')


class Mcell(Base):
    __tablename__ = 'mcell'
    __table_args__ = (
        Index('uq_mcell', 'cellsetid', 'lac', 'cellid', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    cellsetid = Column(ForeignKey('mcellset.id', ondelete='CASCADE'), nullable=False)
    lac = Column(NUMBER(asdecimal=False), nullable=False)
    cellid = Column(NUMBER(asdecimal=False), nullable=False)

    mcellset = relationship('Mcellset')


class Messagetemplate(Base):
    __tablename__ = 'messagetemplate'
    __table_args__ = (
        CheckConstraint('(VGROUPID IS NOT NULL AND ACCFILEID IS NULL) OR (VGROUPID IS NULL AND ACCFILEID IS NOT NULL)'),
        CheckConstraint('(VGROUPID IS NOT NULL AND ACCFILEID IS NULL) OR (VGROUPID IS NULL AND ACCFILEID IS NOT NULL)'),
        CheckConstraint("deliveryType in ('SMS', 'EMAIL', 'URL')"),
        Index('uq_messagetemplate', 'vgroupid', 'accfileid', 'statecode', 'deliverytype', unique=True)
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    vgroupid = Column(ForeignKey('virtualgroup.id'))
    statecode = Column(VARCHAR(64), nullable=False)
    msgtempl = Column(VARCHAR(4000))
    immediatesend = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    deliverytype = Column(VARCHAR(5), nullable=False, server_default=text("'SMS' "))
    isenabled = Column(NUMBER(asdecimal=False), server_default=text("1"))
    is_schedule_enabled = Column(NUMBER(asdecimal=False))
    accfileid = Column(ForeignKey('accountingfile.id', ondelete='CASCADE'))

    accountingfile = relationship('Accountingfile')
    virtualgroup = relationship('Virtualgroup')


class Mnlocation(Base):
    __tablename__ = 'mnlocation'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    locname = Column(VARCHAR(200), nullable=False, unique=True)
    locinfo = Column(VARCHAR(2000))
    locsize = Column(ForeignKey('georegionsize.id'), nullable=False, server_default=text("0 "))

    georegionsize = relationship('Georegionsize')


class Mnoperator(Base):
    __tablename__ = 'mnoperator'
    __table_args__ = (
        Index('uq_mnoper_plmn', 'mcc', 'mnc', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    created = Column(DateTime, nullable=False, server_default=text("sysdate "))
    opname = Column(VARCHAR(200), nullable=False, unique=True)
    opinfo = Column(VARCHAR(2000))
    mcc = Column(VARCHAR(3), nullable=False)
    mnc = Column(VARCHAR(3), nullable=False)
    countryid = Column(ForeignKey('country.id'), index=True)

    country = relationship('Country')


class Msgstatecode(Base):
    __tablename__ = 'msgstatecode'

    statecode = Column(VARCHAR(64), primary_key=True)
    stateinfo = Column(VARCHAR(512))
    cat_code = Column(ForeignKey('msgstatecategory.cat_code'), nullable=False)
    opt_tags = Column(VARCHAR(256))
    disporder = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))

    msgstatecategory = relationship('Msgstatecategory')


class Ntfsetting(Base):
    __tablename__ = 'ntfsettings'
    __table_args__ = (
        CheckConstraint(' NVL2(VGROUP_ID, 1, 0) + NVL2(ACCFILE_ID, 1, 0) = 1 '),
        CheckConstraint(' NVL2(VGROUP_ID, 1, 0) + NVL2(ACCFILE_ID, 1, 0) = 1 '),
        Index('uq_ntfsettings', 'vgroup_id', 'accfile_id', unique=True)
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    vgroup_id = Column(ForeignKey('virtualgroup.id', ondelete='CASCADE'))
    accfile_id = Column(ForeignKey('accountingfile.id', ondelete='CASCADE'))
    smssenderaddress = Column(VARCHAR(64))
    emailsenderaddress = Column(VARCHAR(255))
    sms_schedule = Column(VARCHAR(100))

    accfile = relationship('Accountingfile')
    vgroup = relationship('Virtualgroup')


class Parkbillzone(Base):
    __tablename__ = 'parkbillzone'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    pzonename = Column(VARCHAR(200), nullable=False, unique=True)
    pzoneinfo = Column(VARCHAR(1000))
    defaultcost = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    defcurrencyid = Column(ForeignKey('currency.id'))

    currency = relationship('Currency')


class Parkomat(Base):
    __tablename__ = 'parkomat'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    vgroupid = Column(ForeignKey('virtualgroup.id', ondelete='CASCADE'), nullable=False, index=True)
    ptname = Column(VARCHAR(200), nullable=False)
    ptinfo = Column(VARCHAR(1000))
    geoaddress = Column(VARCHAR(500))
    ipaddress = Column(VARCHAR(32), unique=True)
    extid = Column(VARCHAR(32), unique=True)
    paymethod = Column(VARCHAR(200))

    virtualgroup = relationship('Virtualgroup')


class Parkprivilege(Base):
    __tablename__ = 'parkprivilege'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    created = Column(DateTime, nullable=False, server_default=text("sysdate "))
    registrant = Column(VARCHAR(200), nullable=False)
    ownerdname = Column(VARCHAR(200), nullable=False)
    regdocinfo = Column(VARCHAR(200), nullable=False)
    vehiclenumber = Column(VARCHAR(16), nullable=False, unique=True)
    orderdocno = Column(VARCHAR(64), nullable=False, index=True)
    expired = Column(DateTime)
    info = Column(VARCHAR(1000))
    ownerdnameup = Column(VARCHAR(200), nullable=False, index=True)
    privtypeid = Column(ForeignKey('parkprivilegetype.id'), nullable=False)
    privpersonid = Column(ForeignKey('personinfo.id'))
    reppersonid = Column(ForeignKey('personinfo.id'))
    insurancenumber = Column(VARCHAR(32))
    vehiclemodel = Column(VARCHAR(128))
    vehiclecolor = Column(VARCHAR(128))
    lastupdate = Column(DateTime)
    prolongdate = Column(DateTime)
    canceldate = Column(DateTime)
    disperiodstart = Column(DateTime)
    disperiodend = Column(DateTime)
    disreview = Column(DateTime)

    personinfo = relationship('Personinfo', primaryjoin='Parkprivilege.privpersonid == Personinfo.id')
    parkprivilegetype = relationship('Parkprivilegetype')
    personinfo1 = relationship('Personinfo', primaryjoin='Parkprivilege.reppersonid == Personinfo.id')


class Productactionqueue(Base):
    __tablename__ = 'productactionqueue'
    __table_args__ = (
        Index('uq_productactionqueue', 'card_id', 'prod_id', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    created = Column(DateTime, server_default=text("sysdate"))
    card_id = Column(NUMBER(asdecimal=False), nullable=False)
    prod_id = Column(NUMBER(asdecimal=False), nullable=False)
    next_try = Column(DateTime, nullable=False, index=True)
    discount_id = Column(NUMBER(asdecimal=False))
    subscriptionid = Column(NUMBER(asdecimal=False))
    actiontype = Column(NUMBER(asdecimal=False), server_default=text("0"))
    attemptcount = Column(NUMBER(asdecimal=False), server_default=text("0"))
    requestinfo = Column(VARCHAR(4000))
    provisioning = Column(NUMBER(asdecimal=False), server_default=text("0"))
    uservars = Column(VARCHAR(4000))
    modifiers = Column(VARCHAR(1000))
    ext_account_id = Column(ForeignKey('account.id'))

    ext_account = relationship('Account')


class Qo(Base):
    __tablename__ = 'qos'
    __table_args__ = (
        Index('uq_qoscode', 'servicetype', 'code', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    code = Column(VARCHAR(32), nullable=False)
    servicetype = Column(ForeignKey('baseservicetype.id'))
    name = Column(VARCHAR(128), nullable=False)
    extid = Column(VARCHAR(32), nullable=False)

    baseservicetype = relationship('Baseservicetype')


class Qosp(Qo):
    __tablename__ = 'qosp'

    id = Column(ForeignKey('qos.id'), primary_key=True)
    uspeed = Column(NUMBER(asdecimal=False), nullable=False)
    dspeed = Column(NUMBER(asdecimal=False), nullable=False)
    classid = Column(NUMBER(asdecimal=False), server_default=text("1"))


class QueueSendInvoiceDoc(Base):
    __tablename__ = 'queue_send_invoice_docs'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    client_id = Column(ForeignKey('client.id', ondelete='CASCADE'), nullable=False)
    invoice_id = Column(ForeignKey('client_invoice.invoice_id', ondelete='CASCADE'))
    vgroup_id = Column(ForeignKey('virtualgroup.id', ondelete='CASCADE'))
    lang_id = Column(ForeignKey('lang.id'))
    path_file = Column(VARCHAR(1024))
    created = Column(TIMESTAMP)
    last_send = Column(TIMESTAMP)
    to_delivery = Column(VARCHAR(256))
    count_try_send = Column(NUMBER(asdecimal=False))
    type_delivery = Column(VARCHAR(64))
    status = Column(VARCHAR(128))
    error_message = Column(VARCHAR(2048))
    service = Column(VARCHAR(128))

    client = relationship('Client')
    invoice = relationship('ClientInvoice')
    lang = relationship('Lang')
    vgroup = relationship('Virtualgroup')


class Sgsngroup(Base):
    __tablename__ = 'sgsngroup'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    grname = Column(VARCHAR(200), nullable=False, unique=True)
    grinfo = Column(VARCHAR(2000))
    grsize = Column(ForeignKey('georegionsize.id'), nullable=False, server_default=text("0 "))

    georegionsize = relationship('Georegionsize')


class Simnumberfakeprefix(Base):
    __tablename__ = 'simnumberfakeprefix'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    created = Column(DateTime, nullable=False, server_default=text("sysdate "))
    vgroup_id = Column(ForeignKey('virtualgroup.id'), nullable=False, index=True)
    num_prefix = Column(VARCHAR(32), nullable=False, unique=True)
    num_length = Column(NUMBER(asdecimal=False), nullable=False)
    prefix_name = Column(VARCHAR(100), nullable=False)
    prefix_info = Column(VARCHAR(1000))
    lastupdate = Column(DateTime)

    vgroup = relationship('Virtualgroup')


class Simnumberrate(Base):
    __tablename__ = 'simnumberrate'
    __table_args__ = (
        Index('uq_simnumrate', 'vgroup_id', 'rate_level', unique=True),
        Index('uq_simnumrate_name', 'vgroup_id', 'rate_name', unique=True)
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    vgroup_id = Column(ForeignKey('virtualgroup.id'), nullable=False, index=True)
    created = Column(DateTime, nullable=False, server_default=text("sysdate "))
    rate_level = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    rate_name = Column(VARCHAR(100), nullable=False)
    rate_info = Column(VARCHAR(1000))
    rate_cost = Column(NUMBER(asdecimal=False), nullable=False)
    currency_id = Column(ForeignKey('currency.id'), nullable=False, index=True)

    currency = relationship('Currency')
    vgroup = relationship('Virtualgroup')


class Simreplacementpool(Base):
    __tablename__ = 'simreplacementpool'
    __table_args__ = (
        Index('uq_simrepl_icc', 'vgroupid', 'icc', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    vgroupid = Column(ForeignKey('virtualgroup.id', ondelete='CASCADE'), nullable=False)
    imsi = Column(VARCHAR(64), nullable=False, unique=True)
    icc = Column(VARCHAR(64), nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("sysdate "))
    userid = Column(NUMBER(asdecimal=False), nullable=False)
    pin1 = Column(VARCHAR(16))
    pin2 = Column(VARCHAR(16))
    puk1 = Column(VARCHAR(16))
    puk2 = Column(VARCHAR(16))
    client_id = Column(ForeignKey('client.id', ondelete='SET NULL'), index=True)
    sim_type = Column(VARCHAR(32))
    sim_vendor = Column(VARCHAR(64))
    sim_espec = Column(VARCHAR(32))
    app_vendor = Column(VARCHAR(64))
    app_version = Column(VARCHAR(64))
    sim_actcode = Column(VARCHAR(256))
    batch_number = Column(VARCHAR(64))

    client = relationship('Client')
    virtualgroup = relationship('Virtualgroup')


class Smscommand(Base):
    __tablename__ = 'smscommand'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    command = Column(VARCHAR(128), nullable=False)
    info = Column(VARCHAR(256))
    client_id = Column(ForeignKey('client.id', ondelete='CASCADE'), nullable=False)

    client = relationship('Client')


class Tariffplan(Base):
    __tablename__ = 'tariffplan'
    __table_args__ = {'comment': 'Тарифный план для услуг'}

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    billtype = Column(ForeignKey('billingtype.id'), nullable=False)
    planname = Column(VARCHAR(256))
    planinfo = Column(VARCHAR(1024))
    created = Column(DateTime)
    plancode = Column(VARCHAR(64))
    currencyid = Column(ForeignKey('currency.id'))
    vgroupid = Column(ForeignKey('virtualgroup.id'), index=True)

    billingtype = relationship('Billingtype')
    currency = relationship('Currency')
    virtualgroup = relationship('Virtualgroup')


class Tariffzone(Base):
    __tablename__ = 'tariffzone'
    __table_args__ = (
        Index('uq_calltzone_name', 'schemaid', 'tzname', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    schemaid = Column(ForeignKey('routeschema.id', ondelete='CASCADE'), nullable=False)
    tzname = Column(VARCHAR(256), nullable=False)
    tzinfo = Column(VARCHAR(2000))

    routeschema = relationship('Routeschema')


class Timeperiod(Base):
    __tablename__ = 'timeperiod'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    timeunit = Column(ForeignKey('timeunit.id'), nullable=False)
    amount = Column(NUMBER(asdecimal=False), nullable=False)
    periodname = Column(VARCHAR(128), nullable=False)
    periodinfo = Column(VARCHAR(512))

    timeunit1 = relationship('Timeunit')


class TrgRecord(Base):
    __tablename__ = 'trg_record'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    vgroup_id = Column(ForeignKey('virtualgroup.id'), nullable=False, index=True)
    event_type_id = Column(ForeignKey('trg_eventtype.id'), nullable=False, index=True)
    trg_name = Column(VARCHAR(200))
    astate = Column(NUMBER(asdecimal=False), nullable=False)
    client_id = Column(ForeignKey('client.id', ondelete='CASCADE'), nullable=False, index=True)
    external_id = Column(VARCHAR(64), unique=True)
    scope_id = Column(NUMBER(asdecimal=False), nullable=False)

    client = relationship('Client')
    event_type = relationship('TrgEventtype')
    vgroup = relationship('Virtualgroup')


class Userlogin(Base):
    __tablename__ = 'userlogin'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    login = Column(VARCHAR(64), nullable=False, unique=True)
    passwd = Column(VARCHAR(512), nullable=False)
    userrole = Column(ForeignKey('userrole.id'), nullable=False)
    vgroupid = Column(ForeignKey('virtualgroup.id', ondelete='CASCADE'), index=True)
    personid = Column(ForeignKey('personinfo.id', ondelete='SET NULL'), index=True)
    state = Column(ForeignKey('adminstate.id'), nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("sysdate "))
    info = Column(VARCHAR(2000))
    targetcompanyid = Column(ForeignKey('company.id', ondelete='CASCADE'))
    login_lcase = Column(VARCHAR(64), nullable=False, unique=True)

    personinfo = relationship('Personinfo')
    adminstate = relationship('Adminstate')
    company = relationship('Company')
    userrole1 = relationship('Userrole')
    virtualgroup = relationship('Virtualgroup')


class Ussdcommand(Base):
    __tablename__ = 'ussdcommand'
    __table_args__ = (
        Index('uq_ussdcommand_mask', 'vgroupid', 'ussdmask', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    commandid = Column(ForeignKey('servicecommand.id'), nullable=False, index=True)
    ussdmask = Column(VARCHAR(128), nullable=False)
    smsanswer = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    vgroupid = Column(ForeignKey('virtualgroup.id'), nullable=False, index=True)
    msgtext = Column(VARCHAR(4000))
    defvalues = Column(VARCHAR(1024))

    servicecommand = relationship('Servicecommand')
    virtualgroup = relationship('Virtualgroup')


class Vgtariffschedule(Base):
    __tablename__ = 'vgtariffschedule'
    __table_args__ = (
        Index('uq_vg_tf_sched', 'vgroupid', 'schedname', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    vgroupid = Column(ForeignKey('virtualgroup.id'), nullable=False, index=True)
    schedname = Column(VARCHAR(200), nullable=False)
    schedinfo = Column(VARCHAR(4000))
    n_order = Column(NUMBER(asdecimal=False), nullable=False)

    virtualgroup = relationship('Virtualgroup')


class Vpn(Base):
    __tablename__ = 'vpn'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    client_id = Column(ForeignKey('client.id', ondelete='CASCADE'), nullable=False)
    vpn_type = Column(ForeignKey('vpn_type.id'), nullable=False)
    description = Column(VARCHAR(1000))
    vlan_id = Column(ForeignKey('vlan_ids.id'), unique=True)

    client = relationship('Client')
    vlan = relationship('VlanId')
    vpn_type1 = relationship('VpnType')


class VpnTypeToClient(Base):
    __tablename__ = 'vpn_type_to_client'
    __table_args__ = (
        Index('uq_vpn_type_to_client', 'vpn_type', 'client_id', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    vpn_type = Column(ForeignKey('vpn_type.id'), nullable=False)
    client_id = Column(ForeignKey('client.id', ondelete='CASCADE'), nullable=False)

    client = relationship('Client')
    vpn_type1 = relationship('VpnType')


class Weblogin(Base):
    __tablename__ = 'weblogin'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    created = Column(DateTime, nullable=False, server_default=text("sysdate "))
    login = Column(VARCHAR(32), nullable=False, unique=True)
    passwd = Column(VARCHAR(64), nullable=False)
    ext_role = Column(NUMBER(asdecimal=False))
    client_id = Column(ForeignKey('client.id', ondelete='CASCADE'), index=True)
    approved = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    last_change = Column(DateTime, server_default=text("sysdate"))
    last_passwd = Column(VARCHAR(64))

    client = relationship('Client')


class Xgaterole(Base):
    __tablename__ = 'xgaterole'
    __table_args__ = (
        CheckConstraint("role_class in ('all','all_read','custom')"),
        Index('uq_xgaterole_name', 'vgroupid', 'role_name', unique=True)
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    vgroupid = Column(ForeignKey('virtualgroup.id', ondelete='CASCADE'), nullable=False)
    role_name = Column(VARCHAR(128), nullable=False)
    role_info = Column(VARCHAR(1024))
    role_class = Column(VARCHAR(64), nullable=False)
    xcmd_list = Column(VARCHAR(4000))
    scope_id = Column(ForeignKey('xgatescope.id'))
    admin = Column(NUMBER(asdecimal=False))

    scope = relationship('Xgatescope')
    virtualgroup = relationship('Virtualgroup')


class Accfileplanschedule(Base):
    __tablename__ = 'accfileplanschedule'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    accfileid = Column(ForeignKey('accountingfile.id'), nullable=False, index=True)
    billtype = Column(ForeignKey('billingtype.id'))
    activefrom = Column(DateTime, nullable=False)
    activetill = Column(DateTime)
    planid = Column(ForeignKey('tariffplan.id'), nullable=False, index=True)
    entryinfo = Column(VARCHAR(1000))
    priority = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    destaccfile = Column(ForeignKey('accountingfile.id', ondelete='CASCADE'))

    accountingfile = relationship('Accountingfile', primaryjoin='Accfileplanschedule.accfileid == Accountingfile.id')
    billingtype = relationship('Billingtype')
    accountingfile1 = relationship('Accountingfile', primaryjoin='Accfileplanschedule.destaccfile == Accountingfile.id')
    tariffplan = relationship('Tariffplan')


class Basecard(Base):
    __tablename__ = 'basecard'
    __table_args__ = (
        Index('ix_series_cont', 'accfileid', 'vgroupid'),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    cardtype = Column(ForeignKey('cardtype.id'), nullable=False)
    vgroupid = Column(ForeignKey('virtualgroup.id'), nullable=False)
    accfileid = Column(ForeignKey('accountingfile.id'), nullable=False)
    created = Column(DateTime, nullable=False, server_default=text("sysdate "))
    state = Column(ForeignKey('lock_state.id'), nullable=False)
    dealerid = Column(ForeignKey('company.id'))
    emitentid = Column(ForeignKey('company.id'))
    activefrom = Column(DateTime)
    expired = Column(DateTime)
    saled = Column(DateTime)
    activated = Column(DateTime)
    firsttransaction = Column(DateTime)
    seriesid = Column(ForeignKey('cardseries.id'), index=True)
    seriesnumber = Column(NUMBER(asdecimal=False))
    cardnumber = Column(VARCHAR(64), nullable=False, unique=True)
    lang = Column(ForeignKey('lang.id'))
    info = Column(VARCHAR(1024))
    info2 = Column(VARCHAR(1024))
    opstate = Column(ForeignKey('cardstate.id'), server_default=text("1"))
    opstatechangedate = Column(DateTime)
    lastacfchangedate = Column(DateTime)
    factsellerid = Column(ForeignKey('company.id'))
    shipped = Column(DateTime)
    shipmentuserid = Column(NUMBER(asdecimal=False))
    shipmentuserinfo = Column(VARCHAR(200))
    repairdate = Column(DateTime)
    check_state_id = Column(ForeignKey('cardcheckstate.id'), nullable=False, server_default=text("1 "))
    check_date = Column(DateTime)
    batch_number = Column(VARCHAR(64))

    accountingfile = relationship('Accountingfile')
    cardtype1 = relationship('Cardtype')
    check_state = relationship('Cardcheckstate')
    company = relationship('Company', primaryjoin='Basecard.dealerid == Company.id')
    company1 = relationship('Company', primaryjoin='Basecard.emitentid == Company.id')
    company2 = relationship('Company', primaryjoin='Basecard.factsellerid == Company.id')
    lang1 = relationship('Lang')
    cardstate = relationship('Cardstate')
    cardsery = relationship('Cardsery')
    lock_state = relationship('LockState')
    virtualgroup = relationship('Virtualgroup')
    groups = relationship('Cardgroup', secondary='cardgrouplink')


class CardLastLocation(Basecard):
    __tablename__ = 'card_last_location'

    card_id = Column(ForeignKey('basecard.id', ondelete='CASCADE'), primary_key=True)
    change_date = Column(DateTime, nullable=False)
    mcc = Column(VARCHAR(3), nullable=False)
    mnc = Column(VARCHAR(3), nullable=False)


class Pacodeattemptcounter(Basecard):
    __tablename__ = 'pacodeattemptcounter'

    cardid = Column(ForeignKey('basecard.id', ondelete='CASCADE'), primary_key=True)
    firstattemptdate = Column(DateTime, nullable=False)
    lastattemptdate = Column(DateTime, nullable=False)
    lastattemptnum = Column(NUMBER(asdecimal=False), nullable=False)


class Parkbillcard(Basecard):
    __tablename__ = 'parkbillcard'

    id = Column(ForeignKey('basecard.id', ondelete='CASCADE'), primary_key=True)
    client_id = Column(ForeignKey('client.id', ondelete='CASCADE'), nullable=False)
    account_id = Column(ForeignKey('account.id', ondelete='SET NULL'), nullable=False)
    face_number = Column(VARCHAR(64), unique=True)
    info = Column(VARCHAR(1000))
    rec_code_assigned = Column(DateTime)

    account = relationship('Account')
    client = relationship('Client')


class Vouchercard(Basecard):
    __tablename__ = 'vouchercard'

    id = Column(ForeignKey('basecard.id', ondelete='CASCADE'), primary_key=True)
    secret_code = Column(VARCHAR(64), nullable=False, unique=True)
    money = Column(NUMBER(asdecimal=False), nullable=False)
    currency_id = Column(ForeignKey('currency.id'), nullable=False)
    target_account_id = Column(NUMBER(asdecimal=False))
    target_card_id = Column(NUMBER(asdecimal=False))
    target_number = Column(VARCHAR(64))

    currency = relationship('Currency')


class ClientDiscount(Base):
    __tablename__ = 'client_discount'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    description = Column(VARCHAR(100))
    period_id = Column(ForeignKey('timeperiod.id'), nullable=False)
    priority = Column(NUMBER(asdecimal=False), nullable=False)
    vgroup_id = Column(ForeignKey('virtualgroup.id'), nullable=False)

    period = relationship('Timeperiod')
    vgroup = relationship('Virtualgroup')


class Fincorruserrule(Base):
    __tablename__ = 'fincorruserrules'
    __table_args__ = (
        Index('uq_fincor_urule', 'userid', 'finaccid', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    userid = Column(ForeignKey('userlogin.id', ondelete='CASCADE'), nullable=False)
    finaccid = Column(ForeignKey('fincorraccount.id', ondelete='CASCADE'))
    daylimit = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    lastday = Column(DateTime)
    lastdayvalue = Column(NUMBER(asdecimal=False))

    fincorraccount = relationship('Fincorraccount')
    userlogin = relationship('Userlogin')


class IcObSchedule(Base):
    __tablename__ = 'ic_ob_schedule'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    operator_id = Column(ForeignKey('ic_operator.id', ondelete='CASCADE'), nullable=False, index=True)
    date_from = Column(DateTime, nullable=False)
    date_till = Column(DateTime)
    sched_comment = Column(VARCHAR(512))

    operator = relationship('IcOperator')


class IcOperconn(Base):
    __tablename__ = 'ic_operconn'
    __table_args__ = (
        CheckConstraint("conn_type in ('I','O','A')"),
        Index('ix_ic_operconn_pc', 'point_code', 'conn_type'),
        Index('uq_ic_iperconn', 'conn_ip', 'conn_port', unique=True)
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    conn_ip = Column(VARCHAR(32), nullable=False)
    conn_port = Column(NUMBER(asdecimal=False), nullable=False)
    sgunit_name = Column(VARCHAR(128), nullable=False)
    point_code = Column(NUMBER(asdecimal=False), nullable=False)
    operator_id = Column(ForeignKey('ic_operator.id', ondelete='CASCADE'), nullable=False, index=True)
    conn_type = Column(CHAR(1), nullable=False)
    tfbundle_id = Column(ForeignKey('ic_tfbundle.id'), nullable=False, index=True)
    channel_range = Column(VARCHAR(1000))

    operator = relationship('IcOperator')
    tfbundle = relationship('IcTfbundle')


class IcTfDirection(Base):
    __tablename__ = 'ic_tf_direction'
    __table_args__ = (
        Index('uq_ic_tfdir_index', 'operator_id', 'dir_index', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    operator_id = Column(ForeignKey('ic_operator.id'), nullable=False)
    ext_id = Column(NUMBER(asdecimal=False), nullable=False)
    dir_name = Column(VARCHAR(256), nullable=False)
    dir_index = Column(VARCHAR(64), nullable=False)

    operator = relationship('IcOperator')


class IpAddressPool(Base):
    __tablename__ = 'ip_address_pool'
    __table_args__ = (
        Index('uq_iap_id_vpn', 'id', 'vpn_id', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    type = Column(ForeignKey('ip_address_pool_type.id'), nullable=False)
    vpn_id = Column(ForeignKey('vpn.id'), nullable=False)
    address_mask = Column(VARCHAR(100), nullable=False)
    description = Column(VARCHAR(1000))
    total_ip_count = Column(NUMBER(asdecimal=False))
    free_ip_count = Column(NUMBER(asdecimal=False))

    ip_address_pool_type = relationship('IpAddressPoolType')
    vpn = relationship('Vpn')


class Mnloc2country(Base):
    __tablename__ = 'mnloc2country'
    __table_args__ = (
        Index('uq_mnloc2cnt', 'countryid', 'locid', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    locid = Column(ForeignKey('mnlocation.id', ondelete='CASCADE'), nullable=False, index=True)
    countryid = Column(ForeignKey('country.id', ondelete='CASCADE'), nullable=False)

    country = relationship('Country')
    mnlocation = relationship('Mnlocation')


class Mnloc2operator(Base):
    __tablename__ = 'mnloc2operator'
    __table_args__ = (
        Index('uq_mnloc2oper', 'operid', 'locid', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    locid = Column(ForeignKey('mnlocation.id', ondelete='CASCADE'), nullable=False, index=True)
    operid = Column(ForeignKey('mnoperator.id', ondelete='CASCADE'), nullable=False)

    mnlocation = relationship('Mnlocation')
    mnoperator = relationship('Mnoperator')


class Mnoperprefix(Base):
    __tablename__ = 'mnoperprefix'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    operid = Column(ForeignKey('mnoperator.id', ondelete='CASCADE'), nullable=False, index=True)
    prefix = Column(VARCHAR(32), nullable=False, unique=True)
    info = Column(VARCHAR(1000))

    mnoperator = relationship('Mnoperator')


class Mvnohomeoperator(Base):
    __tablename__ = 'mvnohomeoperator'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    mnoperator_id = Column(ForeignKey('mnoperator.id', ondelete='CASCADE'), nullable=False)
    vgroup_id = Column(ForeignKey('virtualgroup.id', ondelete='CASCADE'), nullable=False)

    mnoperator = relationship('Mnoperator')
    vgroup = relationship('Virtualgroup')


class Parking(Base):
    __tablename__ = 'parking'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    vgroupid = Column(ForeignKey('virtualgroup.id', ondelete='CASCADE'), nullable=False, index=True)
    externalid = Column(VARCHAR(64), nullable=False, unique=True)
    parkname = Column(VARCHAR(512))
    parkaddress = Column(VARCHAR(1024))
    parkspace = Column(NUMBER(asdecimal=False), server_default=text("0"))
    parktypeid = Column(ForeignKey('parkingtype.id'), nullable=False)
    contactpersonid = Column(NUMBER(asdecimal=False))
    workschedule = Column(VARCHAR(1024))
    parkbillzoneid = Column(ForeignKey('parkbillzone.id'), nullable=False)
    rentcost = Column(NUMBER(asdecimal=False))

    parkbillzone = relationship('Parkbillzone')
    parkingtype = relationship('Parkingtype')
    virtualgroup = relationship('Virtualgroup')


class Parkingabonement(Base):
    __tablename__ = 'parkingabonement'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    created = Column(DateTime, nullable=False, server_default=text("sysdate "))
    client_id = Column(ForeignKey('client.id', ondelete='CASCADE'), nullable=False)
    regnum = Column(VARCHAR(32), nullable=False, unique=True)
    vehicenum = Column(VARCHAR(16), nullable=False)
    activefrom = Column(DateTime, nullable=False)
    activetill = Column(DateTime, nullable=False)
    period_id = Column(ForeignKey('timeperiod.id'), nullable=False)

    client = relationship('Client')
    period = relationship('Timeperiod')


class Paymentschema(Base):
    __tablename__ = 'paymentschema'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    currencyid = Column(ForeignKey('currency.id'), nullable=False)
    ordercost = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    nomoneyactionid = Column(ForeignKey('billingaction.id'), nullable=False, server_default=text("0 "))
    totalperiodid = Column(ForeignKey('timeperiod.id'), nullable=False, server_default=text("0 "))
    maxrenewalretry = Column(NUMBER(asdecimal=False), nullable=False)
    paymode = Column(ForeignKey('paymentschemamode.id'), nullable=False, server_default=text("0 "))
    noordercostonacfchange = Column(NUMBER(asdecimal=False), server_default=text("0"))
    priority = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    percentdurationforalignlicfee = Column(NUMBER(asdecimal=False))
    onetimechargewithtrafficend = Column(NUMBER(asdecimal=False))
    switchtodailylicfee = Column(NUMBER(asdecimal=False))

    currency = relationship('Currency')
    billingaction = relationship('Billingaction')
    paymentschemamode = relationship('Paymentschemamode')
    timeperiod = relationship('Timeperiod')


class Sgsn(Base):
    __tablename__ = 'sgsn'
    __table_args__ = (
        Index('ix_sgsn_range', 'minip', 'maxip'),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    created = Column(DateTime, nullable=False, server_default=text("sysdate "))
    operid = Column(ForeignKey('mnoperator.id', ondelete='CASCADE'), nullable=False, index=True)
    sgsn = Column(VARCHAR(128), nullable=False, unique=True)
    netmask = Column(NUMBER(asdecimal=False), nullable=False)
    subnet = Column(NUMBER(asdecimal=False), nullable=False)
    minip = Column(NUMBER(asdecimal=False), nullable=False)
    maxip = Column(NUMBER(asdecimal=False), nullable=False)
    info = Column(VARCHAR(2048))

    mnoperator = relationship('Mnoperator')


class Tariff(Base):
    __tablename__ = 'tariff'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    tariffname = Column(VARCHAR(256))
    tariffinfo = Column(VARCHAR(1024))
    adminstate = Column(NUMBER(asdecimal=False))
    billservice = Column(ForeignKey('billservice.id'), nullable=False)
    currencyid = Column(ForeignKey('currency.id'), nullable=False)
    tariffos = Column(VARCHAR(4000))
    billvolumetype = Column(ForeignKey('billvolume.id'), nullable=False)
    basevolumecost = Column(NUMBER(asdecimal=False))
    slimit = Column(NUMBER(asdecimal=False), server_default=text("0"))
    services = Column(VARCHAR(4000))

    billservice1 = relationship('Billservice')
    billvolume = relationship('Billvolume')
    currency = relationship('Currency')


class Tariffplanschedule(Base):
    __tablename__ = 'tariffplanschedule'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    planid = Column(ForeignKey('tariffplan.id', ondelete='CASCADE'), nullable=False, index=True)
    info = Column(VARCHAR(1024))
    activefrom = Column(DateTime)
    activetill = Column(DateTime)
    routeschema = Column(ForeignKey('routeschema.id'))

    tariffplan = relationship('Tariffplan')
    routeschema1 = relationship('Routeschema')


class TrgAction(Base):
    __tablename__ = 'trg_action'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    action_type_id = Column(ForeignKey('trg_actiontype.id'), nullable=False, index=True)
    trigger_id = Column(ForeignKey('trg_record.id', ondelete='CASCADE'), nullable=False, index=True)
    params = Column(VARCHAR(200))

    action_type = relationship('TrgActiontype')
    trigger = relationship('TrgRecord')


class TrgConfigCounter(Base):
    __tablename__ = 'trg_config_counter'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    trigger_id = Column(ForeignKey('trg_record.id', ondelete='CASCADE'), nullable=False, index=True)
    bill_service = Column(ForeignKey('billservice.id'), nullable=False)
    measure_unit = Column(ForeignKey('measureunit.id'))
    limit_value = Column(NUMBER(asdecimal=False), nullable=False)
    period_id = Column(ForeignKey('timeperiod.id'), nullable=False)
    changed_date = Column(TIMESTAMP, nullable=False, server_default=text("sysdate "))
    count_bill_services = Column(VARCHAR(500))
    count_currency_id = Column(NUMBER(asdecimal=False))

    billservice = relationship('Billservice')
    measureunit = relationship('Measureunit')
    period = relationship('Timeperiod')
    trigger = relationship('TrgRecord')


class TrgCtrlLocationConfig(Base):
    __tablename__ = 'trg_ctrl_location_config'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    trigger_id = Column(ForeignKey('trg_record.id', ondelete='CASCADE'), nullable=False, index=True)
    check_interval_in_seconds = Column(NUMBER(asdecimal=False), nullable=False)

    trigger = relationship('TrgRecord')


class TrgLiveImsiConfig(Base):
    __tablename__ = 'trg_live_imsi_config'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    trigger_id = Column(ForeignKey('trg_record.id', ondelete='CASCADE'), nullable=False, index=True)
    enabled_action_on_init = Column(NUMBER(asdecimal=False), server_default=text("0"))

    trigger = relationship('TrgRecord')


class Vgtariffscheduledatum(Base):
    __tablename__ = 'vgtariffscheduledata'
    __table_args__ = (
        Index('ix_vgtariffscheduledata', 'schedule_id', 'daytype'),
        Index('ix_vgtariffscheduledatasd', 'daydate', 'schedule_id')
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    schedule_id = Column(ForeignKey('vgtariffschedule.id', ondelete='CASCADE'), nullable=False)
    daytype = Column(ForeignKey('daytype.id'), nullable=False)
    usetime = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    tstart = Column(NUMBER(asdecimal=False), server_default=text("0"))
    tend = Column(NUMBER(asdecimal=False), server_default=text("86400"))
    daydate = Column(DateTime)
    is_exclude = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))

    daytype1 = relationship('Daytype')
    schedule = relationship('Vgtariffschedule')


class Vlr(Base):
    __tablename__ = 'vlr'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    created = Column(DateTime, nullable=False, server_default=text("sysdate "))
    operid = Column(ForeignKey('mnoperator.id', ondelete='CASCADE'), nullable=False, index=True)
    vlrprefix = Column(VARCHAR(32), nullable=False, unique=True)
    vlrinfo = Column(VARCHAR(1000))

    mnoperator = relationship('Mnoperator')


class Zonedirection(Base):
    __tablename__ = 'zonedirection'
    __table_args__ = (
        Index('uq_calldirprefix', 'schemaid', 'prefix', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    zoneid = Column(ForeignKey('tariffzone.id', ondelete='CASCADE'))
    schemaid = Column(ForeignKey('routeschema.id', ondelete='CASCADE'), nullable=False)
    prefix = Column(VARCHAR(64), nullable=False)
    numlength = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("-1 "))
    adminstate = Column(NUMBER(asdecimal=False), nullable=False)
    dirname = Column(VARCHAR(200), nullable=False, index=True)
    created = Column(DateTime, nullable=False, server_default=text("sysdate "))
    isexclude = Column(NUMBER(asdecimal=False), server_default=text("0"))

    routeschema = relationship('Routeschema')
    tariffzone = relationship('Tariffzone')


class BankInformationSub(Base):
    __tablename__ = 'bank_information_subs'
    __table_args__ = (
        Index('uq_bank_inform_subs', 'card_id', 'bank_name', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    card_id = Column(ForeignKey('basecard.id', ondelete='CASCADE'), nullable=False)
    msisdn = Column(VARCHAR(32), nullable=False)
    bank_name = Column(VARCHAR(200), nullable=False)
    start_date = Column(DateTime, nullable=False)
    params = Column(VARCHAR(600))

    card = relationship('Basecard')


class Block(Base):
    __tablename__ = 'block'
    __table_args__ = (
        CheckConstraint('NVL2(CARD, 1, 0) + NVL2(CLIENT, 1, 0) + NVL2(ACCFILE, 1, 0) + NVL2(VGROUP, 1, 0) = 1'),
        CheckConstraint('NVL2(CARD, 1, 0) + NVL2(CLIENT, 1, 0) + NVL2(ACCFILE, 1, 0) + NVL2(VGROUP, 1, 0) = 1'),
        CheckConstraint('NVL2(CARD, 1, 0) + NVL2(CLIENT, 1, 0) + NVL2(ACCFILE, 1, 0) + NVL2(VGROUP, 1, 0) = 1'),
        CheckConstraint('NVL2(CARD, 1, 0) + NVL2(CLIENT, 1, 0) + NVL2(ACCFILE, 1, 0) + NVL2(VGROUP, 1, 0) = 1'),
        Index('uq_block', 'card', 'client', 'accfile', 'vgroup', unique=True)
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    vgroup = Column(ForeignKey('virtualgroup.id'))
    client = Column(ForeignKey('client.id', ondelete='CASCADE'))
    card = Column(ForeignKey('basecard.id', ondelete='CASCADE'))
    restrictions = Column(VARCHAR(2000), nullable=False)
    accfile = Column(ForeignKey('accountingfile.id', ondelete='CASCADE'))

    accountingfile = relationship('Accountingfile')
    basecard = relationship('Basecard')
    client1 = relationship('Client')
    virtualgroup = relationship('Virtualgroup')


t_card_geo_area = Table(
    'card_geo_area', metadata,
    Column('card_id', ForeignKey('basecard.id', ondelete='CASCADE'), primary_key=True),
    Column('area_id', ForeignKey('geo_area.id', ondelete='CASCADE'), nullable=False, index=True)
)


class CardGeoLocation(Base):
    __tablename__ = 'card_geo_location'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    card_id = Column(ForeignKey('basecard.id', ondelete='CASCADE'), nullable=False, unique=True)
    lat = Column(NUMBER(asdecimal=False))
    lon = Column(NUMBER(asdecimal=False))
    record_date = Column(DateTime, nullable=False)
    last_contact_tower_date = Column(DateTime)
    status = Column(VARCHAR(50), nullable=False)

    card = relationship('Basecard')


class CardGroupToIaPool(Base):
    __tablename__ = 'card_group_to_ia_pool'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    card_group_id = Column(ForeignKey('cardgroup.id'), nullable=False)
    pool_id = Column(ForeignKey('ip_address_pool.id'), nullable=False)

    card_group = relationship('Cardgroup')
    pool = relationship('IpAddressPool')


t_card_notification = Table(
    'card_notification', metadata,
    Column('external_id', NUMBER(asdecimal=False), nullable=False),
    Column('card_id', ForeignKey('basecard.id', ondelete='CASCADE'), nullable=False),
    Column('change_date', DateTime, nullable=False),
    Column('message_code', VARCHAR(200), nullable=False),
    Column('notification_type', VARCHAR(200), nullable=False),
    Column('threshold_value', NUMBER(asdecimal=False)),
    Column('additional_id', VARCHAR(200)),
    Index('uq_card_notification', 'card_id', 'message_code', 'notification_type', 'additional_id', unique=True)
)


t_cardgrouplink = Table(
    'cardgrouplink', metadata,
    Column('card_id', ForeignKey('basecard.id', ondelete='CASCADE'), primary_key=True),
    Column('group_id', ForeignKey('cardgroup.id', ondelete='CASCADE'), nullable=False, index=True)
)


class Cardpayntfconfig(Base):
    __tablename__ = 'cardpayntfconfig'
    __table_args__ = (
        Index('uq_cardpayntfconfig', 'card_id', 'vgroup_id', unique=True),
        Index('cardpayntfconfig_inx', 'vgroup_id', 'card_id')
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    card_id = Column(ForeignKey('basecard.id'), index=True)
    vgroup_id = Column(ForeignKey('virtualgroup.id'), nullable=False)
    enable_recommended_date = Column(NUMBER(asdecimal=False))
    fixed_day_month = Column(NUMBER(asdecimal=False))
    fixed_amount = Column(NUMBER(asdecimal=False))
    account_limit = Column(NUMBER(asdecimal=False))
    account_amount = Column(NUMBER(asdecimal=False))

    card = relationship('Basecard')
    vgroup = relationship('Virtualgroup')


class ClientDiscountActivateRule(Base):
    __tablename__ = 'client_discount_activate_rule'
    __table_args__ = (
        Index('ix_cl_discount_act_rule', 'client_id', 'billservice_id'),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    client_id = Column(ForeignKey('client.id', ondelete='CASCADE'), nullable=False)
    billservice_id = Column(ForeignKey('billservice.id'))
    discount_id = Column(ForeignKey('client_discount.id'), nullable=False)
    threshold_value = Column(NUMBER(asdecimal=False), nullable=False)
    threshold_type = Column(NUMBER(asdecimal=False), nullable=False)
    measure_unit_id = Column(ForeignKey('measureunit.id'))
    currency_id = Column(ForeignKey('currency.id'))

    billservice = relationship('Billservice')
    client = relationship('Client')
    currency = relationship('Currency')
    discount = relationship('ClientDiscount')
    measure_unit = relationship('Measureunit')


class ClientDiscountEntry(Base):
    __tablename__ = 'client_discount_entry'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    client_id = Column(ForeignKey('client.id', ondelete='CASCADE'), nullable=False, index=True)
    discount_id = Column(ForeignKey('client_discount.id'), nullable=False, index=True)
    active_from = Column(DateTime, nullable=False)
    active_till = Column(DateTime, nullable=False)

    client = relationship('Client')
    discount = relationship('ClientDiscount')


class ClientInvoiceCard(Base):
    __tablename__ = 'client_invoice_card'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    client_invoice_id = Column(ForeignKey('client_invoice.id', ondelete='CASCADE'), nullable=False, index=True)
    card_id = Column(ForeignKey('basecard.id'), nullable=False, index=True)

    card = relationship('Basecard')
    client_invoice = relationship('ClientInvoice')


class DiscountRule(Base):
    __tablename__ = 'discount_rule'
    __table_args__ = (
        CheckConstraint('rate_percent >= 0 and rate_percent <= 100'),
        Index('uq_discount_rule', 'discount_id', 'billservice_id', unique=True)
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    discount_id = Column(ForeignKey('client_discount.id', ondelete='CASCADE'), nullable=False)
    rule_priority = Column(NUMBER(asdecimal=False), nullable=False)
    billservice_id = Column(ForeignKey('billservice.id'))
    rate_percent = Column(NUMBER(asdecimal=False), nullable=False)

    billservice = relationship('Billservice')
    discount = relationship('ClientDiscount')


class IcOpertariff(Base):
    __tablename__ = 'ic_opertariff'
    __table_args__ = (
        CheckConstraint("conn_type in ('I','O','A')"),
        Index('uq_ic_opertariff', 'sched_id', 'conn_type', 'tfbundle_id', 'ext_dir_id', unique=True)
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    sched_id = Column(ForeignKey('ic_ob_schedule.id', ondelete='CASCADE'), nullable=False)
    conn_type = Column(CHAR(1), nullable=False)
    tfbundle_id = Column(ForeignKey('ic_tfbundle.id', ondelete='CASCADE'))
    ext_dir_id = Column(NUMBER(asdecimal=False), index=True)
    mb_cost = Column(NUMBER(asdecimal=False))

    sched = relationship('IcObSchedule')
    tfbundle = relationship('IcTfbundle')


class IcTariff(Base):
    __tablename__ = 'ic_tariff'
    __table_args__ = (
        CheckConstraint("conn_type in ('I','O','A')"),
        Index('uq_ic_tariff', 'sched_id', 'conn_type', 'tfbundle_id', 'dir_index', unique=True)
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    sched_id = Column(ForeignKey('ic_ob_schedule.id', ondelete='CASCADE'), nullable=False)
    operator_id = Column(ForeignKey('ic_operator.id', ondelete='CASCADE'), nullable=False, index=True)
    conn_type = Column(CHAR(1), nullable=False)
    tfbundle_id = Column(ForeignKey('ic_tfbundle.id'), index=True)
    mb_cost = Column(NUMBER(asdecimal=False))
    ext_dir_id = Column(NUMBER(asdecimal=False))
    dir_index = Column(VARCHAR(64), nullable=False)
    dir_name = Column(VARCHAR(256), nullable=False)

    operator = relationship('IcOperator')
    sched = relationship('IcObSchedule')
    tfbundle = relationship('IcTfbundle')


class IpAddres(Base):
    __tablename__ = 'ip_address'
    __table_args__ = (
        ForeignKeyConstraint(['pool_id', 'vpn_id'], ['ip_address_pool.id', 'ip_address_pool.vpn_id']),
        Index('uq_ia_address_vpn_id', 'address', 'vpn_id', unique=True)
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    address = Column(NUMBER(asdecimal=False), nullable=False)
    pool_id = Column(NUMBER(asdecimal=False), nullable=False)
    card_id = Column(ForeignKey('basecard.id'))
    vpn_id = Column(NUMBER(asdecimal=False), nullable=False)
    session_id = Column(VARCHAR(256))
    ocs_cluster_id = Column(VARCHAR(36))
    release_date = Column(DateTime)

    card = relationship('Basecard')
    pool = relationship('IpAddressPool')


class Mnloc2sgsn(Base):
    __tablename__ = 'mnloc2sgsn'
    __table_args__ = (
        Index('uq_mnloc2sgsn', 'locid', 'sgsnid', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    locid = Column(ForeignKey('mnlocation.id', ondelete='CASCADE'), nullable=False)
    sgsnid = Column(ForeignKey('sgsn.id', ondelete='CASCADE'), nullable=False, index=True)

    mnlocation = relationship('Mnlocation')
    sgsn = relationship('Sgsn')


class Mnloc2vlr(Base):
    __tablename__ = 'mnloc2vlr'
    __table_args__ = (
        Index('uq_mnloc2vlr', 'vlrid', 'locid', unique=True),
        Index('uq_mnloc2vlr_size', 'vlrid', 'locsize', unique=True)
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    locid = Column(ForeignKey('mnlocation.id', ondelete='CASCADE'), nullable=False)
    vlrid = Column(ForeignKey('vlr.id', ondelete='CASCADE'), nullable=False)
    locsize = Column(NUMBER(asdecimal=False), nullable=False)

    mnlocation = relationship('Mnlocation')
    vlr = relationship('Vlr')


class Parkvehicle(Base):
    __tablename__ = 'parkvehicle'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    created = Column(DateTime, nullable=False, server_default=text("sysdate "))
    vregnum = Column(VARCHAR(10), unique=True)
    client_id = Column(ForeignKey('client.id', ondelete='CASCADE'), index=True)
    billcard_id = Column(ForeignKey('basecard.id', ondelete='CASCADE'), index=True)
    exmpriv = Column(NUMBER(asdecimal=False))
    reg_type = Column(ForeignKey('parkvehicleregtype.id'), nullable=False, server_default=text("1 "))
    reg_details = Column(VARCHAR(1000))
    info = Column(VARCHAR(1000))

    billcard = relationship('Basecard')
    client = relationship('Client')
    parkvehicleregtype = relationship('Parkvehicleregtype')


t_payment_compensation = Table(
    'payment_compensation', metadata,
    Column('payment_schema_id', ForeignKey('paymentschema.id', ondelete='CASCADE'), nullable=False, unique=True),
    Column('rule', VARCHAR(2000), nullable=False)
)


class Paymentschemarule(Base):
    __tablename__ = 'paymentschemarule'
    __table_args__ = (
        Index('uq_psrule', 'schemaid', 'rule_order', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    schemaid = Column(ForeignKey('paymentschema.id', ondelete='CASCADE'), nullable=False)
    rule_order = Column(NUMBER(asdecimal=False), nullable=False)
    durationid = Column(ForeignKey('timeperiod.id'))
    billperiodid = Column(ForeignKey('timeperiod.id'), nullable=False)
    billperiodcost = Column(NUMBER(asdecimal=False), nullable=False)
    dailycost = Column(NUMBER(asdecimal=False))

    timeperiod = relationship('Timeperiod', primaryjoin='Paymentschemarule.billperiodid == Timeperiod.id')
    timeperiod1 = relationship('Timeperiod', primaryjoin='Paymentschemarule.durationid == Timeperiod.id')
    paymentschema = relationship('Paymentschema')


class Product(Base):
    __tablename__ = 'product'
    __table_args__ = (
        Index('ix_prod_vgservice', 'vgroupid', 'billserviceid'),
        Index('uq_prodcode', 'prodcode', 'vgroupid', unique=True),
        Index('uq_prodordercode', 'ordercode', 'vgroupid', unique=True)
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    vgroupid = Column(ForeignKey('virtualgroup.id'), nullable=False)
    prodcode = Column(VARCHAR(64), nullable=False)
    ordercode = Column(VARCHAR(64))
    prodname = Column(VARCHAR(256), nullable=False)
    prodinfo = Column(VARCHAR(1024))
    prodtypeid = Column(ForeignKey('producttype.id'), nullable=False)
    currencyid = Column(ForeignKey('currency.id'), nullable=False)
    payment_schema_id = Column(ForeignKey('paymentschema.id'))
    smprodnumber = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    billserviceid = Column(ForeignKey('billservice.id'))
    initprovstate = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("1 "))
    provrequired = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    config = Column(VARCHAR(4000))
    userstatementflag = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    incomeaccreport = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("1 "))
    enable_on_restricted_card = Column(NUMBER(asdecimal=False))
    change_prov_on_restricted = Column(NUMBER(asdecimal=False))
    autorenewwithtrafficend = Column(NUMBER(asdecimal=False))
    deleted = Column(DateTime, server_default=text("NULL"))
    provifcardnotactivated = Column(NUMBER(asdecimal=False))

    billservice = relationship('Billservice')
    currency = relationship('Currency')
    payment_schema = relationship('Paymentschema')
    producttype = relationship('Producttype')
    virtualgroup = relationship('Virtualgroup')


class Sgsn2group(Base):
    __tablename__ = 'sgsn2group'
    __table_args__ = (
        Index('uq_sgsn2group', 'sgsnid', 'groupid', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    sgsnid = Column(ForeignKey('sgsn.id', ondelete='CASCADE'), nullable=False)
    groupid = Column(ForeignKey('sgsngroup.id', ondelete='CASCADE'), nullable=False)

    sgsngroup = relationship('Sgsngroup')
    sgsn = relationship('Sgsn')


class Simcard(Base):
    __tablename__ = 'simcard'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    imsi = Column(VARCHAR(64), nullable=False, unique=True)
    account = Column(ForeignKey('account.id'), nullable=False, index=True)
    client = Column(ForeignKey('client.id'), index=True)
    contract = Column(ForeignKey('contract.id'), index=True)
    pin1 = Column(VARCHAR(16))
    pin2 = Column(VARCHAR(16))
    puk1 = Column(VARCHAR(16))
    puk2 = Column(VARCHAR(16))
    iccid = Column(VARCHAR(32), nullable=False, unique=True)
    imei = Column(VARCHAR(32))
    cardid = Column(ForeignKey('basecard.id', ondelete='CASCADE'), nullable=False, index=True)
    corpgroupid = Column(NUMBER(asdecimal=False))
    msisdn = Column(VARCHAR(32), unique=True)
    old_msisdn = Column(VARCHAR(32), index=True)
    immortal = Column(NUMBER(asdecimal=False), server_default=text("0"))
    user_name = Column(VARCHAR(300))
    clientchangedate = Column(DateTime)
    tariff_version = Column(NUMBER(asdecimal=False))
    cust_private_num = Column(VARCHAR(64))
    sim_type = Column(VARCHAR(32))
    sim_vendor = Column(VARCHAR(64))
    sim_espec = Column(VARCHAR(32))
    app_vendor = Column(VARCHAR(64))
    app_version = Column(VARCHAR(64))
    sim_actcode = Column(VARCHAR(256))

    account1 = relationship('Account')
    basecard = relationship('Basecard')
    client1 = relationship('Client')
    contract1 = relationship('Contract')


class Tariffbindextservice(Base):
    __tablename__ = 'tariffbindextservice'
    __table_args__ = (
        Index('uq_tariffbindextservice', 'planscheduleid', 'extserviceid', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    planscheduleid = Column(ForeignKey('tariffplanschedule.id'), nullable=False)
    extserviceid = Column(ForeignKey('externalservice.id'), nullable=False)
    tariffid = Column(ForeignKey('tariff.id'), nullable=False)

    externalservice = relationship('Externalservice')
    tariffplanschedule = relationship('Tariffplanschedule')
    tariff = relationship('Tariff')


class Tariffbindgpr(Base):
    __tablename__ = 'tariffbindgprs'
    __table_args__ = (
        Index('ix_tbind_gprs_ts', 'operatorid', 'planscheduleid', 'sgsngroupid'),
        Index('uq_gprs_tfb', 'planscheduleid', 'operatorid', 'accpointid', 'sgsngroupid', 'vgschedid', unique=True)
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    planscheduleid = Column(ForeignKey('tariffplanschedule.id', ondelete='CASCADE'), nullable=False)
    accpointid = Column(ForeignKey('gprs_ap.id'), nullable=False)
    operatorid = Column(ForeignKey('mnoperator.id'), nullable=False)
    sgsngroupid = Column(ForeignKey('sgsngroup.id'), nullable=False, server_default=text("0 "))
    tariffid = Column(ForeignKey('tariff.id', ondelete='CASCADE'), nullable=False, index=True)
    vgschedid = Column(ForeignKey('vgtariffschedule.id'), index=True)

    gprs_ap = relationship('GprsAp')
    mnoperator = relationship('Mnoperator')
    tariffplanschedule = relationship('Tariffplanschedule')
    sgsngroup = relationship('Sgsngroup')
    tariff = relationship('Tariff')
    vgtariffschedule = relationship('Vgtariffschedule')


class Tariffbindgprs2(Base):
    __tablename__ = 'tariffbindgprs2'
    __table_args__ = (
        Index('uq_gprs_tfb2', 'planscheduleid', 'locid', 'accpointid', 'vgschedid', unique=True),
        Index('ix_tbind_gprs2_ts', 'locid', 'planscheduleid')
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    planscheduleid = Column(ForeignKey('tariffplanschedule.id', ondelete='CASCADE'), nullable=False)
    accpointid = Column(ForeignKey('gprs_ap.id'), nullable=False)
    locid = Column(ForeignKey('mnlocation.id'), nullable=False)
    tariffid = Column(ForeignKey('tariff.id', ondelete='CASCADE'), nullable=False, index=True)
    vgschedid = Column(ForeignKey('vgtariffschedule.id'), index=True)

    gprs_ap = relationship('GprsAp')
    mnlocation = relationship('Mnlocation')
    tariffplanschedule = relationship('Tariffplanschedule')
    tariff = relationship('Tariff')
    vgtariffschedule = relationship('Vgtariffschedule')


class Tariffbindmcall(Base):
    __tablename__ = 'tariffbindmcall'
    __table_args__ = (
        CheckConstraint("homeSubsMode in ('H','F','A')"),
        CheckConstraint("redirectMode in ('R','D','A')"),
        Index('uq_mcall_tfb', 'planscheduleid', 'locid', 'bzoneid', 'billserviceid', 'redirectmode', 'homesubsmode', 'vgschedid', unique=True),
        Index('ix_tbind_mcall_ts', 'bzoneid', 'locid', 'planscheduleid', 'billserviceid')
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    planscheduleid = Column(ForeignKey('tariffplanschedule.id', ondelete='CASCADE'), nullable=False)
    locid = Column(ForeignKey('mnlocation.id'), nullable=False)
    bzoneid = Column(ForeignKey('tariffzone.id', ondelete='CASCADE'), nullable=False)
    billserviceid = Column(NUMBER(asdecimal=False), nullable=False)
    modrulea = Column(VARCHAR(64))
    modruleb = Column(VARCHAR(64))
    tariffid = Column(ForeignKey('tariff.id', ondelete='CASCADE'), nullable=False, index=True)
    redirectmode = Column(CHAR(1), nullable=False, server_default=text("'A' "))
    homesubsmode = Column(CHAR(1), nullable=False, server_default=text("'A' "))
    vgschedid = Column(ForeignKey('vgtariffschedule.id'), index=True)

    tariffzone = relationship('Tariffzone')
    mnlocation = relationship('Mnlocation')
    tariffplanschedule = relationship('Tariffplanschedule')
    tariff = relationship('Tariff')
    vgtariffschedule = relationship('Vgtariffschedule')


class Tariffbindparking(Base):
    __tablename__ = 'tariffbindparking'
    __table_args__ = (
        Index('uq_tariffbindparking', 'planscheduleid', 'parkzoneid', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    planscheduleid = Column(NUMBER(asdecimal=False), nullable=False)
    parkzoneid = Column(NUMBER(asdecimal=False), nullable=False)
    tariffid = Column(ForeignKey('tariff.id', ondelete='CASCADE'), nullable=False, index=True)

    tariff = relationship('Tariff')


class Tariffbindsm(Base):
    __tablename__ = 'tariffbindsms'
    __table_args__ = (
        CheckConstraint("homeSubsMode in ('H','F','A')"),
        Index('uq_sms_tfb', 'planscheduleid', 'locid', 'bzoneid', 'homesubsmode', 'vgschedid', unique=True),
        Index('ix_tbind_sms_ts', 'bzoneid', 'locid', 'planscheduleid')
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    planscheduleid = Column(ForeignKey('tariffplanschedule.id', ondelete='CASCADE'), nullable=False)
    locid = Column(ForeignKey('mnlocation.id'), nullable=False)
    bzoneid = Column(ForeignKey('tariffzone.id'), nullable=False)
    tariffid = Column(ForeignKey('tariff.id', ondelete='CASCADE'), nullable=False, index=True)
    homesubsmode = Column(CHAR(1), nullable=False, server_default=text("'A' "))
    vgschedid = Column(ForeignKey('vgtariffschedule.id'), index=True)

    tariffzone = relationship('Tariffzone')
    mnlocation = relationship('Mnlocation')
    tariffplanschedule = relationship('Tariffplanschedule')
    tariff = relationship('Tariff')
    vgtariffschedule = relationship('Vgtariffschedule')


class TariffplanTfentry(Base):
    __tablename__ = 'tariffplan_tfentry'
    __table_args__ = (
        Index('uq_tplan_tfentry', 'planid', 'tariffid', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    planid = Column(ForeignKey('tariffplan.id', ondelete='CASCADE'), nullable=False)
    tariffid = Column(ForeignKey('tariff.id', ondelete='CASCADE'), nullable=False, index=True)
    isshared = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))

    tariffplan = relationship('Tariffplan')
    tariff = relationship('Tariff')


class Tariffplanschedservice(Base):
    __tablename__ = 'tariffplanschedservice'
    __table_args__ = (
        Index('uq_tariffplanschedservice', 'planscheduleid', 'billservice', unique=True),
        {'comment': 'Заполняется автоматически, используется для фильтрации наборов тарифов в момент поиска'}
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    billservice = Column(ForeignKey('billservice.id'), nullable=False)
    planscheduleid = Column(ForeignKey('tariffplanschedule.id', ondelete='CASCADE'), nullable=False)

    billservice1 = relationship('Billservice')
    tariffplanschedule = relationship('Tariffplanschedule')


class TrgActionQueue(Base):
    __tablename__ = 'trg_action_queue'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    trigger_id = Column(ForeignKey('trg_record.id', ondelete='CASCADE'), nullable=False)
    next_try = Column(DateTime, nullable=False)
    attempt_count = Column(NUMBER(asdecimal=False))
    card_id = Column(ForeignKey('basecard.id', ondelete='CASCADE'), nullable=False, index=True)
    record_date = Column(DateTime, nullable=False)

    card = relationship('Basecard')
    trigger = relationship('TrgRecord')


class TrgBindCard(Base):
    __tablename__ = 'trg_bind_card'
    __table_args__ = (
        CheckConstraint('(CARD_ID IS NOT NULL AND CARD_GROUP_ID IS NULL) OR (CARD_ID IS NULL AND CARD_GROUP_ID IS NOT NULL)'),
        CheckConstraint('(CARD_ID IS NOT NULL AND CARD_GROUP_ID IS NULL) OR (CARD_ID IS NULL AND CARD_GROUP_ID IS NOT NULL)'),
        CheckConstraint('ONSTATE in (0,1)'),
        Index('uq_trg_bind_card', 'trigger_id', 'card_id', 'card_group_id', unique=True)
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    trigger_id = Column(ForeignKey('trg_record.id', ondelete='CASCADE'), nullable=False, index=True)
    card_id = Column(ForeignKey('basecard.id', ondelete='CASCADE'), index=True)
    card_group_id = Column(ForeignKey('cardgroup.id', ondelete='CASCADE'), index=True)
    onstate = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("1 "))

    card_group = relationship('Cardgroup')
    card = relationship('Basecard')
    trigger = relationship('TrgRecord')


class TrgCounterCard(Base):
    __tablename__ = 'trg_counter_card'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    trigger_id = Column(ForeignKey('trg_record.id', ondelete='CASCADE'), nullable=False, index=True)
    card_id = Column(ForeignKey('basecard.id', ondelete='CASCADE'), nullable=False, index=True)
    usage_start = Column(DateTime, nullable=False)
    usage_value = Column(NUMBER(asdecimal=False), nullable=False)
    enqueued = Column(TIMESTAMP)

    card = relationship('Basecard')
    trigger = relationship('TrgRecord')


class TrgLiveImsiState(Base):
    __tablename__ = 'trg_live_imsi_state'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    card_id = Column(ForeignKey('basecard.id', ondelete='CASCADE'), nullable=False, index=True)
    state = Column(NUMBER(asdecimal=False), nullable=False)
    change_date = Column(DateTime, nullable=False)

    card = relationship('Basecard')


class TrgLocker(Base):
    __tablename__ = 'trg_locker'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    trigger_id = Column(ForeignKey('trg_record.id', ondelete='CASCADE'), nullable=False, index=True)
    card_id = Column(ForeignKey('basecard.id', ondelete='CASCADE'), nullable=False, index=True)
    bill_service = Column(ForeignKey('billservice.id'), nullable=False)
    lock_date = Column(DateTime, nullable=False)

    billservice = relationship('Billservice')
    card = relationship('Basecard')
    trigger = relationship('TrgRecord')


class AccfileCpProduct(Base):
    __tablename__ = 'accfile_cp_product'
    __table_args__ = (
        Index('uq_accfile_cp_product', 'product_id', 'vgroup_id', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    vgroup_id = Column(NUMBER(asdecimal=False), nullable=False)
    product_id = Column(ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    autoorderflag = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    actonfirstusage = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    ussdcontrol = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("1 "))
    systemcontrol = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("1 "))
    webcontrol = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))

    product = relationship('Product')


class Accfileproduct(Base):
    __tablename__ = 'accfileproduct'
    __table_args__ = (
        Index('uq_accfileprod_code', 'accfileid', 'ordercode', unique=True),
        Index('uq_accfileprod', 'accfileid', 'prodid', unique=True)
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    accfileid = Column(ForeignKey('accountingfile.id'), nullable=False)
    prodid = Column(ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    ordercode = Column(VARCHAR(64), nullable=False)
    info = Column(VARCHAR(1024))
    activefrom = Column(DateTime, nullable=False, server_default=text("sysdate "))
    expired = Column(DateTime)
    autoorderflag = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    actonfirstusage = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    ussdcontrol = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("1 "))
    systemcontrol = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("1 "))
    webcontrol = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    config = Column(VARCHAR(4000))

    accountingfile = relationship('Accountingfile')
    product = relationship('Product')


class Accountcommandqueue(Base):
    __tablename__ = 'accountcommandqueue'
    __table_args__ = (
        Index('uq_acccommandqueue', 'account_id', 'type', 'card_id', 'client_id', 'closed', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    initiator = Column(VARCHAR(256), nullable=False)
    created = Column(DateTime, nullable=False)
    next_try = Column(DateTime, nullable=False)
    type = Column(NUMBER(asdecimal=False), nullable=False)
    src_account_id = Column(ForeignKey('account.id', ondelete='CASCADE'), nullable=False)
    account_id = Column(ForeignKey('account.id', ondelete='CASCADE'))
    card_id = Column(ForeignKey('simcard.id', ondelete='CASCADE'))
    client_id = Column(ForeignKey('client.id', ondelete='CASCADE'))
    modes = Column(VARCHAR(400))
    attempt_count = Column(NUMBER(asdecimal=False))
    closed = Column(TIMESTAMP)
    status = Column(NUMBER(asdecimal=False))
    err_desc = Column(VARCHAR(256))

    account = relationship('Account', primaryjoin='Accountcommandqueue.account_id == Account.id')
    card = relationship('Simcard')
    client = relationship('Client')
    src_account = relationship('Account', primaryjoin='Accountcommandqueue.src_account_id == Account.id')


t_card_activity = Table(
    'card_activity', metadata,
    Column('card_id', ForeignKey('simcard.id', ondelete='CASCADE'), nullable=False),
    Column('type_id', NUMBER(asdecimal=False), nullable=False),
    Column('last_activity', DateTime, index=True),
    Column('change_avg_time', DateTime),
    Column('avg_time_minutes', NUMBER(asdecimal=False)),
    Index('uq_card_activity', 'card_id', 'type_id', unique=True)
)


class Cardpayntfqueue(Base):
    __tablename__ = 'cardpayntfqueue'
    __table_args__ = (
        Index('cardpayntfqueue_inx', 'card_id', 'event_type', 'bill_date'),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    card_id = Column(ForeignKey('basecard.id'), nullable=False)
    config_id = Column(ForeignKey('cardpayntfconfig.id'), nullable=False)
    bill_date = Column(DateTime)
    amount = Column(NUMBER(asdecimal=False), nullable=False)
    next_try = Column(DateTime, nullable=False)
    state = Column(NUMBER(asdecimal=False), nullable=False)
    event_type = Column(NUMBER(asdecimal=False), nullable=False)

    card = relationship('Basecard')
    config = relationship('Cardpayntfconfig')


class Discountautoorder(Base):
    __tablename__ = 'discountautoorder'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    accfileid = Column(ForeignKey('accountingfile.id', ondelete='CASCADE'), nullable=False, index=True)
    active_from = Column(DateTime, nullable=False)
    active_till = Column(DateTime, nullable=False)
    rule_info = Column(VARCHAR(1024))
    client_type = Column(ForeignKey('clienttype.id'), server_default=text("null"))
    paym_system = Column(ForeignKey('paymentsystemtype.id'), nullable=False, server_default=text("0 "))
    min_paym_value = Column(NUMBER(asdecimal=False), nullable=False)
    prod_to_order = Column(ForeignKey('product.id', ondelete='CASCADE'), nullable=False, index=True)

    accountingfile = relationship('Accountingfile')
    clienttype = relationship('Clienttype')
    paymentsystemtype = relationship('Paymentsystemtype')
    product = relationship('Product')


class Productactivationcode(Base):
    __tablename__ = 'productactivationcode'
    __table_args__ = (
        Index('ix_pacode_part_iter', 'partition', 'iteration_num'),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    activation_code = Column(VARCHAR(200), nullable=False, unique=True)
    partition = Column(VARCHAR(1000), nullable=False)
    productid = Column(ForeignKey('product.id'), nullable=False)
    generated_dt = Column(DateTime, nullable=False)
    expired_dt = Column(DateTime)
    used_dt = Column(DateTime)
    state = Column(ForeignKey('productactivationcodestate.id'), nullable=False)
    iteration_num = Column(NUMBER(asdecimal=False), nullable=False)

    product = relationship('Product')
    productactivationcodestate = relationship('Productactivationcodestate')


class Productpackage(Base):
    __tablename__ = 'productpackage'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    productid = Column(ForeignKey('product.id', ondelete='CASCADE'), nullable=False, index=True)
    billservice = Column(ForeignKey('billservice.id'), nullable=False)
    packagepriority = Column(NUMBER(asdecimal=False), nullable=False)
    packagename = Column(VARCHAR(128), nullable=False)
    usageperiodid = Column(ForeignKey('timeperiod.id'))
    usagecost = Column(NUMBER(asdecimal=False), nullable=False)
    tariffplanid = Column(ForeignKey('tariffplan.id'), nullable=False, index=True)
    billvolumeid = Column(NUMBER(asdecimal=False), nullable=False)
    totalvolume = Column(NUMBER(asdecimal=False))
    usageresetlimit = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    usagemode = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    services = Column(VARCHAR(4000))
    state = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("1 "))
    ntfppackpercentthrshlds = Column(VARCHAR(200))
    maxtransferpackagevol = Column(NUMBER(asdecimal=False))

    billservice1 = relationship('Billservice')
    product = relationship('Product')
    tariffplan = relationship('Tariffplan')
    timeperiod = relationship('Timeperiod')


class Productsubscription(Base):
    __tablename__ = 'productsubscription'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    orderdate = Column(DateTime, nullable=False)
    order_no = Column(VARCHAR(32), nullable=False)
    product_id = Column(ForeignKey('product.id'), nullable=False, index=True)
    order_cost = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    currencyid = Column(ForeignKey('currency.id'), nullable=False)
    startbilldate = Column(DateTime)
    account_id = Column(ForeignKey('account.id'), nullable=False, index=True)
    client_id = Column(ForeignKey('client.id'), index=True)
    targetdesc = Column(VARCHAR(512))
    payment_schema_id = Column(ForeignKey('paymentschema.id'), nullable=False)
    nextbilldate = Column(DateTime, nullable=False, index=True)
    lastbillamount = Column(NUMBER(asdecimal=False), nullable=False)
    totalbillamount = Column(NUMBER(asdecimal=False), nullable=False)
    lastattempnumber = Column(NUMBER(asdecimal=False))
    payruleid = Column(ForeignKey('paymentschemarule.id'), index=True)
    payrulestart = Column(DateTime)
    state = Column(ForeignKey('productsubsstate.id'), nullable=False)
    cardid = Column(ForeignKey('basecard.id'), index=True)
    accfileid = Column(ForeignKey('accountingfile.id'))
    lastbilldate = Column(DateTime)
    last_error = Column(VARCHAR(64))
    nextperiodcost = Column(NUMBER(asdecimal=False))
    provisioning = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    uservars = Column(VARCHAR(4000))
    xgatelogin_id = Column(NUMBER(asdecimal=False))
    compensationcost = Column(NUMBER(asdecimal=False))
    truncatedperiod = Column(NUMBER(asdecimal=False))
    isneedsendlicfeeprediction = Column(NUMBER(asdecimal=False))
    order_unpaid = Column(NUMBER(asdecimal=False))

    accountingfile = relationship('Accountingfile')
    account = relationship('Account')
    basecard = relationship('Basecard')
    client = relationship('Client')
    currency = relationship('Currency')
    payment_schema = relationship('Paymentschema')
    paymentschemarule = relationship('Paymentschemarule')
    product = relationship('Product')
    productsubsstate = relationship('Productsubsstate')


class Simcardimsi(Base):
    __tablename__ = 'simcardimsi'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    imsi = Column(VARCHAR(20), nullable=False, unique=True)
    simcardid = Column(ForeignKey('simcard.id', ondelete='CASCADE'), nullable=False)
    norder = Column(NUMBER(asdecimal=False), nullable=False)
    tariffplanid = Column(NUMBER(asdecimal=False))
    state = Column(NUMBER(asdecimal=False), nullable=False)
    regtime = Column(DateTime)

    simcard = relationship('Simcard')


class Simnumber(Base):
    __tablename__ = 'simnumber'
    __table_args__ = (
        CheckConstraint("own_type in ('OWN','MNP')"),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    pnumber = Column(VARCHAR(32), nullable=False, unique=True)
    simcardid = Column(ForeignKey('simcard.id'), index=True)
    numbertype = Column(ForeignKey('simnumbertype.id'), nullable=False)
    norder = Column(NUMBER(asdecimal=False), nullable=False)
    nstate = Column(NUMBER(asdecimal=False))
    released = Column(DateTime)
    rate_id = Column(ForeignKey('simnumberrate.id'), nullable=False, index=True)
    vgroup_id = Column(ForeignKey('virtualgroup.id'), nullable=False, index=True)
    own_type = Column(CHAR(3), nullable=False, server_default=text("'OWN' "))
    operstate = Column(ForeignKey('simnumberstate.id'), nullable=False)
    last_update = Column(DateTime, server_default=text("sysdate"))

    simnumbertype = relationship('Simnumbertype')
    simnumberstate = relationship('Simnumberstate')
    rate = relationship('Simnumberrate')
    simcard = relationship('Simcard')
    vgroup = relationship('Virtualgroup')


class TrgCompleteaction(Base):
    __tablename__ = 'trg_completeaction'
    __table_args__ = (
        Index('uq_trg_completeaction', 'action_queue_id', 'action_id', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    action_id = Column(ForeignKey('trg_action.id', ondelete='CASCADE'), nullable=False, index=True)
    action_queue_id = Column(ForeignKey('trg_action_queue.id', ondelete='CASCADE'), nullable=False)

    action = relationship('TrgAction')
    action_queue = relationship('TrgActionQueue')


class Xgateuserprofile(Base):
    __tablename__ = 'xgateuserprofile'
    __table_args__ = (
        Index('uq_xgateuserprofile', 'vgroupid', 'profilename', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    vgroupid = Column(ForeignKey('virtualgroup.id', ondelete='CASCADE'), nullable=False)
    profilename = Column(VARCHAR(200), nullable=False)
    profileinfo = Column(VARCHAR(4000))
    maxrequestperhour = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    maxrequestperday = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    appconfig = Column(VARCHAR(4000))
    product_id = Column(ForeignKey('product.id'))

    product = relationship('Product')
    virtualgroup = relationship('Virtualgroup')


class Offlinepackageusage(Base):
    __tablename__ = 'offlinepackageusage'
    __table_args__ = (
        Index('uq_offpackusage', 'subsid', 'packageid', 'cardid', 'usagestart', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    subsid = Column(ForeignKey('productsubscription.id', ondelete='CASCADE'), nullable=False)
    packageid = Column(ForeignKey('productpackage.id'), nullable=False)
    cardid = Column(ForeignKey('simcard.id'))
    usagestart = Column(DateTime)
    usagestop = Column(DateTime)
    usagevalue = Column(NUMBER(asdecimal=False), nullable=False)
    actual_limit = Column(NUMBER(asdecimal=False))

    simcard = relationship('Simcard')
    productpackage = relationship('Productpackage')
    productsubscription = relationship('Productsubscription')


class Packageschedule(Base):
    __tablename__ = 'packageschedule'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    productid = Column(ForeignKey('product.id'), index=True)
    daytype = Column(NUMBER(asdecimal=False), nullable=False)
    timefrom = Column(NUMBER(asdecimal=False), nullable=False)
    timetill = Column(NUMBER(asdecimal=False), nullable=False)
    packageid = Column(ForeignKey('productpackage.id'), index=True)

    productpackage = relationship('Productpackage')
    product = relationship('Product')


class Packagevolumerule(Base):
    __tablename__ = 'packagevolumerule'
    __table_args__ = (
        Index('uq_package_rule', 'consumeorder', 'packageid', unique=True),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    packageid = Column(ForeignKey('productpackage.id', ondelete='CASCADE'), nullable=False)
    consumeorder = Column(NUMBER(asdecimal=False), nullable=False)
    amount = Column(NUMBER(asdecimal=False), nullable=False)
    qosp = Column(NUMBER(asdecimal=False))
    paymode = Column(ForeignKey('packagepaymode.id'), nullable=False)
    roundrule = Column(NUMBER(asdecimal=False))
    basecost = Column(NUMBER(asdecimal=False))
    tariffplanid = Column(NUMBER(asdecimal=False))

    productpackage = relationship('Productpackage')
    packagepaymode = relationship('Packagepaymode')


class Productpackageusage(Base):
    __tablename__ = 'productpackageusage'
    __table_args__ = (
        Index('ix_ppack_usage', 'subsid', 'packageid'),
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    subsid = Column(ForeignKey('productsubscription.id', ondelete='CASCADE'), nullable=False)
    packageid = Column(ForeignKey('productpackage.id'), nullable=False)
    corpitem = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    cardid = Column(ForeignKey('simcard.id'), index=True)
    usagestart = Column(DateTime)
    usagevalue = Column(NUMBER(asdecimal=False), nullable=False)
    lastusagereset = Column(DateTime)
    totalvalue = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    usageresetnumber = Column(NUMBER(asdecimal=False), nullable=False, server_default=text("0 "))
    actual_limit = Column(NUMBER(asdecimal=False))

    simcard = relationship('Simcard')
    productpackage = relationship('Productpackage')
    productsubscription = relationship('Productsubscription')


class Productrelation(Base):
    __tablename__ = 'productrelation'
    __table_args__ = (
        CheckConstraint("relation in ('>','X','S')"),
        ForeignKeyConstraint(['accfile_id', 'product_id_1'], ['accfileproduct.accfileid', 'accfileproduct.prodid'], ondelete='CASCADE'),
        ForeignKeyConstraint(['accfile_id', 'product_id_2'], ['accfileproduct.accfileid', 'accfileproduct.prodid'], ondelete='CASCADE'),
        Index('ix_productrelation_acf', 'accfile_id', 'product_id_1')
    )

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    accfile_id = Column(NUMBER(asdecimal=False), nullable=False)
    product_id_1 = Column(ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    product_id_2 = Column(ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    relation = Column(CHAR(1), nullable=False)

    accfile = relationship('Accfileproduct', primaryjoin='Productrelation.accfile_id == Accfileproduct.accfileid')
    accfile1 = relationship('Accfileproduct', primaryjoin='Productrelation.accfile_id == Accfileproduct.accfileid')
    product = relationship('Product', primaryjoin='Productrelation.product_id_1 == Product.id')
    product1 = relationship('Product', primaryjoin='Productrelation.product_id_2 == Product.id')


class Xgatelogin(Base):
    __tablename__ = 'xgatelogin'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    created = Column(DateTime)
    registrant = Column(VARCHAR(128))
    login = Column(VARCHAR(64), unique=True)
    passw = Column(VARCHAR(256))
    groupid = Column(ForeignKey('virtualgroup.id', ondelete='CASCADE'), nullable=False, index=True)
    state = Column(NUMBER(asdecimal=False))
    info = Column(VARCHAR(2000))
    xrole_id = Column(ForeignKey('xgaterole.id'))
    targetcompanyid = Column(ForeignKey('company.id', ondelete='CASCADE'))
    profileid = Column(ForeignKey('xgateuserprofile.id', ondelete='SET NULL'), index=True)
    appdata = Column(VARCHAR(4000))
    client_id = Column(ForeignKey('client.id', ondelete='CASCADE'), index=True)
    login_lcase = Column(VARCHAR(64), nullable=False, unique=True)

    client = relationship('Client')
    virtualgroup = relationship('Virtualgroup')
    xgateuserprofile = relationship('Xgateuserprofile')
    company = relationship('Company')
    xrole = relationship('Xgaterole')


class ClientUiMsgUnread(Base):
    __tablename__ = 'client_ui_msg_unread'

    id = Column(NUMBER(asdecimal=False), primary_key=True)
    login_id = Column(ForeignKey('xgatelogin.id', ondelete='CASCADE'), nullable=False, index=True)
    msg_id = Column(ForeignKey('client_ui_msg.id', ondelete='CASCADE'), nullable=False, index=True)

    login = relationship('Xgatelogin')
    msg = relationship('ClientUiMsg')
