from Apis.Abstract import *

module_logger = logging.getLogger('Apis.KoreanOption')
module_logger.setLevel(logging.INFO)
module_logger.addHandler(ch)

class KoreanOptionInfo(AbsTROccurs):
    def __init__(self):
        AbsTROccurs.__init__(self) # 추상화 클래스 생성자
        self.code = "t8433" #TR Code

    def OnReceiveData(self, tr_code):
        self.is_data_received = True
        self.count = self.GetBlockCount("t8433OutBlock")
        self.total_data = []

        for i in range(self.count):
            tmp_data = [
                self.GetFieldData("t8433OutBlock", "hname", i),
                self.GetFieldData("t8433OutBlock", "shcode", i),
                self.GetFieldData("t8433OutBlock", "expcode", i),
                self.GetFieldData("t8433OutBlock", "hprice", i),
                self.GetFieldData("t8433OutBlock", "lprice", i),
                self.GetFieldData("t8433OutBlock", "jnilclose", i),
                self.GetFieldData("t8433OutBlock", "jnilhigh", i),
                self.GetFieldData("t8433OutBlock", "jnillow", i),
                self.GetFieldData("t8433OutBlock", "recprice", i)
            ]
            self.total_data.append(tmp_data)

        df_total_data = pd.DataFrame(self.total_data)
        df_total_data.columns = [
            "종목명",
            "단축코드",
            "확장코드",
            "상한가",
            "하한가",
            "전일종가",
            "전일고가",
            "전일저가",
            "기준가"
        ]

        self.df_received_data = df_total_data

    def start(self):
        AbsTROccurs.start(self, self.code)

    def singleRequest(self, *args):
        dummy = args[0]
        self.SetFieldData("t8433InBlock", "dummy", 0, dummy)
        self.Request(False)

class KoreanOptionHoga(AbsReal):  ## 해외 선물 호가
    def __init__(self):
        AbsReal.__init__(self)
        self._open_file()
        self.code = "OH0"

    def OnReceiveRealData(self, tr_code):
        self.data = []

        self.data.append(self.GetFieldData("OutBlock", "optcode"))
        self.data.append(time.time())  # Computer Time
        self.data.append(self.GetFieldData("OutBlock", "hotime"))

        for i in range(1, 6):  # 1~5
            self.data.append(self.GetFieldData("OutBlock", "offerho" + str(i)))
        for i in range(1, 6):  # 1~5
            self.data.append(self.GetFieldData("OutBlock", "offerrem" + str(i)))
        for i in range(1, 6):  # 1~5
            self.data.append(self.GetFieldData("OutBlock", "offercnt" + str(i)))

        for i in range(1, 6):  # 1~5
            self.data.append(self.GetFieldData("OutBlock", "bidho" + str(i)))
        for i in range(1, 6):  # 1~5
            self.data.append(self.GetFieldData("OutBlock", "bidrem" + str(i)))
        for i in range(1, 6):  # 1~5
            self.data.append(self.GetFieldData("OutBlock", "bidcnt" + str(i)))

        self.data.append(self.GetFieldData("OutBlock", "totofferrem"))
        self.data.append(self.GetFieldData("OutBlock", "totbidrem"))
        self.data.append(self.GetFieldData("OutBlock", "totoffercnt"))
        self.data.append(self.GetFieldData("OutBlock", "totbidcnt"))
        self.data.append(self.GetFieldData("OutBlock", "danhochk"))
        self.data.append(self.GetFieldData("OutBlock", "alloc_gubun"))

        self.writer.writerow(self.data)
        self.f.flush()

    def _open_file(self):  # I/O
        AbsReal._open_file(self, "KOREANOPTION", "KOREANOPTION_TOTAL")

    def start(self):
        AbsReal.start(self, self.code)

