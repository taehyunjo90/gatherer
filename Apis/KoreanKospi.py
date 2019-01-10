from Apis.Abstract import *

module_logger = logging.getLogger('Apis.KoreanKospi')
module_logger.setLevel(logging.INFO)
module_logger.addHandler(ch)

class KoreanKospiInfo(AbsTROccurs):
    def __init__(self):
        AbsTROccurs.__init__(self) # 추상화 클래스 생성자
        self.code = "t8436" #TR Code

    def OnReceiveData(self, tr_code):
        self.is_data_received = True
        self.count = self.GetBlockCount("t8436OutBlock")
        self.total_data = []

        for i in range(self.count):
            tmp_data = [
                self.GetFieldData("t8436OutBlock", "hname", i),
                self.GetFieldData("t8436OutBlock", "shcode", i),
                self.GetFieldData("t8436OutBlock", "expcode", i),
                self.GetFieldData("t8436OutBlock", "etfgubun", i),
                self.GetFieldData("t8436OutBlock", "uplmtprice", i),
                self.GetFieldData("t8436OutBlock", "dnlmtprice", i),
                self.GetFieldData("t8436OutBlock", "jnilclose", i),
                self.GetFieldData("t8436OutBlock", "memedan", i),
                self.GetFieldData("t8436OutBlock", "recprice", i),
                self.GetFieldData("t8436OutBlock", "gubun", i),
                self.GetFieldData("t8436OutBlock", "bu12gubun", i),
                self.GetFieldData("t8436OutBlock", "spac_gubun", i),
                self.GetFieldData("t8436OutBlock", "filler", i),
            ]
            self.total_data.append(tmp_data)

        df_total_data = pd.DataFrame(self.total_data)
        df_total_data.columns = [
            "종목명",
            "단축코드",
            "확장코드",
            "ETF구분(1:ETF2:ETN)",
            "상한가",
            "하한가",
            "전일가",
            "주문수량단위",
            "기준가",
            "구분(1:코스피2:코스닥)",
            "증권그룹",
            "기업인수목적회사여부(Y/N)",
            "filler(미사용)"
        ]

        self.df_received_data = df_total_data

    def start(self):
        AbsTROccurs.start(self, self.code)

    def singleRequest(self, *args):
        gubun = args[0]
        self.SetFieldData("t8436InBlock", "gubun", 0, gubun)
        self.Request(False)


class KoreanKospiHoga(AbsReal):  ## 해외 선물 호가
    def __init__(self):
        AbsReal.__init__(self)
        self._open_file()
        self.code = "H1_"

    def OnReceiveRealData(self, tr_code):
        self.data = []

        self.data.append(self.GetFieldData("OutBlock", "shcode"))
        self.data.append(time.time())  # Computer Time
        self.data.append(self.GetFieldData("OutBlock", "hotime"))

        for i in range(1, 11):  # 1~10
            self.data.append(self.GetFieldData("OutBlock", "offerho" + str(i)))
        for i in range(1, 11):  # 1~10
            self.data.append(self.GetFieldData("OutBlock", "offerrem" + str(i)))

        for i in range(1, 11):  # 1~10
            self.data.append(self.GetFieldData("OutBlock", "bidho" + str(i)))
        for i in range(1, 11):  # 1~10
            self.data.append(self.GetFieldData("OutBlock", "bidrem" + str(i)))


        self.data.append(self.GetFieldData("OutBlock", "totofferrem"))
        self.data.append(self.GetFieldData("OutBlock", "totbidrem"))
        self.data.append(self.GetFieldData("OutBlock", "donsigubun"))
        self.data.append(self.GetFieldData("OutBlock", "alloc_gubun"))

        # print(self.data)

        self.writer.writerow(self.data)
        self.f.flush()

    def _open_file(self):  # I/O
        AbsReal._open_file(self, "KOREANSTOCK", "KOREANSTOCK_KOSPI_HOGA")

    def start(self):
        AbsReal.start(self, self.code)

class KoreanKospiChegyul(AbsReal):  ## 해외선물 체결

    def __init__(self):
        AbsReal.__init__(self)
        self._open_file()
        self.code = "S3_"

    def OnReceiveRealData(self, tr_code):  # event handler
        self.data = []
        self.data.append(self.GetFieldData("OutBlock", "shcode"))
        self.data.append(time.time())
        self.data.append(self.GetFieldData("OutBlock", "chetime"))
        self.data.append(self.GetFieldData("OutBlock", "sign"))
        self.data.append(self.GetFieldData("OutBlock", "change"))
        self.data.append(self.GetFieldData("OutBlock", "drate"))
        self.data.append(self.GetFieldData("OutBlock", "price"))
        self.data.append(self.GetFieldData("OutBlock", "opentime"))
        self.data.append(self.GetFieldData("OutBlock", "open"))
        self.data.append(self.GetFieldData("OutBlock", "hightime"))
        self.data.append(self.GetFieldData("OutBlock", "high"))
        self.data.append(self.GetFieldData("OutBlock", "lowtime"))
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
        self.data.append(self.GetFieldData("OutBlock", "w_avrg"))
        self.data.append(self.GetFieldData("OutBlock", "offerho"))
        self.data.append(self.GetFieldData("OutBlock", "bidho"))
        self.data.append(self.GetFieldData("OutBlock", "status"))
        self.data.append(self.GetFieldData("OutBlock", "jnilvolume"))

        self.writer.writerow(self.data)
        self.f.flush()

    def _open_file(self):  # I/O
        AbsReal._open_file(self, "KOREANSTOCK", "KOREANSTOCK_KOSPI_CHEGYUL")

    def start(self):
        AbsReal.start(self, self.code)

