# Interpark Ticketing Macro

<div>
    <img src="https://img.shields.io/badge/python-3-brightgreen"> <img src="https://img.shields.io/badge/webdriver-selenium-brightgreen"> <img src="https://img.shields.io/badge/BeautifulSoup-bs4-brightgreen"> <img src="https://img.shields.io/badge/PyQt-PyQt5-brightgreen"> <img src="https://img.shields.io/badge/chromedriver-ver.86-brightgreen">
</div>

> 파일 셋팅 및 간단한 사용법

    (0) chrome 이 설치되어있어야하고, 현재 chrome version과 동일한 chromedriver를 다운.

    (1) 다운받은 chromedriver.exe & ticketingmacro-ui.ui 파일을 macro.py 파일과 동일한 경로에 셋팅.

    (2-1) 해당 경로에서 CLI를 통해 python macro.py 또는 (2-2) pyinstaller 를 통해 macro.py 를 .exe 파일로 conversion 하여 실행.

    (3) 예매할 공연 또는 콘서트(이하 편의상 공연)를 확인 후, 해당 공연의 코드 / 날짜 / 회차 / 좌석 등을 미리 파악.

<p align="center">
    <img src="https://github.com/holyfrog666/ticketing/blob/master/tm_manual.PNG">   
    <p align="center">&lt;첫 실행 화면&gt;</p>
</p>

    (4) 실행 화면에서 미리 기입된 양식에 맞게 정보들을 기입 후, (예매정보 입력) 및 (로그인 버튼)을 누르고 잠시 대기.

    (5) 네이버 시계창과 시간 동기화가 끝나고 (티켓팅 시작) 버튼을 통해 티켓팅을 시작합니다.

    (6) 도중에 로딩 오류나, 티켓팅 화면에서 날짜 또는 회차가 제대로 선택이 안되고 자동으로 넘어가지 않는 경우 (다시 티켓팅 시작 버튼)을 눌러 티켓팅을 재시도합니다.

    위 코드는 구글의 많은 선행코드를 참조하여 만들었습니다.

> 악용 금지

    티켓 관련 매크로는 불순한 의도로 이용될 요지가 다소 있는 관계로 아래와 같은 내용을 미리 알려드립니다.
    python 및 selenium 등 study 가 목적이므로, study 용으로 사용 또는 참고하시는 것은 괜찮지만 상업적 목적 또는 불순한 의도로 수정 또는 배포 등의 악용은 불가합니다.
    해당 코드를 작성자(holyfrog666)가 의도하지 않은 목적으로 사용될 경우에 따른 모든 책임은 사용자에게 있으며, 작성자는 아무런 책임이 없음을 알려드립니다.
