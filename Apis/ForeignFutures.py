from Apis.Abstract import *

module_logger = logging.getLogger('Apis.ForeignFutures')
module_logger.setLevel(logging.INFO)
module_logger.addHandler(ch)

class ForeignFuturesInfo(AbsTROccurs):

    def __init__(self):
        AbsTROccurs.__init__(self) # 추상화 클래스 생성자
        self.code = "o3101" #TR Code

    def OnReceiveData(self, tr_code):
        self.is_data_received = True
        self.count = self.GetBlockCount("o3101OutBlock")
        self.total_data = []

        for i in range(self.count):
            tmp_data = [
            self.GetFieldData("o3101OutBlock", "Symbol", i),
            self.GetFieldData("o3101OutBlock", "SymbolNm", i),
            self.GetFieldData("o3101OutBlock", "ApplDate", i),
            self.GetFieldData("o3101OutBlock", "BscGdsCd", i),
            self.GetFieldData("o3101OutBlock", "BscGdsNm", i),
            self.GetFieldData("o3101OutBlock", "ExchCd", i),
            self.GetFieldData("o3101OutBlock", "ExchNm", i),
            self.GetFieldData("o3101OutBlock", "CrncyCd", i),
            self.GetFieldData("o3101OutBlock", "NotaCd", i),
            self.GetFieldData("o3101OutBlock", "UntPrc", i),
            self.GetFieldData("o3101OutBlock", "MnChgAmt", i),
            self.GetFieldData("o3101OutBlock", "RgltFctr", i),
            self.GetFieldData("o3101OutBlock", "CtrtPrAmt", i),
            self.GetFieldData("o3101OutBlock", "GdsCd", i),
            self.GetFieldData("o3101OutBlock", "LstngYr", i),
            self.GetFieldData("o3101OutBlock", "LstngM", i),
            self.GetFieldData("o3101OutBlock", "EcPrc", i),
            self.GetFieldData("o3101OutBlock", "DlStrtTm", i),
            self.GetFieldData("o3101OutBlock", "DlEndTm", i),
            self.GetFieldData("o3101OutBlock", "DlPsblCd", i),
            self.GetFieldData("o3101OutBlock", "MgnCltCd", i),
            self.GetFieldData("o3101OutBlock", "OpngMgn", i),
            self.GetFieldData("o3101OutBlock", "MntncMgn", i),
            self.GetFieldData("o3101OutBlock", "OpngMgnR", i),
            self.GetFieldData("o3101OutBlock", "MntncMgnR", i),
            self.GetFieldData("o3101OutBlock", "DotGb", i)
            ]
            self.total_data.append(tmp_data)
            df_total_data = pd.DataFrame(self.total_data)
            df_total_data.columns = ['종목코드',
                                     '종목명',
                                     '종목배치일(한국)',
                                     '기초상품코드',
                                     '기초상품명',
                                     '거래소코드',
                                     '거래소명',
                                     '기준통화코드',
                                     '진법구분코드',
                                     '호가단위가격',
                                     '최소가격변동금액',
                                     '가격조정계수',
                                     '계약당금액',
                                     '상품구분코드',
                                     '월물(년)',
                                     '월물(월)',
                                     '정산가격',
                                     '거래시작시간',
                                     '거래종료시간',
                                     '거래가능구분코드',
                                     '증거금징수구분코드',
                                     '개시증거금',
                                     '유지증거금',
                                     '개시증거금율',
                                     '유지증거금율',
                                     '유효소수점자리수']

            self.df_received_data = df_total_data

    def start(self):
        AbsTROccurs.start(self, self.code)

    def singleRequest(self, *args):
        gubun = args[0]

        self.SetFieldData("o3101InBlock", "gubun", 0, gubun)
        self.Request(False)



class ForeignFuturesHoga(AbsReal):  ## 해외 선물 호가
    def __init__(self):
        AbsReal.__init__(self)
        self._open_file()
        self.code = "OVH"

    def OnReceiveRealData(self, tr_code):  # event handler
        """
        이베스트 서버에서 이벤트를 받으면 실행되는 event handler
        """

        self.data = []

        self.data.append(self.GetFieldData("OutBlock", "symbol"))
        self.data.append(time.time())  # Computer Time
        self.data.append(self.GetFieldData("OutBlock", "hotime"))

        for i in range(1, 6):  # 1~5
            self.data.append(self.GetFieldData("OutBlock", "offerho" + str(i)))
        for i in range(1, 6):  # 1~5
            self.data.append(self.GetFieldData("OutBlock", "offerrem" + str(i)))
        for i in range(1, 6):  # 1~5
            self.data.append(self.GetFieldData("OutBlock", "offerno" + str(i)))

        for i in range(1, 6):  # 1~5
            self.data.append(self.GetFieldData("OutBlock", "bidho" + str(i)))
        for i in range(1, 6):  # 1~5
            self.data.append(self.GetFieldData("OutBlock", "bidrem" + str(i)))
        for i in range(1, 6):  # 1~5
            self.data.append(self.GetFieldData("OutBlock", "bidno" + str(i)))

        self.data.append(self.GetFieldData("OutBlock", "totoffercnt"))
        self.data.append(self.GetFieldData("OutBlock", "totbidcnt"))
        self.data.append(self.GetFieldData("OutBlock", "totofferrem"))
        self.data.append(self.GetFieldData("OutBlock", "totbidrem"))

        # if self.data[0] == "HSIF19":
        #     print(self.data)

        self.writer.writerow(self.data)
        self.f.flush()

    def _open_file(self):  # I/O
        AbsReal._open_file(self, "FOREIGNFUTURES", "FOREIGNFUTURES_TOTAL")

    def start(self):
        AbsReal.start(self, self.code)


