from Apis.Abstract import *

module_logger = logging.getLogger('Apis.ForeignOption')
module_logger.setLevel(logging.DEBUG)
module_logger.addHandler(ch)

class ForeignOptionInfo(AbsTROccurs):

    def __init__(self):
        AbsTROccurs.__init__(self) # 추상화 클래스 생성자
        self.code = "o3121" #TR Code

    def OnReceiveData(self, tr_code):
        self.is_data_received = True
        self.count = self.GetBlockCount("o3121OutBlock")
        self.total_data = []

        for i in range(self.count):
            tmp_data = [
                self.GetFieldData("o3121OutBlock", "Symbol", i),
                self.GetFieldData("o3121OutBlock", "SymbolNm", i),
                self.GetFieldData("o3121OutBlock", "ApplDate", i),
                self.GetFieldData("o3121OutBlock", "BscGdsCd", i),
                self.GetFieldData("o3121OutBlock", "BscGdsNm", i),
                self.GetFieldData("o3121OutBlock", "ExchCd", i),
                self.GetFieldData("o3121OutBlock", "ExchNm", i),
                self.GetFieldData("o3121OutBlock", "CrncyCd", i),
                self.GetFieldData("o3121OutBlock", "NotaCd", i),
                self.GetFieldData("o3121OutBlock", "UntPrc", i),
                self.GetFieldData("o3121OutBlock", "MnChgAmt", i),
                self.GetFieldData("o3121OutBlock", "RgltFctr", i),
                self.GetFieldData("o3121OutBlock", "CtrtPrAmt", i),
                self.GetFieldData("o3121OutBlock", "GdsCd", i),
                self.GetFieldData("o3121OutBlock", "LstngYr", i),
                self.GetFieldData("o3121OutBlock", "LstngM", i),
                self.GetFieldData("o3121OutBlock", "EcPrc", i),
                self.GetFieldData("o3121OutBlock", "DlStrtTm", i),
                self.GetFieldData("o3121OutBlock", "DlEndTm", i),
                self.GetFieldData("o3121OutBlock", "DlPsblCd", i),
                self.GetFieldData("o3121OutBlock", "MgnCltCd", i),
                self.GetFieldData("o3121OutBlock", "OpngMgn", i),
                self.GetFieldData("o3121OutBlock", "MntncMgn", i),
                self.GetFieldData("o3121OutBlock", "OpngMgnR", i),
                self.GetFieldData("o3121OutBlock", "MntncMgnR", i),
                self.GetFieldData("o3121OutBlock", "DotGb", i),
                self.GetFieldData("o3121OutBlock", "XrcPrc", i),
                self.GetFieldData("o3121OutBlock", "FdasBasePrc", i),
                self.GetFieldData("o3121OutBlock", "OptTpCode", i),
                self.GetFieldData("o3121OutBlock", "RgtXrcPtnCode", i),
                self.GetFieldData("o3121OutBlock", "Moneyness", i),
                self.GetFieldData("o3121OutBlock", "LastSettPtnCode", i),
                self.GetFieldData("o3121OutBlock", "OptMinOrcPrc", i),
                self.GetFieldData("o3121OutBlock", "OptMinBaseOrcPrc", i)
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
                                     '유효소수점자리수',
                                     '옵션행사가',
                                     '기초자산기준가격',
                                     '옵션콜풋구분',
                                     '권리행사구분코드',
                                     'ATM구분',
                                     '해외파생기초자산종목코드',
                                     '해외옵션최소호가',
                                     '해외옵션최소기준호가']

            self.df_received_data = df_total_data

    def start(self):
        AbsTROccurs.start(self, self.code)

    def singleRequest(self, *args):
        MktGb = args[0]
        BscGdsCd = args[1]
        self.SetFieldData("o3121InBlock", "MktGb", 0, MktGb)
        self.SetFieldData("o3121InBlock", "BscGdsCd", 0, BscGdsCd)
        self.Request(False)


class ForeignOptionHoga(AbsReal):  ## 해외 선물 호가
    """
    해외 선물 실시간 호가를 가져오는 class
    데이터 저장 방식은 csv 파일로 저장
    """
    def __init__(self):
        AbsReal.__init__(self)
        self._open_file()
        self.code = "WOH"

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

        self.writer.writerow(self.data)
        # print(self.data)
        self.f.flush()

    def _open_file(self):  # I/O
        AbsReal._open_file(self, "FOREIGNOPTION", "FOREIGNOPTION_TOTAL")

    def start(self):
        AbsReal.start(self, self.code)


