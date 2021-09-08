import attr
from typing import List

from models.services.base import BaseModelOperations, convert_to, atr
from lib.utils import Fake


fake = Fake()


@attr.s
class Card(BaseModelOperations):
    iccid: str = atr(converter=convert_to(int))
    msisdn: str = atr(converter=convert_to(str))
    imsi: str = atr(converter=convert_to(str))
    imei: str = atr(converter=convert_to(str))
    cardId: int = atr(converter=convert_to(int))


@attr.s
class CardOperativeStateChangeJournal(BaseModelOperations):
    virtualGroupId: int = atr(converter=convert_to(int))
    accountingFileId: int = atr(converter=convert_to(int))
    cardId: int = atr(converter=convert_to(int))
    iccId: str = atr(converter=convert_to(str))
    oldOperativeState: str = atr(converter=convert_to(str))
    newOperativeState: str = atr(converter=convert_to(str))
    id: int = atr(converter=convert_to(int))
    recordDate: str = atr(converter=convert_to(str))
    accountingFileName: str = atr(converter=convert_to(str))


@attr.s
class NumberState(BaseModelOperations):
    """
    https://wiki.protei.ru/doku.php?id=protei:cpe:billing:xgate:dict
    Состояние номера
    """
    id: int = atr(converter=int)
    code: str = atr(converter=str)


@attr.s
class CardStateInfo(BaseModelOperations):
    numberState: NumberState = atr()
    cardState: str = atr(converter=convert_to(str))
    cardOperativeState: str = atr(converter=convert_to(str))
    cardExpiredDt: str = atr(converter=convert_to(str))
    cardSaledDt: str = atr(converter=convert_to(str))
    cardActivatedDt: str = atr(converter=convert_to(str))
    cardFirstTransactionDt: str = atr(converter=convert_to(str))
    accountCreatedDt: str = atr(converter=convert_to(str))
    accountFirstTransactionDt: str = atr(converter=convert_to(str))
    accountLastTransactionDt: str = atr(converter=convert_to(str))
    cardOperativeStateChangeHistory: List[CardOperativeStateChangeJournal] = atr()
    pin1: str = atr(converter=convert_to(str))
    pin2: str = atr(converter=convert_to(str))
    puk1: str = atr(converter=convert_to(str))
    puk2: str = atr(converter=convert_to(str))


@attr.s
class Lang(BaseModelOperations):
    id: int = atr(converter=int)
    langName: str = atr(converter=str)
    langInfo: str = atr(converter=str)
    langCode: str = atr(converter=convert_to(str))


@attr.s
class ReplaceCardResult(BaseModelOperations):
    msisdn: str = atr(converter=convert_to(str))
    imsi: str = atr(converter=convert_to(str))
    iccid: str = atr(converter=convert_to(str))
    pin1: str = atr(converter=convert_to(str))
    pin2: str = atr(converter=convert_to(str))
    puk1: str = atr(converter=convert_to(str))
    puk2: str = atr(converter=convert_to(str))
    batchNumber: str = atr(converter=convert_to(str))
    simType: str = atr(converter=convert_to(str))
    simVendor: str = atr(converter=convert_to(str))
    eSpec: str = atr(converter=convert_to(str))
    appVendor: str = atr(converter=convert_to(str))
    appVersion: str = atr(converter=convert_to(str))
    simCardActivationCode: str = atr(converter=str)


@attr.s
class CardInfo(BaseModelOperations):
    cardId: str = atr(converter=convert_to(str))
    status: str = atr(converter=convert_to(str))


@attr.s
class FailedCards(BaseModelOperations):
    failedCards: List[CardInfo] = atr()


@attr.s
class HLRProfileInfo(BaseModelOperations):
    requestMsisdn: str = atr(converter=str)


@attr.s
class HLRProfileInfo(BaseModelOperations):
    requestMsisdn: str = atr(converter=str)
    hlrImsiByMsisdnRequest: str = atr(converter=str)
    statusByMsisdnRequest: str = atr(converter=str)
    requestImsi: str = atr(converter=str)
    hlrMsisdnByImsiRequest: str = atr(converter=str)
    statusByImsiRequest: str = atr(converter=str)


