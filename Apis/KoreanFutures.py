from Apis.Abstract import *

module_logger = logging.getLogger('Apis.KoreanFutures')
module_logger.setLevel(logging.INFO)
module_logger.addHandler(ch)

class KoreanFuturesInfo(AbsTROccurs):
    def __init__(self):
        AbsTROccurs.__init__(self) # 추상화 클래스 생성자
        self.code = "t8432" #TR Code

    def OnReceiveData(self, tr_code):
        self.is_data_received = True
        self.count = self.GetBlockCount("t8432OutBlock")
        self.total_data = []

        for i in range(self.count):
            tmp_data = [
                self.GetFieldData("t8432OutBlock", "hname", i),
                self.GetFieldData("t8432OutBlock", "shcode", i),
                self.GetFieldData("t8432OutBlock", "expcode", i),
                self.GetFieldData("t8432OutBlock", "uplmtprice", i),
                self.GetFieldData("t8432OutBlock", "dnlmtprice", i),
                self.GetFieldData("t8432OutBlock", "jnilclose", i),
                self.GetFieldData("t8432OutBlock", "jnilhigh", i),
                self.GetFieldData("t8432OutBlock", "jnillow", i),
                self.GetFieldData("t8432OutBlock", "recprice", i)
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
        gubun = args[0]
        self.SetFieldData("t8432InBlock", "gubun", 0, gubun)
        self.Request(False)

class KoreanFuturesHoga(AbsReal):  ## 해외 선물 호가
    def __init__(self):
        AbsReal.__init__(self)
        self._open_file()
        self.code = "FH0"

    def OnReceiveRealData(self, tr_code):
        self.data = []

        self.data.append("hoga")
        self.data.append(self.GetFieldData("OutBlock", "futcode"))
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
        AbsReal._open_file(self, "KOREANFUTURES", "KOREANFUTURES")

    def start(self):
        AbsReal.start(self, self.code)

class KoreanFuturesChegyul(AbsReal):  ## 해외선물 체결

    def __init__(self):
        AbsReal.__init__(self)
        self._open_file()
        self.code = "FC0"

    def OnReceiveRealData(self, tr_code):  # event handler
        self.data = []

        self.data.append("chegyul")
        self.data.append(self.GetFieldData("OutBlock", "futcode"))
        self.data.append(time.time())
        self.data.append(self.GetFieldData("OutBlock", "chetime"))
        self.data.append(self.GetFieldData("OutBlock", "sign"))
        self.data.append(self.GetFieldData("OutBlock", "change"))
        self.data.append(self.GetFieldData("OutBlock", "drate"))
        self.data.append(self.GetFieldData("OutBlock", "price"))
        self.data.append(self.GetFieldData("OutBlock", "open"))
        self.data.append(self.GetFieldData("OutBlock", "high"))
        self.data.append(self.GetFieldData("OutBlock", "low"))
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
        self.data.append(self.GetFieldData("OutBlock", "theoryprice"))
        self.data.append(self.GetFieldData("OutBlock", "kasis"))
        self.data.append(self.GetFieldData("OutBlock", "sbasis"))
        self.data.append(self.GetFieldData("OutBlock", "ibasis"))
        self.data.append(self.GetFieldData("OutBlock", "openyakcha"))
        self.data.append(self.GetFieldData("OutBlock", "jgubun"))
        self.data.append(self.GetFieldData("OutBlock", "jnilvolume"))

        self.writer.writerow(self.data)
        self.f.flush()

    def _open_file(self):  # I/O
        AbsReal._open_file(self, "KOREANFUTURES", "KOREANFUTURES")

    def start(self):
        AbsReal.start(self, self.code)

def getKoreanFuturesInfo(option):
    info_handler = KoreanFuturesInfo.getInstance()
    info_handler.start()
    info_handler.singleRequest(option)

    while info_handler.is_data_received == False:
        pythoncom.PumpWaitingMessages()

    if option == "V":
        filename = "VOL"
    elif option == "S":
        filename = "SECTOR"
    else:
        filename = "IDX"

    info_handler.saveResultData("KOREANFUTURES", "KOREANFUTURES_" + filename + "_INFO") # dataframe csv file save
    df_data =  info_handler.getResultData()

    module_logger.info("Get info with setting :: " + str(filename) )

    return df_data

def getWholeKoreanFuturesInfo():
    df_vol = getKoreanFuturesInfo("V")
    time.sleep(0.6)
    df_sector = getKoreanFuturesInfo("S")
    time.sleep(0.6)
    df_idx = getKoreanFuturesInfo(0)
    time.sleep(0.6)

    df_whole = pd.concat([df_idx, df_vol, df_sector])

    module_logger.info("Get total info successfully :: VOL + SECTOR + IDX")

    return df_whole


def getKoreanFuturesRealData(list_futcode):
    hoga_handler = KoreanFuturesHoga.getInstance()
    hoga_handler.start()

    chegyul_handler = KoreanFuturesChegyul.getInstance()
    chegyul_handler.start()

    # 해외 선물 종목 추가
    for futcode in list_futcode:
        chegyul_handler.add_item(futcode, "futcode")
        hoga_handler.add_item(futcode, "futcode")

    nums = len(list_futcode)
    module_logger.info("Added futures codes well :: total codes are " + str(nums) + ".")

    return hoga_handler, chegyul_handler


def getGatheringInstance():
    """
    나중에 옵션을 주어서 원하는 종목들만 받아올 수 있게 개선
    :return:
    """
    df_info = getWholeKoreanFuturesInfo()

    list_futcode = df_info.loc[:, '단축코드'] # 전 종목 가져오기
    list_futcode = list(list_futcode)

    h1, h2 = getKoreanFuturesRealData(list_futcode)
    return h1, h2


if __name__ == "__main__":
    import Apis.Login

    Apis.Login.do_login(True)
    df_info = getWholeKoreanFuturesInfo()

    list_futcode = df_info.loc[:, '단축코드'] # 전 종목 가져오기
    list_futcode = list(list_futcode)

    kfh, kfc = getKoreanFuturesRealData(list_futcode)

    while True:
        pythoncom.PumpWaitingMessages()