class KoreanKospiCounter(AbsReal):  ## 해외선물 체결

    def __init__(self):
        AbsReal.__init__(self)
        self._open_file()
        self.code = "K1_"

    def OnReceiveRealData(self, tr_code):  # event handler
        self.data = []
        self.data.append(self.GetFieldData("OutBlock", "shcode"))
        self.data.append(time.time())
        self.data.append(self.GetFieldData("OutBlock", "offerno1"))
        self.data.append(self.GetFieldData("OutBlock", "bidno1"))
        self.data.append(self.GetFieldData("OutBlock", "offertrad1"))
        self.data.append(self.GetFieldData("OutBlock", "bidtrad1"))
        self.data.append(self.GetFieldData("OutBlock", "tradmdvol1"))
        self.data.append(self.GetFieldData("OutBlock", "tradmsvol1"))
        self.data.append(self.GetFieldData("OutBlock", "tradmdrate1"))
        self.data.append(self.GetFieldData("OutBlock", "tradmsrate1"))
        self.data.append(self.GetFieldData("OutBlock", "tradmdcha1"))
        self.data.append(self.GetFieldData("OutBlock", "tradmscha1"))
        self.data.append(self.GetFieldData("OutBlock", "offerno2"))
        self.data.append(self.GetFieldData("OutBlock", "bidno2"))
        self.data.append(self.GetFieldData("OutBlock", "offertrad2"))
        self.data.append(self.GetFieldData("OutBlock", "bidtrad2"))
        self.data.append(self.GetFieldData("OutBlock", "tradmdvol2"))
        self.data.append(self.GetFieldData("OutBlock", "tradmsvol2"))
        self.data.append(self.GetFieldData("OutBlock", "tradmdrate2"))
        self.data.append(self.GetFieldData("OutBlock", "tradmsrate2"))
        self.data.append(self.GetFieldData("OutBlock", "tradmdcha2"))
        self.data.append(self.GetFieldData("OutBlock", "tradmscha2"))
        self.data.append(self.GetFieldData("OutBlock", "offerno3"))
        self.data.append(self.GetFieldData("OutBlock", "bidno3"))
        self.data.append(self.GetFieldData("OutBlock", "offertrad3"))
        self.data.append(self.GetFieldData("OutBlock", "bidtrad3"))
        self.data.append(self.GetFieldData("OutBlock", "tradmdvol3"))
        self.data.append(self.GetFieldData("OutBlock", "tradmsvol3"))
        self.data.append(self.GetFieldData("OutBlock", "tradmdrate3"))
        self.data.append(self.GetFieldData("OutBlock", "tradmsrate3"))
        self.data.append(self.GetFieldData("OutBlock", "tradmdcha3"))
        self.data.append(self.GetFieldData("OutBlock", "tradmscha3"))
        self.data.append(self.GetFieldData("OutBlock", "offerno4"))
        self.data.append(self.GetFieldData("OutBlock", "bidno4"))
        self.data.append(self.GetFieldData("OutBlock", "offertrad4"))
        self.data.append(self.GetFieldData("OutBlock", "bidtrad4"))
        self.data.append(self.GetFieldData("OutBlock", "tradmdvol4"))
        self.data.append(self.GetFieldData("OutBlock", "tradmsvol4"))
        self.data.append(self.GetFieldData("OutBlock", "tradmdrate4"))
        self.data.append(self.GetFieldData("OutBlock", "tradmsrate4"))
        self.data.append(self.GetFieldData("OutBlock", "tradmdcha4"))
        self.data.append(self.GetFieldData("OutBlock", "tradmscha4"))
        self.data.append(self.GetFieldData("OutBlock", "offerno5"))
        self.data.append(self.GetFieldData("OutBlock", "bidno5"))
        self.data.append(self.GetFieldData("OutBlock", "offertrad5"))
        self.data.append(self.GetFieldData("OutBlock", "bidtrad5"))
        self.data.append(self.GetFieldData("OutBlock", "tradmdvol5"))
        self.data.append(self.GetFieldData("OutBlock", "tradmsvol5"))
        self.data.append(self.GetFieldData("OutBlock", "tradmdrate5"))
        self.data.append(self.GetFieldData("OutBlock", "tradmsrate5"))
        self.data.append(self.GetFieldData("OutBlock", "tradmdcha5"))
        self.data.append(self.GetFieldData("OutBlock", "tradmscha5"))
        self.data.append(self.GetFieldData("OutBlock", "ftradmdvol"))
        self.data.append(self.GetFieldData("OutBlock", "ftradmsvol"))
        self.data.append(self.GetFieldData("OutBlock", "ftradmdrate"))
        self.data.append(self.GetFieldData("OutBlock", "ftradmsrate"))
        self.data.append(self.GetFieldData("OutBlock", "ftradmdcha"))
        self.data.append(self.GetFieldData("OutBlock", "ftradmscha"))
        self.data.append(self.GetFieldData("OutBlock", "tradmdval1"))
        self.data.append(self.GetFieldData("OutBlock", "tradmsval1"))
        self.data.append(self.GetFieldData("OutBlock", "tradmdavg1"))
        self.data.append(self.GetFieldData("OutBlock", "tradmsavg1"))
        self.data.append(self.GetFieldData("OutBlock", "tradmdval2"))
        self.data.append(self.GetFieldData("OutBlock", "tradmsval2"))
        self.data.append(self.GetFieldData("OutBlock", "tradmdavg2"))
        self.data.append(self.GetFieldData("OutBlock", "tradmsavg2"))
        self.data.append(self.GetFieldData("OutBlock", "tradmdval3"))
        self.data.append(self.GetFieldData("OutBlock", "tradmsval3"))
        self.data.append(self.GetFieldData("OutBlock", "tradmdavg3"))
        self.data.append(self.GetFieldData("OutBlock", "tradmsavg3"))
        self.data.append(self.GetFieldData("OutBlock", "tradmdval4"))
        self.data.append(self.GetFieldData("OutBlock", "tradmsval4"))
        self.data.append(self.GetFieldData("OutBlock", "tradmdavg4"))
        self.data.append(self.GetFieldData("OutBlock", "tradmsavg4"))
        self.data.append(self.GetFieldData("OutBlock", "tradmdval5"))
        self.data.append(self.GetFieldData("OutBlock", "tradmsval5"))
        self.data.append(self.GetFieldData("OutBlock", "tradmdavg5"))
        self.data.append(self.GetFieldData("OutBlock", "tradmsavg5"))
        self.data.append(self.GetFieldData("OutBlock", "ftradmdval"))
        self.data.append(self.GetFieldData("OutBlock", "ftradmsval"))
        self.data.append(self.GetFieldData("OutBlock", "ftradmdavg"))
        self.data.append(self.GetFieldData("OutBlock", "ftradmsavg"))

        self.writer.writerow(self.data)
        self.f.flush()

    def _open_file(self):  # I/O
        AbsReal._open_file(self, "KOREANSTOCK", "KOREANSTOCK_KOSPI_COUNTER")

    def start(self):
        AbsReal.start(self, self.code)

