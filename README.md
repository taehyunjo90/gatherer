# gatherer

![File:Charles Sillem Lidderdale The fern gatherer 1877.jpg](https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Charles_Sillem_Lidderdale_The_fern_gatherer_1877.jpg/415px-Charles_Sillem_Lidderdale_The_fern_gatherer_1877.jpg)





# 개요

본 소스코드는 출저(현재의 깃허브 주소)만 밝히신다면 자유롭게 사용가능합니다.

**star는 제작자를 기쁘게 합니다!^^**

이베스트증권 API를 활용하여 실시간 시장 데이터 수집을 하는 도구입니다.

현재 수집 가능한 데이터는 다음과 같습니다.  



- 대한민국 코스피, 코스닥 **호가, 체결, 거래원 틱 데이터**
- 대한민국 파생상품 선물/옵션 **호가, 체결 틱 데이터**
- 해외 선물 **호가, 체결 틱 데이터**
- 해외 옵션 **호가, 체결 틱 데이터** <u><현재 작동하지 않음></u>



<u>현재의 기능상으로는 전체 종목을 수집하게 되어 있습니다. 이는 차후에 업데이트에서 원하는 종목만 수집하는 기능을 추가할 예정입니다.</u>



# 빠른 실행

** 대부분의 코드는 ["파이썬으로 배우는 알고리즘 트레이딩"](https://wikidocs.net/book/110)을 참조하여 작성되었습니다. 자세한 사항은 이를 참조 부탁드리겠습니다.



**0) 이베스트 API가 설치 및 사용신청이 선행되어야 합니다.**



**1) 최상위 폴더에 다음과 같은 내용으로 CONFIG.PY을 생성합니다.**

```
LOGININFO = {'ID' : 이베스트아이디,
             'PW' : 비밀번호,
             'CERTPW' : 공인인증서비밀번호}
             
IOINFO = {
    'PATH' : 저장경로 (ex "D:\\MARKETDATA\\")
}

TIMEINFO={
    'CRITERIA_HOUR' : 7,
    'CRITERIA_MINUTE' : 30
}
```

** TIMEINEFO의 경우 해외선물/옵션 같은 경우 우리나라 시간 기준으로 오전 7시에 장이 끝나는 경우가 많습니다. 그래서 수집데이터의 일자 구분을 위해서 D+0일 오전 7시 30분 - D+1일 오전 7시 30분까지는 D+0로 봅니다. 



**2) main.py를 작성합니다.**

현재는 실시간 데이터는 양이 많기 때문에 멀티프로세싱으로 프로세스 별로 데이터를 수집하게 해놨습니다. 예를들어 다음과 같이 main문을 실행을 시키면 p0 프로세스에서는 코스닥 데이터를 수집하고, p1 프로세스에서는 코스피 데이터를 수집합니다.



```
p0 = Process(target=Multi.doKosdaq) // 코스닥 호가, 체결 데이터 수집
p1 = Process(target=Multi.doKospi) // 코스피 호가, 체결 데이터 수집

p0.start()
p1.start()

p0.join()
p1.join()
```



**3) 올바르게 실행되었다면 제대로 실행되었다는 프롬프트 메세지가 출력되고, 원하는 실시간 데이터가 CONFIG.py에 지정된 경로에 저장됩니다.**



```
로그인 성공 :: 0000 :: 로그인 성공
로그인 성공 :: 0000 :: 로그인 성공
2019-01-30 07:50:06,733 - Apis.KoreanKosdaq - INFO - Get korean stock(KOSDAQ) info successfully
2019-01-30 07:50:06,764 - Apis.KoreanKospi - INFO - Get korean stock(KOSPI) info successfully
2019-01-30 07:50:06,904 - Apis.KoreanKosdaq - INFO - Added korean stock(KOSDAQ) codes well :: total codes are 1326.
2019-01-30 07:50:06,951 - Apis.KoreanKospi - INFO - Added korean stock(KOSPI) codes well :: total codes are 1524.
```



# 디테일 한 설명

- 저장되는 데이터 설명
  - 이베스트 증권 API에 관련된 설명서 및 DevCenter를 통해 확인 바랍니다.
- 구체적인 작동방식
  - 이베스트 증권 API와 통신하는 객체가 생성되고, 무한루프를 돌면서 이베스트서버에서 이 객체로 실시간으로 데이터가 전송이되고, 이 객체 내부에서 데이터를 파일로 저장하게 됩니다.
  - 대부분의 코드는 ["파이썬으로 배우는 알고리즘 트레이딩"](https://wikidocs.net/book/110)을 참조하여 작성되었습니다.
  - 이 부분을 참고하신다면 구체적인 작동방식에 대해서 이해가 쉽게 되실 것 입니다.



# 추후 업데이트 예정

현재의 수집 기능은 다음과 같은 단위의 전 종목을 수집하는 것만 가능합니다.

- 대한민국 코스피 **호가, 체결, 거래원 틱 데이터** (KoreanKospi.py에 구현)
- 대한민국 코스닥 **호가, 체결, 거래원 틱 데이터** (KoreanKosdaq.py에 구현)
- 대한민국 파생상품 선물 **호가, 체결 틱 데이터** (KoreanFutures.py에 구현)
- 대한민국 파생상품 옵션 **호가, 체결 틱 데이터** (KoreanOption.py에 구현)
- 해외 선물 **호가, 체결 틱 데이터** (ForeignFutures.py에 구현)
- 해외 옵션 **호가, 체결 틱 데이터** (ForeignOption.py에 구현) <u><현재 작동하지 않음></u>



예를들어, 현재는 코스피 전종목 호가,체결 틱 데이터는 수집 가능하지만 내가 원하는 종목들을 선택해서 수집하는 기능은 구현되어 있지 않습니다. 

주의) 이와 관련되어서 발생하는 문제가 존재합니다. 해외 옵션 같은 경우에는 각 상품별, 종목수가 15,000종목이 넘습니다. 그렇기 때문에 이렇게 많은 종목들의 실시간 데이터들을 요청하게 되면 제대로 작동하지 않습니다. 그래서 현재 해외 옵션 호가,체결 틱 데이터는 제대로 기능하지 않습니다.



# 문의 사항

본 소스코드는 출저(현재의 깃허브 주소)만 밝히신다면 자유롭게 사용가능합니다.

문의사항 및 개선사항은 taehyun.jo.90@gmail.com으로 언제든지 연락바랍니다. 감사합니다.