@attr.s
class RoamingInfo(BaseModelOperations):
    vlr: str = atr(converter=str)
    registeredDt: str = atr(converter=str)
    isPurged: str = atr(converter=str)
    purgedDt: str = atr(converter=str)


@attr.s
class RoamingSgsnInfo(BaseModelOperations):
    sgsn: str = atr(converter=str)
    registeredDt: str = atr(converter=str)
    isPurged: str = atr(converter=str)
    purgedDt: str = atr(converter=str)
    dmMmeHost: str = atr(converter=str)
    dmMmeRealm: str = atr(converter=str)
    isPurgedEpsMme: str = atr(converter=str)
    purgedEpsMmeDt: str = atr(converter=str)
    isPurgedEpsSgsn: str = atr(converter=str)
    purgedEpsSgsnDt: str = atr(converter=str)


@attr.s
class HLRRegistrationInfo(BaseModelOperations):
    roamingInfo: RoamingInfo = atr()
    roamingSgsnInfo: RoamingSgsnInfo = atr()


@attr.s
class CardInfoCounter(BaseModelOperations):
    moneyExpenses: float = atr(converter=float)
    moneyLimit: float = atr(converter=float)
    currencyCode: str = atr(converter=str)
    periodStart: str = atr(converter=str)
    periodEnd: str = atr(converter=str)
    enabledNotification: bool = atr(converter=bool)


@attr.s
class Long(BaseModelOperations):
    long: int = atr(converter=int)
    resultObject: CardInfoCounter = atr()


@attr.s
class Entry(BaseModelOperations):
    entry: List[Long] = atr()


@attr.s
class CardActivityInfo(BaseModelOperations):
    cardId: int = atr(converter=int)
    msisdn: str = atr(converter=str)
    imsi: str = atr(converter=str)
    lastActivity: str = atr(converter=str)
    changeAvgTime: str = atr(converter=str)
    avgTimeInMinutes: int = atr(converter=int)


@attr.s
class Results(BaseModelOperations):
    results: List[CardActivityInfo] = atr()


@attr.s
class ClientInvoiceShortInfo(BaseModelOperations):
    invoiceId: int = atr(converter=int)
    accountId: int = atr(converter=int)
    clientId: int = atr(converter=int)
    unpaidAmount: float = atr(converter=float)
    currencyCode: str = atr(converter=str)


@attr.s
class ActualCardStateInfo(BaseModelOperations):
    state: str = atr(converter=str)
    cardOperativeStateChangeHistory: List[CardOperativeStateChangeJournal] = atr()
    billingMode: str = atr(converter=str)
    accountBalance: float = atr(converter=float)
    accountLimit: float = atr(converter=float)
    sumUnpaidInvoices: float = atr(converter=float)
    currencyCode: str = atr(converter=str)
    unpaidInvoices: List[ClientInvoiceShortInfo] = atr()


@attr.s
class Long(BaseModelOperations):
    long: [int] = atr()


@attr.s
class BaseCard(BaseModelOperations):
    id: int = atr(eq=False, converter=convert_to(int))
    cardtype: int = atr(converter=convert_to(int))
    vgroupid: int = atr(converter=convert_to(int))
    accfileid: int = atr(converter=convert_to(int))
    state: int = atr(converter=convert_to(int))
    cardnumber: str = atr(default=fake.uuid4(), converter=str)


if __name__ == "__main__":
    # test = Card()
    # a = NumberState(id=1, code="1")
    # b = CardOperativeStateChangeJournal()
    # a = CardInfo(cardId="123", status="NOT FOUND")
    # test = FailedCards([a])
    a = [1, 2, 3]
    test = Long(a)
    print(test.to_xml(root="test"))
    # test = CardStateInfo(numberState=a, cardOperativeStateChangeHistory=[b])
    print(test)
    print(test.to_dict())
    print(test.to_xml(root="test"))