class KoreanOptionChegyul(AbsReal):  ## 해외선물 체결

    def __init__(self):
        AbsReal.__init__(self)
        self._open_file()
        self.code = "OC0"

    def OnReceiveRealData(self, tr_code):  # event handler
        self.data = []
        self.data.append(self.GetFieldData("OutBlock", "optcode"))
        self.data.append(time.time())
        self.data.append(self.GetFieldData("OutBlock", "chetime"))
        self.data.append(self.GetFieldData("OutBlock", "sign"))
        self.data.append(self.GetFieldData("OutBlock", "change"))
        self.data.append(self.GetFieldData("OutBlock", "drate"))
        self.data.append(self.GetFieldData("OutBlock", "price"))
        self.data.append(self.GetFieldData("OutBlock", "open"))
        self.data.append(self.GetFieldData("OutBlock", "high"))
        self.data.append(self.GetFieldData("OutBlock", "low"""))
        self.data.append(self.GetFieldData("OutBlock", "cgubun"))
        self.data.append(self.GetFieldData("OutBlock", "cvolume"))
        self.data.append(self.GetFieldData("OutBlock", "volume"))
        self.data.append(self.GetFieldData("OutBlock", "value"))
        self.data.append(self.GetFieldData("OutBlock", "mdvolume"))
        self.data.append(self.GetFieldData("OutBlock", "mdchecnt"))
        self.data.append(self.GetFieldData("OutBlock", "msvolume"))
        self.data.append(self.GetFieldData("OutBlock", "mschecnt"))
        self.data.append(self.GetFieldData("OutBlock", "cpower"))
        self.data.append(self.GetFieldData("OutBlock", "offerho1"))
        self.data.append(self.GetFieldData("OutBlock", "bidho1"))
        self.data.append(self.GetFieldData("OutBlock", "openyak"))
        self.data.append(self.GetFieldData("OutBlock", "k200jisu"))
        self.data.append(self.GetFieldData("OutBlock", "eqva"))
        self.data.append(self.GetFieldData("OutBlock", "theoryprice"))
        self.data.append(self.GetFieldData("OutBlock", "impv"))
        self.data.append(self.GetFieldData("OutBlock", "openyakcha"))
        self.data.append(self.GetFieldData("OutBlock", "timevalue"))
        self.data.append(self.GetFieldData("OutBlock", "jgubun"))
        self.data.append(self.GetFieldData("OutBlock", "jnilvolume"))

        self.writer.writerow(self.data)
        self.f.flush()

    def _open_file(self):  # I/O
        AbsReal._open_file(self, "KOREANOPTION", "KOREANOPTION_TOTAL")

    def start(self):
        AbsReal.start(self, self.code)

def getKoreanOptionInfo():
    info_handler = KoreanOptionInfo.getInstance()
    info_handler.start()
    info_handler.singleRequest(0)

    while info_handler.is_data_received == False:
        pythoncom.PumpWaitingMessages()

    info_handler.saveResultData("KOREANOPTION", "KOREANOPTION_INFO") # dataframe csv file save
    df_data =  info_handler.getResultData()

    module_logger.info("Get korean option info successfully")

    return df_data


def getKoreanOptionRealData(list_optcode):
    hoga_handler = KoreanOptionHoga.getInstance()
    hoga_handler.start()

    chegyul_handler = KoreanOptionChegyul.getInstance()
    chegyul_handler.start()

    # 해외 선물 종목 추가
    for optcode in list_optcode:
        hoga_handler.add_item(optcode, "optcode")
        chegyul_handler.add_item(optcode, "optcode")

    nums = len(list_optcode)
    module_logger.info("Added futures codes well :: total codes are " + str(nums) + ".")

    return hoga_handler, chegyul_handler


def getGatheringInstance():
    """
    나중에 옵션을 주어서 원하는 종목들만 받아올 수 있게 개선
    :return:
    """
    df_info = getKoreanOptionInfo()

    list_optcode = df_info.loc[:, '단축코드'] # 전 종목 가져오기
    list_optcode = list(list_optcode)

    h1, h2 = getKoreanOptionRealData(list_optcode)
    return h1, h2


if __name__ == "__main__":
    import Apis.Login

    Apis.Login.do_login(True)
    df_info = getKoreanOptionInfo()

    list_optcode = df_info.loc[:, '단축코드'] # 전 종목 가져오기
    list_optcode = list(list_optcode)

    koh, koc = getKoreanOptionRealData(list_optcode)

    while True:
        pythoncom.PumpWaitingMessages()