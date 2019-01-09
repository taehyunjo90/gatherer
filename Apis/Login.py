import win32com.client
import pythoncom


import CONFIG

## 로그인 ##
class LoginHandler(object):
    def __init__(self):
        self.is_logined = False
        self.id = CONFIG.LOGININFO['ID']
        self.pw = CONFIG.LOGININFO['PW']
        self.cert_pw = CONFIG.LOGININFO['CERTPW']

    def start(self, real_market = True):
        self.real_market = real_market
        if self.real_market:
            self.ConnectServer("hts.ebestsec.co.kr", 20001)
        elif not self.real_market:
            self.ConnectServer("demo.ebestsec.co.kr", 20001)

        self.Login(self.id, self.pw, self.cert_pw, 0, 0)

    def OnLogin(self, code, msg):
        if code == "0000":
            self.is_logined = True
            print("로그인 성공 ::", code, "::" ,msg)
        else:
            print("로그인 실패 ::", code, "::" ,msg)

    @classmethod
    def getInstance(cls):
        instXASession = win32com.client.DispatchWithEvents("XA_Session.XASession", cls)
        return instXASession

def do_login(real_market = True):
    loginhandler = LoginHandler.getInstance()
    loginhandler.start(real_market)
    while loginhandler.is_logined == False:
        pythoncom.PumpWaitingMessages()

if __name__ == "__main__":
    do_login(True)