class ForeignOptionChegyul(AbsReal):  ## 해외선물 체결

    def __init__(self):
        AbsReal.__init__(self)
        self._open_file()
        self.code = "WOC"

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

        self.writer.writerow(self.data)
        self.f.flush()

    def _open_file(self):  # I/O
        AbsReal._open_file(self, "FOREIGNOPTION", "FOREIGNOPTION_TOTAL")

    def start(self):
        AbsReal.start(self, self.code)


def getForeignOptionAssetInfo(option):
    """
    option == 0 전체 종목
    option > 0, option 숫자만큼 차월물로 이동해서 (달로 이동하는게 아니라 상품 간격 단위 만큼 이동)
    example) option == 2
    1901, 1903, 1905, 1907 ... 만기물이면
    1901과 1903만 가져옴
    :param option:
    :return:
    """
    info_asset_handler = ForeignOptionInfo.getInstance()
    info_asset_handler.start()
    info_asset_handler.singleRequest("O","") # Option의 "O", 두번째 공란의 경우 옵션 기초상품 조회

    while info_asset_handler.is_data_received == False:
        pythoncom.PumpWaitingMessages()

    info_asset_handler.saveResultData("FOREIGNOPTION", "FOREIGNOPTION_TOTAL_INFO")
    df_asset = info_asset_handler.getResultData()

    module_logger.info("Successfully get simple info of whole foreign option.")

    list_df_info = []

    for idx, code in enumerate(df_asset.loc[:,'기초상품코드']):
        time.sleep(1.1) #TR제한 1초당 1건
        info_handler = ForeignOptionInfo.getInstance()
        info_handler.start()
        info_handler.singleRequest("O", code)  # Option의 "O", 두번째 공란의 경우 옵션 기초상품 조회

        while info_handler.is_data_received == False:
            pythoncom.PumpWaitingMessages()

        real_code = code.split("_")[-1]

        # 저장
        info_handler.saveResultData("FOREIGNOPTION", "FOREINGOPTION_" + str(real_code) + "_INFO")
        module_logger.info("Successfully get " + str(real_code) + " option details. :: " + str(idx+1) + "th")

        df_option_info = info_handler.getResultData()
        if option != 0 :
            df_cut_option_info = getCodesByExpirationNums(df_option_info, option)
            list_df_info.append(df_cut_option_info)
        elif option == 0:
            list_df_info.append(df_option_info)

    df_whole_info = pd.concat(list_df_info)

    return df_whole_info

def getCodesByExpirationNums(df_option_info, num):
    sr_expiration = df_option_info.loc[:,'종목명'].map(lambda x: x.split("(")[-1])
    sr_expiration = sr_expiration.map(lambda x:x.split(")")[0])

    arr_target_codes = sr_expiration.unique()[:num]

    target_idx = 0
    for idx, code in sr_expiration.iteritems():
        if code in arr_target_codes:
            target_idx = idx
        else:
            break
    module_logger.debug(str(target_idx))
    df_cut_option_info = df_option_info.iloc[:target_idx + 1]
    return df_cut_option_info


def getForeignOptionRealData(list_symbol):
    # 해외 옵션 호가 인스턴스
    hoga_handler = ForeignOptionHoga.getInstance()
    hoga_handler.start()

    # 해쇠 선물 체결 인스턴스
    chegyul_handler = ForeignOptionChegyul.getInstance()
    chegyul_handler.start()

    # 해외 선물 종목 추가
    total_length = len(list_symbol)
    for i, symbol in enumerate(list_symbol):
        hoga_handler.add_item(symbol, "symbol")
        chegyul_handler.add_item(symbol, "symbol")
        module_logger.debug(str(i + 1) + "/" + str(total_length))

    return hoga_handler, chegyul_handler

if __name__ == "__main__":
    import Apis.Login
    Apis.Login.do_login(True)
    df_whole_info = getForeignOptionAssetInfo(0)
    list_symbol = list(df_whole_info.loc[:,'종목코드'])

    ## 해외 옵션의 경우 종목 수가 너무 많아서 주요 종목만 크롤링 하는 방법을 만들어야 겠다.
    f1 = getForeignOptionRealData(list_symbol[:5000])
    f2 = getForeignOptionRealData(list_symbol[5000:10000])
    f3 = getForeignOptionRealData(list_symbol[10000:15000])
    f4 = getForeignOptionRealData(list_symbol[15000:20000])
    f5 = getForeignOptionRealData(list_symbol[20000:25000])
    f6 = getForeignOptionRealData(list_symbol[25000:30000])
    f7 = getForeignOptionRealData(list_symbol[30000:])

    while True:
        pythoncom.PumpWaitingMessages()



