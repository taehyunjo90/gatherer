from Apis import ForeignFutures
from Apis import ForeignOption

from Apis import KoreanFutures
from Apis import KoreanOption

from Apis import KoreanKospi
from Apis import KoreanKosdaq

from Apis import Login

import pythoncom

def doKospi():
    Login.do_login(True)

    # 국내 주식(코스피)
    ksdh, ksdc, ksdco = KoreanKosdaq.getGatheringInstance()
    while True:
        pythoncom.PumpWaitingMessages()

def doKosdaq():
    Login.do_login(True)
    # 국내 주식(코스닥)
    ksph, kspc, kspco = KoreanKospi.getGatheringInstance()
    while True:
        pythoncom.PumpWaitingMessages()

def doKoreanDerivatiesAndForeignFutures():
    Login.do_login(True)
    # 국내 선물
    kfh, kfc = KoreanFutures.getGatheringInstance()
    # 국내 옵션
    koh, koc = KoreanOption.getGatheringInstance()
    # 해외 선물
    ffh, ffc = ForeignFutures.getGatheringInstance()
    while True:
        pythoncom.PumpWaitingMessages()