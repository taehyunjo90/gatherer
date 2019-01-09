from Apis import Login

from Apis import ForeignFutures
from Apis import ForeignOption

from Apis import KoreanFutures
from Apis import KoreanOption

from Apis import KoreanKospi
from Apis import KoreanKosdaq

import pythoncom

if __name__ == "__main__":

    # 로그인
    Login.do_login(True)

    # 해외 선물
    ffh, ffc = ForeignFutures.getGatheringInstance()

    # 국내 선물
    kfh, kfc = KoreanFutures.getGatheringInstance()

    # 국내 옵션
    koh, koc = KoreanOption.getGatheringInstance()

    # 국내 주식(코스피)
    ksdh, ksdc, ksdco = KoreanKosdaq.getGatheringInstance()

    # 국내 주식(코스닥)
    ksph, kspc, kspco = KoreanKospi.getGatheringInstance()

    while True:
        pythoncom.PumpWaitingMessages()


