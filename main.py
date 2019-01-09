from Apis import Login
from Apis import ForeignFutures
from Apis import ForeignOption
from Apis import KoreanFutures

import pythoncom

if __name__ == "__main__":

    Login.do_login(True)

    df_info = KoreanFutures.getWholeKoreanFuturesInfo()
    list_futcode = df_info.loc[:, '단축코드'] # 전 종목 가져오기
    list_futcode = list(list_futcode)

    kfh, kfc = KoreanFutures.getForeignFuturesRealData(list_futcode)

    while True:
        pythoncom.PumpWaitingMessages()