def getKoreanKospiInfo():
    info_handler = KoreanKospiInfo.getInstance()
    info_handler.start()
    info_handler.singleRequest(1) # 0 :전체 1: 코스피 2: 코스닥

    while info_handler.is_data_received == False:
        pythoncom.PumpWaitingMessages()

    info_handler.saveResultData("KOREANSTOCK", "KOREANSTOCK_KOSPI_INFO") # dataframe csv file save
    df_data =  info_handler.getResultData()

    module_logger.info("Get korean stock(KOSPI) info successfully")

    return df_data


def getKoreanKospiRealData(list_shcode):
    hoga_handler = KoreanKospiHoga.getInstance()
    hoga_handler.start()

    chegyul_handler = KoreanKospiChegyul.getInstance()
    chegyul_handler.start()

    counter_handler = KoreanKospiCounter.getInstance()
    counter_handler.start()

    # 해외 선물 종목 추가
    for shcode in list_shcode:
        hoga_handler.add_item(shcode, "shcode")
        chegyul_handler.add_item(shcode, "shcode")
        counter_handler.add_item(shcode, "shcode")

    nums = len(list_shcode)
    module_logger.info("Added korean stock(KOSPI) codes well :: total codes are " + str(nums) + ".")

    return hoga_handler, chegyul_handler, counter_handler


def getGatheringInstance():
    """
    나중에 옵션을 주어서 원하는 종목들만 받아올 수 있게 개선
    :return:
    """
    df_info = getKoreanKospiInfo()

    list_shcode = df_info.loc[:, '단축코드']  # 전 종목 가져오기
    list_shcode = list(list_shcode)

    h1, h2, h3 = getKoreanKospiRealData(list_shcode)

    return h1, h2, h3

if __name__ == "__main__":
    import Apis.Login

    Apis.Login.do_login(True)
    df_info = getKoreanKospiInfo()

    list_shcode = df_info.loc[:, '단축코드'] # 전 종목 가져오기
    list_shcode = list(list_shcode)

    h1,h2,h3  = getKoreanKospiRealData(list_shcode)

    while True:
        pythoncom.PumpWaitingMessages()