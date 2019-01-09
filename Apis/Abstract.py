import win32com.client
import pythoncom
import pandas as pd
import time
import csv
import Apis.Util as util
import logging


logger = logging.getLogger('Apis.Abstract') # Not will be used on normal situation.
# logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
# logger.addHandler(ch)



class AbsTROccurs(object):
    """
    종목 관련 정보를 가져오는 TR을 요청하는 추상화 CLASS
    이 class를 통해서 종목 정보를 가져오고
    여기서 얻어진 종목정보 및 종목코드를 토대로 호가 및 체결 데이터들(실시간)을 가져올 것이다.
    """
    def __init__(self):
        self.is_data_received = False

    def OnReceiveData(self, tr_code):
        pass

    def getResultData(self):
        """
        DataFrame화 된 TR요청 결과를 반환.
        :return:
        """
        return self.df_received_data

    def saveResultData(self, foldername, filename):
        # DataFrame화 된 Tr요청 결과를 csv 파일로 저장
        file_path = util.get_file_path(foldername, filename)
        util.check_and_make_dir(file_path)
        self.df_received_data.to_csv(file_path, encoding='cp949')

    def start(self, code):
        """
        code must be string
        :param code:
        :return:
        """
        self.ResFileName = "C:\\eBEST\\xingAPI\\Res\\" + code + ".res"

    def singleRequest(self, *args):
        pass

    @classmethod
    def getInstance(cls):
        xq = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", cls)
        return xq

class AbsReal(object):  ## 해외 선물 호가
    """
    호가를 가져오는 추상화 클래스
    Real 데이터 요청을 통해서 받아오고
    데이터 저장 방식은 csv 파일로 저장
    """

    def __init__(self):
        super().__init__()
        self._open_file() #csv 저장 연결 부분

    def OnReceiveRealData(self, tr_code):  # event handler
        """
        이베스트 서버에서 이벤트를 받으면 실행되는 event handler
        """
        pass

    def _open_file(self, foldername, filename):  # I/O
        self.f = util.open_file_by_date(foldername= foldername, filename=filename)
        self.writer = csv.writer(self.f)

    def start(self, code):
        self.ResFileName = "C:\\eBEST\\xingAPI\\Res\\" + code + ".res"  # RES 파일 등록

    def add_item(self, item, option):
        # 실시간데이터 요청 종목 추가
        if option == "shcode":
            self.SetFieldData("InBlock", "shcode", item)
        elif option == "symbol":
            self.SetFieldData("InBlock", "symbol", item)
        elif option == "futcode":
            self.SetFieldData("InBlock", "futcode", item)
        elif option == "optcode":
            self.SetFieldData("InBlock", "optcode", item)

        self.AdviseRealData()

    def remove_item(self, symbol):
        # stockcode 종목만 실시간데이터 요청 취소
        self.UnadviseRealDataWithKey(symbol)

    def stop(self):
        self.UnadviseRealData()  # 실시간데이터 요청 모두 취소
        del self.writer

    @classmethod
    def getInstance(cls):
        xr = win32com.client.DispatchWithEvents("XA_DataSet.XAReal", cls)
        return xr

