# Interpark Ticketing Macro

> 설명

python으로 구현했고 처음 구글링 초기에 PyQt4로 구현된 코드들이 많았지만 PyQt5가 latest version이라서 PyQt5로 UI를 구현했습니다.  
Selenium을 사용하여 web 요소에 접근하였고 FireFox gecko webdriver가 안정적이라는 얘기를 봤지만 Chrome이 좀 더 친숙해서 Chromedriver를 사용하였습니다.  
Interpark Ticketing Page에서 콘서트, 뮤지컬 등 다양한 분야에서 티켓팅 서비스를 제공하지만 매 티켓팅마다 Ticket seat DOM 구성이 다르게 되어 있는 부분이 있는데(미니맵 여부 또는 섹터 여부 등),  
현업이 더 중요한 관계로, 코드 내부에 분기처리는 해놓았으나 완벽하게 작동하는 수준까지 코드를 마무리하진 않았습니다.  
pyinstaller를 통해 exe파일로 build 후, 테스팅에 성공했고 실제로 예매도 성공적으로 이루어졌습니다.  
저처럼 python 또는 selenium 등을 공부하시는 분들에게는 한번은 다뤄볼만한 좋은 예제가 되었으면 합니다.  
python이 친숙하지 않아서 혹시 코드를 보고 feedback을 주시는 분들께서는 이점 참고해서 전달주시면 감사하고, 시간적 여유가 있을 때 적극 반영할 수 있도록 하겠습니다.

<div>
    <img src="https://img.shields.io/badge/python-3-brightgreen"> <img src="https://img.shields.io/badge/webdriver-selenium-brightgreen"> <img src="https://img.shields.io/badge/BeautifulSoup-bs4-brightgreen"> <img src="https://img.shields.io/badge/PyQt-5-brightgreen"> <img src="https://img.shields.io/badge/chromedriver-ver.86-brightgreen">
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