class ForeignFuturesChegyul(AbsReal):  ## 해외선물 체결

    def __init__(self):
        AbsReal.__init__(self)
        self._open_file()
        self.code = "OVC"

    def OnReceiveRealData(self, tr_code):  # event handler
        self.data = []

        self.data.append(self.GetFieldData("OutBlock", "symbol"))
        self.data.append(time.time())
        self.data.append(self.GetFieldData("OutBlock", "ovsdate"))
        self.data.append(self.GetFieldData("OutBlock", "kordate"))
        self.data.append(self.GetFieldData("OutBlock", "trdtm"))
        self.data.append(self.GetFieldData("OutBlock", "kortm"))
        self.data.append(self.GetFieldData("OutBlock", "curpr"))
        self.data.append(self.GetFieldData("OutBlock", "ydiffpr"))
        self.data.append(self.GetFieldData("OutBlock", "ydiffSign"))
        self.data.append(self.GetFieldData("OutBlock", "open"))
        self.data.append(self.GetFieldData("OutBlock", "high"))
        self.data.append(self.GetFieldData("OutBlock", "low"))
        self.data.append(self.GetFieldData("OutBlock", "chgrate"))
        self.data.append(self.GetFieldData("OutBlock", "trdq"))
        self.data.append(self.GetFieldData("OutBlock", "totq"))
        self.data.append(self.GetFieldData("OutBlock", "cgubun"))
        self.data.append(self.GetFieldData("OutBlock", "mdvolume"))
        self.data.append(self.GetFieldData("OutBlock", "msvolume"))
        self.data.append(self.GetFieldData("OutBlock", "ovsmkend"))

        # if self.data[0] == "HSIF19":
        #     print(self.data)

        self.writer.writerow(self.data)
        self.f.flush()

    def _open_file(self):  # I/O
        AbsReal._open_file(self, "FOREIGNFUTURES", "FOREIGNFUTURES_TOTAL")

    def start(self):
        AbsReal.start(self, self.code)

def getForeignFuturesInfo():
    info_handler = ForeignFuturesInfo.getInstance()
    info_handler.start()
    info_handler.singleRequest(0)

    while info_handler.is_data_received == False:
        pythoncom.PumpWaitingMessages()

    info_handler.saveResultData("FOREIGNFUTURES", "FOREIGNFUTURES_INFO") # dataframe csv file save
    df_data =  info_handler.getResultData()

    module_logger.info("Get total info successfully.")

    return df_data

def getForeignFuturesRealData(list_symbol):
    # 해외 선물 호가 인스턴스
    hoga_handler = ForeignFuturesHoga.getInstance()
    hoga_handler.start()

    # 해쇠 선물 체결 인스턴스
    chegyul_handler = ForeignFuturesChegyul.getInstance()
    chegyul_handler.start()

    # 해외 선물 종목 추가
    for symbol in list_symbol:
        hoga_handler.add_item(symbol, "symbol")
        chegyul_handler.add_item(symbol, "symbol")

    nums = len(list_symbol)
    module_logger.info("Added futures codes well :: total codes are " + str(nums) + ".")

    return hoga_handler, chegyul_handler


def getGatheringInstance():
    """
    나중에 옵션을 주어서 원하는 종목들만 받아올 수 있게 개선
    :return:
    """

    df_foreign_futures_info = getForeignFuturesInfo()

    list_symbols = df_foreign_futures_info.loc[:,'종목코드'] #전 종목 가져오기
    list_symbols = list(list_symbols)

    h1, h2 = getForeignFuturesRealData(list_symbols)
    return h1,h2

if __name__ == "__main__":
    import Apis.Login

    Apis.Login.do_login(True)
    df_foreign_futures_info = getForeignFuturesInfo()

    list_symbols = df_foreign_futures_info.loc[:,'종목코드'] #전 종목 가져오기
    list_symbols = list(list_symbols)

    ffh, ffc = getForeignFuturesRealData(list_symbols)

    while True:
        pythoncom.PumpWaitingMessages()
