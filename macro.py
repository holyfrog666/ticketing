# Macro by holyfrog666
# 취미, 공부 및 연구 등을 1차적 목적으로 만들었습니다.
# 구글링을 통해 좋은 코드들을 응용한 바 있습니다.
# 해당 소스들의 제작자들과 동일하게 상업적으로 배포 및 공유하는 것은 금지합니다.

# 인터파크 콘서트, 뮤지컬 등 공연 티켓팅용
# 현재 코드상 미니맵/구역 구분은 해놨지만, 미니맵 있는 공연의 경우 X

import sys
import os
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *

form_class = uic.loadUiType('ticketingmacro-ui.ui')[0]

# 활동로그를 기록하는 함수


def log(logText):
    # 현재 시간을 구한다.
    now = time.localtime()
    nowTime = "%04d-%02d-%02d %02d:%02d:%02d" % (
        now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

    # 활동로그를 기록한다.
    log = open("log.txt", "a", encoding="utf-8")
    log.write("[" + nowTime + "] " + str(logText) + "\n")
    log.close()


class MyWindow(QtWidgets.QMainWindow, form_class):
    is_data_disabled = False  # 정보 입력창 비활성화 여부
    time = None  # 스레드로부터 받아오는 현재 시간

    # 매크로 프로그램 정의
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('인터파크 티켓팅 매크로')
        self.setWindowIcon(QIcon('interpark_icon.ico'))
        self.user_password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.seats_number_spinbox.setValue(1)
        self.date_edit.setDate(QtCore.QDate.currentDate())
        self.restart_macro.clicked.connect(self.restart)
        self.apply_btn.clicked.connect(self.initData)  # 확인 버튼 클릭
        self.login_btn.clicked.connect(self.startLogin)  # 로그인 버튼 클릭
        self.cb_checkBox_1.stateChanged.connect(self.checkBoxState1)
        self.cb_checkBox_2.stateChanged.connect(self.checkBoxState2)
        self.cb_checkBox_3.stateChanged.connect(self.checkBoxState3)
        self.cb_checkBox_4.stateChanged.connect(self.checkBoxState4)
        self.cb_checkBox_5.stateChanged.connect(self.checkBoxState5)
        self.start_ticketing_btn.clicked.connect(
            self.startTicketing)  # 시작 버튼 클릭
        self.seats_number_spinbox.valueChanged.connect(
            self.checkSeatsNumber)  # 좌석 개수 변경
        # 로그인 및 시작 버튼 비활성화
        self.disableElements(self.login_btn, self.start_ticketing_btn)

    # 프로그램 재시작 함수
    def restart(self):
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

    # 매크로 프로그램 정보 입력 데이터 바인딩
    def initData(self):
        if not self.is_data_disabled:  # 정보 입력창 활성화 시
            self.user_id = self.user_id_input.text()  # 아이디
            self.user_password = self.user_password_input.text()  # 비밀번호
            self.product_code = self.product_code_input.text()  # 공연 코드
            self.product_seq = self.product_seq_input.text()  # 공연 코드
            self.seats_number = self.seats_number_spinbox.value()  # 좌석 개수

            self.cb1 = self.cb_checkBox_1.isChecked()   # 좌석등급 VIP 체크 여부
            self.cb2 = self.cb_checkBox_2.isChecked()   # 좌석등급 R 체크 여부
            self.cb3 = self.cb_checkBox_3.isChecked()   # 좌석등급 A 체크 여부
            self.cb4 = self.cb_checkBox_4.isChecked()   # 좌석등급 S 체크 여부
            self.cb5 = self.cb_checkBox_5.isChecked()   # 좌석등급 모두 체크 여부

            self.date = self.date_edit.date()  # 날짜
            self.date = self.date.toPyDate()
            self.date = str(self.date).replace('-', '')
            self.disableElements(self.user_id_input, self.user_password_input, self.product_code_input, self.product_seq_input, self.date_edit,
                                 self.seats_number_spinbox, self.cb_checkBox_1, self.cb_checkBox_2, self.cb_checkBox_3, self.cb_checkBox_4, self.cb_checkBox_5)  # 요소 비활성화
            self.is_data_disabled = True
            self.apply_btn.setText('수정')
            QtWidgets.QMessageBox.information(self, '완료', '정보 입력이 완료되었습니다.')
            # 로그인 및 시작 버튼 활성화
            self.enableElements(self.login_btn, self.start_ticketing_btn)

            self.directlink = 'http://poticket.interpark.com/Book/BookSession.asp?GroupCode={}&Tiki=N&Point=N&PlayDate={}&PlaySeq=001&BizCode=&BizMemberCode='.format(
                self.product_code, self.date)
            self.user_direct_link.setText(self.directlink)
        else:
            self.is_data_disabled = False
            self.apply_btn.setText('확인')
            self.enableElements(self.user_id_input, self.user_password_input, self.product_code_input, self.product_seq_input, self.date_edit,
                                self.seats_number_spinbox, self.cb_checkBox_1, self.cb_checkBox_2, self.cb_checkBox_3, self.cb_checkBox_4, self.cb_checkBox_5)  # 요소 활성화

    @QtCore.pyqtSlot(int)
    def checkBoxState1(self):
        if self.sender().isChecked() == True:
            self.cb_checkBox_5.setChecked(False)

    def checkBoxState2(self):
        if self.sender().isChecked() == True:
            self.cb_checkBox_5.setChecked(False)

    def checkBoxState3(self):
        if self.sender().isChecked() == True:
            self.cb_checkBox_5.setChecked(False)

    def checkBoxState4(self):
        if self.sender().isChecked() == True:
            self.cb_checkBox_5.setChecked(False)

    def checkBoxState5(self):
        if self.sender().isChecked() == True:
            self.cb_checkBox_1.setChecked(True)
            self.cb_checkBox_2.setChecked(True)
            self.cb_checkBox_3.setChecked(True)
            self.cb_checkBox_4.setChecked(True)
            self.cb_checkBox_5.setChecked(True)

    # 좌석 개수 변경
    def checkSeatsNumber(self):
        if self.seats_number_spinbox.value() > 4:
            self.seats_number_spinbox.setValue(4)
            QtWidgets.QMessageBox.critical(
                self, '좌석수 선택 다시 확인', '최대 좌석 개수는 4개입니다.')
        if self.seats_number_spinbox.value() < 1:
            self.seats_number_spinbox.setValue(1)
            QtWidgets.QMessageBox.critical(
                self, '좌석수 선택 다시 확인', '최소 좌석 개수는 1개입니다.')

    # 요소들 입력받아 한꺼번에 활성화
    def enableElements(self, *elements):
        for element in elements:
            element.setEnabled(True)

    # 요소들 입력받아 한꺼번에 비활성화
    def disableElements(self, *elements):
        for element in elements:
            element.setEnabled(False)

    # 로그인
    def startLogin(self):
        self.time_th = TimeThread()
        if self.apply_btn.text() == '확인':  # 확인 버튼을 누르지 않았을 때
            QtWidgets.QMessageBox.critical(
                self, '확인 버튼을 꼭 눌러주세여', '예매 정보를 입력하세요.')
        else:
            # Dictionary 형식으로 정보 전달
            ticketing_data_to_send = {
                'user_id': self.user_id,  # 아이디
                'user_pw': self.user_password,  # 비밀번호
                'product_code': self.product_code,  # 공연 번호
                'product_seq': self.product_seq,  # 회차(공연시간)
                'date': self.date,  # 공연 날짜
                'seats_number': self.seats_number,  # 좌석 개수
                'cb_check1': self.cb1,  # 좌석 등급 체크
                'cb_check2': self.cb2,  # 좌석 등급 체크
                'cb_check3': self.cb3,  # 좌석 등급 체크
                'cb_check4': self.cb4,  # 좌석 등급 체크
                'cb_check5': self.cb5,  # 좌석 등급 체크
                'time_signal': self.time_th.time_signal  # 시간 스레드
            }
            self.apply_btn.setEnabled(False)  # 확인(수정) 버튼 비활성화
            self.login_btn.setEnabled(False)  # 로그인 버튼 비활성화
            # 시간/티켓팅 스레드 시작
            self.time_th.start()
            self.time_th.time_signal.connect(self.changeTime)
            self.ticketing_th = TicketingThread(
                ticketing_data=ticketing_data_to_send)
            self.ticketing_th.start()

    # 티켓팅 시작
    def startTicketing(self):
        self.ticketing_th.start_ticketing = True
        self.apply_btn.setEnabled(False)  # 확인(수정) 버튼 비활성화
        self.login_btn.setEnabled(False)  # 로그인 버튼 비활성화
        self.start_ticketing_btn.setText(
            '티켓팅 진행중, 클릭시 티켓팅 다시 시작')  # 티켓팅 시작 버튼 텍스트 변경

    # 타이머 시작
    def startTimer(self):
        self.time_th = TimeThread()
        self.time_th.start()
        self.time_th.time_signal.connect(self.changeTime)

    @QtCore.pyqtSlot(str)
    def changeTime(self, time):
        if time == 'error':  # 웹드라이버(시계) 종료시 알림
            QtWidgets.QMessageBox.critical(
                self, '네이버 시간 크롬창 끄지 마세요..', '네이버 시간 크롬창 끄지마셈. ㅡㅡ')
        else:
            self.now_time.setText(time)


class TimeThread(QtCore.QThread):
    time_signal = QtCore.pyqtSignal(str)
    navertimehandle = ''

    def run(self):
        while True:
            self.driver = webdriver.Chrome('chromedriver.exe')
            # 네이버 시계 접속
            self.driver.get(
                'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EB%84%A4%EC%9D%B4%EB%B2%84+%EC%8B%9C%EA%B3%84&oquery=%EC%8B%9C%EA%B3%84&tqi=UEMiLdprvTossFQzFhCssssssKG-165498')

            while True:
                try:
                    text = self.driver.find_element_by_css_selector(
                        '#_cs_domestic_clock > div._timeLayer.time_bx > div > div').text  # 네이버 시계 text
                    text = text.replace('\n', '').replace(' ', '')[0:8]
                    dayornight = self.driver.find_element_by_css_selector(
                        '#_cs_domestic_clock > div._timeLayer.time_bx > div > div > span:last-child').text    # 네이버 시계 AM PM text
                    timetext = text + ' ' + dayornight
                except:
                    self.time_signal.emit('error')  # 웹드라이버(시계) 종료 시 error emit
                    break

                self.time_signal.emit(''.join(timetext))


class TicketingThread(QtCore.QThread):
    def __init__(self, ticketing_data, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.user_id = ticketing_data['user_id']
        self.user_password = ticketing_data['user_pw']
        self.product_code = ticketing_data['product_code']
        self.product_seq = ticketing_data['product_seq']
        self.date = ticketing_data['date']
        self.seats_number = ticketing_data['seats_number']
        self.cb_check1 = ticketing_data['cb_check1']
        self.cb_check2 = ticketing_data['cb_check2']
        self.cb_check3 = ticketing_data['cb_check3']
        self.cb_check4 = ticketing_data['cb_check4']
        self.cb_check5 = ticketing_data['cb_check5']
        self.time_signal = ticketing_data['time_signal']
        self.driver = webdriver.Chrome('chromedriver.exe')
        self.is_logined = False  # 로그인 여부 False
        self.start_ticketing = False  # 시작 여부 False

    # 로그인

    def login(self):
        self.driver.set_window_position(60, 60)
        self.driver.get('https://ticket.interpark.com/Gate/TPLogin.asp')
        iframes = self.driver.find_elements_by_tag_name('iframe')
        self.driver.switch_to.frame(iframes[0])
        self.driver.find_element_by_id('userId').send_keys(self.user_id)
        self.driver.find_element_by_id('userPwd').send_keys(self.user_password)
        self.driver.find_element_by_id('btn_login').click()
        self.driver.get('https://ticket.interpark.com/')  # 인터파크 메인 페이지로 강제 접속

    def selectSeat(self):
        # 티켓 매크로 시작
        self.failed_to_get_ticket = False  # 취켓팅용-기본적으로 성공으로 표시

        # 공연정보를 통한 공연 페이지 연결
        self.url = 'http://ticket.interpark.com/Ticket/Goods/GoodsInfo.asp?GoodsCode={}'.format(
            self.product_code)
        self.driver.get(self.url)

        # 예매하기
        try:
            # 공연 기간 정보 가져오기
            Dnow = self.driver.find_element_by_xpath('//p[@class="time"]').text
            Dnow = Dnow[Dnow.find('~ ') + 2:].replace('.', '')

            # 예매창 열기
            self.driver.execute_script('javascript:fnNormalBooking();')

            # 예매창 객체 받아오기
            self.driver.switch_to.window(self.driver.window_handles[1])

            # 멤버쉽 여부 확인 및 일반 회원입니다.
            try:
                self.driver.find_element_by_xpath(
                    "//img[@alt='일반회원 구매']").click()
                self.driver.switch_to.window(self.driver.window_handles[1])

            except:
                elem = ''

            # 알림창 닫기 버튼 클릭
            try:
                self.driver.execute_script(
                    'javascript:fnBookNoticeShowHide('');')
            except:
                elem = ''

            # 날짜/회차 선택 (1단계)
            try:
                # 날짜
                # 1단계 프레임 받아오기
                frame = self.driver.find_element_by_id('ifrmBookStep')
                self.driver.switch_to.frame(frame)

                # 달(月) 바꾸기
                self.driver.execute_script(
                    "javascript: fnChangeMonth('" + self.date[:6] + "');")

                # 날짜 선택하기
                try:
                    # 달력 정보가 존재할 경우
                    # 달력 정보 가져오기
                    # print(driver.page_source)
                    bs4 = BeautifulSoup(self.driver.page_source, "html.parser")
                    calender = bs4.findAll('a', id='CellPlayDate')
                    elem = calender[0]["onclick"]

                    # 사용자의 입력값과 일치하는 함수를 찾는다.
                    for i in range(0, len(calender)):
                        if "fnSelectPlayDate(" + str(i) + ", '" + self.date + "')" == calender[i]["onclick"]:
                            elem = calender[i]["onclick"]
                            break

                    # 해당 날짜 선택하기
                    self.driver.execute_script("javascript:" + elem)

                except:
                    # 달력 정보가 존재하지 않을 경우
                    # 공연가능한 마지막 달로 이동한다
                    self.driver.execute_script(
                        "javascript: fnChangeMonth('" + Dnow[:6] + "');")

                    # 달력 정보 가져오기
                    # print(driver.page_source)
                    bs4 = BeautifulSoup(self.driver.page_source, "html.parser")
                    calender = bs4.findAll('a', id='CellPlayDate')
                    Dnow = calender[len(calender) - 1]["onclick"]

                    # 해당 날짜 선택하기
                    self.driver.execute_script("javascript:" + Dnow)

                # 페이지 로딩 대기
                time.sleep(0.3)

                # 회차
                # 회차 정보 가져오기
                def seqtextcheck(tag):
                    return tag.name == 'a' and self.product_seq in tag.contents[0]

                bs4 = BeautifulSoup(self.driver.page_source, "html.parser")
                timeList = bs4.find('div', class_='scrollY').find(
                    'span', id='TagPlaySeq').findAll('a', id='CellPlaySeq')
                timeListseq = bs4.find('div', class_='scrollY').find(
                    'span', id='TagPlaySeq').find(seqtextcheck)

                # 회차 유효성 검사
                try:
                    if len(timeListseq) > 0:
                        elem = timeListseq["onclick"]
                    else:
                        elem = timeList[0]["onclick"]
                except:
                    elem = timeList[0]["onclick"]

                # 회차 선택하기
                self.driver.execute_script("javascript:" + elem)

                # 다음단계
                # 메인 프레임 받아오기
                self.driver.switch_to.default_content()

                # 2단계로 넘어가기
                self.driver.execute_script("javascript:fnNextStep('P');")

                # 당일 예매 경고창 감지
                try:
                    alert = self.driver.switch_to.alert()
                    alert.accept()
                except:
                    elem = ''

            except:
                # 관람일/회차선택 단계가 없을 경우
                elem = ''

            # 좌석 선택 (2단계)
            # 안심 예매
            # 2단계 프레임 받아오기
            self.driver.switch_to.default_content()
            frame = self.driver.find_element_by_id('ifrmSeat')
            self.driver.switch_to.frame(frame)

            # 페이지 로딩 대기
            time.sleep(0.2)

            # Captcha hacked
            try:
                # Captcha가 있을 경우
                # Captcha 사진 가져오기
                bs4 = BeautifulSoup(self.driver.page_source, "html.parser")
                Captcha = bs4.find('div', class_='capchaInner').find(
                    'img', id='imgCaptcha')['src']

                self.driver.execute_script("javascript:capchaHide();")
                print("[ Captcha O ] 캡챠가 존재합니다. 캡챠를 접어둡니다.")

            except:
                # Captcha가 없을 경우
                elem = ''
                print("[ Captcha X ] 캡챠가 존재하지 않습니다.")

            # 좌석 찾기
            # 2단계 프레임 받아오기
            print("[ 좌석 찾기 진행합니다. ]")
            self.driver.switch_to.default_content()
            frame = self.driver.find_element_by_id('ifrmSeat')
            self.driver.switch_to.frame(frame)

            # 미니맵 여부 검사
            try:
                frame = self.driver.find_element_by_id('ifrmSeatView')
                self.driver.switch_to.frame(frame)
                bs4 = BeautifulSoup(self.driver.page_source, "html.parser")
                elem = bs4.find('map')

            except:
                elem = None

            # 미니맵 및 구역의 상태에 따라 동작 구분
            # 미니맵 존재 O / 구역 존재 O
            if elem != None:
                # 미니맵 존재 O
                print("[ 미니맵 O ] 구역 리스트를 받아옵니다")
                # 구역 리스트 받아오기
                areaList = bs4.findAll('area')

                # 빈 좌석 찾기
                seatch = False
                while seatch != True:
                    for i in range(0, len(areaList) + 1):
                        # 좌석 프레임 받아오기
                        self.driver.switch_to.default_content()
                        frame = self.driver.find_element_by_id('ifrmSeat')
                        self.driver.switch_to.frame(frame)
                        frame = self.driver.find_element_by_id(
                            'ifrmSeatDetail')
                        self.driver.switch_to.frame(frame)

                        # 좌석 정보 읽어오기
                        bs4 = BeautifulSoup(
                            self.driver.page_source, "html.parsere")
                        seatList = bs4.findAll('img', class_='stySeat')

                        # 좌석 존재할 경우, error X -> except 실행 X
                        try:
                            # 좌석 등급 조건에 따라서 seatch 변수 변경 및 break
                            for i in range(0, len(seatList)):
                                seat = seatList[i]
                                text = seat['alt'][seat['alt'].find('[') + 1:]
                                seatIndex = i

                                if (text.find('VIP') != -1) & (self.cb_check1 == True):
                                    seatch = True
                                    break

                                if (text.find('R') != -1) & (self.cb_check2 == True):
                                    seatch = True
                                    break

                                if (text.find('S') != -1) & (self.cb_check3 == True):
                                    seatch = True
                                    break

                                if (text.find('A') != -1) & (self.cb_check4 == True):
                                    seatch = True
                                    break

                                if self.cb_check5 == 1:
                                    seatch = True
                                    break

                                print('seatch = ' + seatch)
                                print('seat = ' + seat)

                            # 좌석 유무 검사
                            if seatch == True:
                                # 좌석이 있는 경우
                                # 좌석 선택하기
                                if self.seats_number < 2:
                                    self.driver.execute_script(
                                        seat['onclick'] + ";")
                                else:
                                    seatnum = self.seats_number
                                    for j in range(0, seatnum):
                                        self.driver.execute_script(
                                            seatList[seatIndex + j]['onclick'] + ";")
                                        # print(seatIndex+j)

                                # 2단계 프레임 받아오기
                                self.driver.switch_to.default_content()
                                frame = self.driver.find_element_by_id(
                                    'ifrmSeat')
                                self.driver.switch_to.frame(frame)

                                # 3단계 넘어가기 실행
                                self.driver.execute_script(
                                    "javascript:fnSelect();")

                                # 로그
                                print('빈좌석 찾기 성공')

                                # 페이지 로딩 대기
                                time.sleep(0.3)

                                # 반복문 break
                                break

                        # 좌석이 존재하지 않는 경우, error O -> except 실행 O
                        except:
                            print('[ 미니맵 O / 구역 O ] 좌석이 존재하지 않습니다.')
                            # 좌석이 없는 경우
                            # 미니맵 프레임 받아오기
                            self.driver.switch_to.default_content()
                            frame = self.driver.find_element_by_id('ifrmSeat')
                            self.driver.switch_to.frame(frame)
                            frame = self.driver.find_element_by_id(
                                'ifrmSeatView')
                            self.driver.switch_to.frame(frame)

                            # 구역 리스트 받아오기
                            bs4 = BeautifulSoup(
                                self.driver.page_source, "html.parser")
                            areaList = bs4.findAll('area')

                            # 구역 바꾸기
                            if i == len(areaList):
                                # 마지막 반복 단계
                                self.driver.execute_script(areaList[0]["href"])
                            else:
                                # 그 외
                                try:
                                    # 구역 리스트의 크기가 같을 경우
                                    self.driver.execute_script(
                                        areaList[i]["href"])
                                except:
                                    # 구역 리스트의 크기가 다를 경우
                                    self.driver.execute_script(
                                        areaList[0]["href"])

                            # 페이지 로딩 대기
                            time.sleep(0.3)

                            # 좌석을 불러오기 경고창 감지
                            try:
                                alert = self.driver.switch_to.alert()
                                alert.accept()
                                time.sleep(3)
                            except:
                                elem = ''

            else:
                try:
                    # 미니맵 존재 X
                    print("[ 미니맵 X ] 좌석 프레임을 받아옵니다")
                    # 좌석 프레임 받아오기
                    self.driver.switch_to.default_content()
                    frame = self.driver.find_element_by_id('ifrmSeat')
                    self.driver.switch_to.frame(frame)
                    frame = self.driver.find_element_by_id('ifrmSeatDetail')
                    self.driver.switch_to.frame(frame)

                    # 구역 존재여부 검사
                    bs4 = BeautifulSoup(self.driver.page_source, "html.parser")

                    # 미니맵 X, 구역 O
                    if bs4.find('area') != None:
                        # 구역 존재 O
                        print("[ 미니맵 X / 구역 O ] 구역리스트를 받아옵니다")
                        # 구역 리스트 받아오기
                        areaList = bs4.findAll('area')

                        # 빈 좌석 찾기
                        seatch = False
                        while seatch != True:
                            needseatupdate = False
                            for i in range(0, len(areaList)):
                                # 좌석 프레임 받아오기
                                self.driver.switch_to.default_content()
                                frame = self.driver.find_element_by_id(
                                    'ifrmSeat')
                                self.driver.switch_to.frame(frame)
                                frame = self.driver.find_element_by_id(
                                    'ifrmSeatDetail')
                                self.driver.switch_to.frame(frame)

                                # 구역 바꾸기
                                self.driver.execute_script(
                                    '"' + areaList[i]["href"] + ';"')
                                print('"' + areaList[i]["href"] + ';"')

                                # 좌석 정보를 읽어온다.
                                bs4 = BeautifulSoup(
                                    self.driver.page_source, "html.parser")
                                seatList = bs4.findAll('span', value='N')

                                # 좌석 존재 O, error X -> except 실행 X
                                try:
                                    # 좌석 등급 조건에 따른 가부
                                    for i in range(0, len(seatList)):
                                        seat = seatList[i]
                                        text = seat['title'][seat['title'].find(
                                            '[') + 1:]
                                        print('text = ' + text)
                                        print(
                                            'seat["title"] = ' + seat['title'])
                                        seatIndex = i

                                        if (text.find("VIP") != -1) & (self.cb_check1 == True):
                                            seatch = True
                                            break
                                        if (text.find("R") != -1) & (self.cb_check2 == True):
                                            seatch = True
                                            break
                                        if (text.find("S") != -1) & (self.cb_check3 == True):
                                            seatch = True
                                            break
                                        if (text.find("A") != -1) & (self.cb_check4 == True):
                                            seatch = True
                                            break
                                        if self.cb_check4 == 1:
                                            seatch = True
                                            break

                                    print('seatch = ' + seatch)
                                    print('seat = ' + seat)

                                    # 좌석 유무를 검사한다.
                                    if seatch == True:
                                        # 좌석이 있을 경우
                                        # 좌석 선택하기
                                        if self.seats_number < 2:
                                            self.driver.execute_script(
                                                seat['onclick'] + ";")
                                        else:
                                            seatnum = self.seats_number
                                            for j in range(0, seatnum):
                                                self.driver.execute_script(
                                                    seatList[seatIndex+j]['onclick'] + ";")
                                                # print(seatIndex+j)

                                        # 2단계 프레임 받아오기
                                        self.driver.switch_to.default_content()
                                        frame = self.driver.find_element_by_id(
                                            'ifrmSeat')
                                        self.driver.switch_to.frame(frame)

                                        # 3단계 넘어가기
                                        self.driver.execute_script(
                                            "javascript:fnSelect();")

                                        # 활동로그
                                        print("빈좌석 찾기 성공")

                                        # 페이지 로딩 대기
                                        time.sleep(0.5)

                                        # 반복문 종료
                                        seatch = True
                                        break

                                # 좌석이 존재 X error O -> except 실행
                                except:
                                    print('[ 미니맵 X / 구역 O ] 좌석이 존재하지 않습니다.')
                                    needseatupdate = True

                            if needseatupdate == True:
                                # 좌석이 없는 경우
                                # 2단계 프레임 받아오기
                                self.driver.switch_to.default_content()
                                frame = self.driver.find_element_by_id(
                                    'ifrmSeat')
                                self.driver.switch_to.frame(frame)

                                # 좌석도 전체보기
                                self.driver.execute_script(
                                    "javascript:fnSeatUpdate();")
                                print('좌석 업데이트했습니다(fnSeatUpdate();)')

                                # 페이지 로딩 대기
                                time.sleep(0.5)

                                # 좌석을 불러오기 경고창 감지
                                try:
                                    alert = self.driver.switch_to.alert()
                                    alert.accept()
                                    time.sleep(3)
                                except:
                                    elem = ''

                    # 미니맵 = X, 구역 = X
                    else:
                        # 구역이 존재하지 않을 경우
                        # 빈 좌석 찾기
                        while (True):
                            print('[ 미니맵 X, 구역 X ] 빈 좌석을 찾기위해 좌석 프레임을 받아옵니다.')
                            # 좌석 프레임 받아오기
                            self.driver.switch_to.default_content()
                            frame = self.driver.find_element_by_id('ifrmSeat')
                            self.driver.switch_to.frame(frame)
                            frame = self.driver.find_element_by_id(
                                'ifrmSeatDetail')
                            self.driver.switch_to.frame(frame)

                            # 좌석 정보를 읽어온다.
                            bs4 = BeautifulSoup(
                                self.driver.page_source, "html.parser")
                            seatList = bs4.findAll('img', class_='stySeat')

                            # 좌석 존재 O, error X -> except 실행 X
                            try:
                                # if Len(seatList) > 0:
                                # 좌석 등급 조건에 따른 가부
                                for i in range(0, len(seatList)):
                                    seat = seatList[i]
                                    text = seat['alt'][seat['alt'].find(
                                        '[') + 1:]
                                    print('text = ' + text)
                                    print('seat["title"] = ' + seat['title'])
                                    seatIndex = i

                                    if (text.find("VIP") != -1) & (self.cb_check1 == True):
                                        seatch = True
                                        break
                                    if (text.find("R") != -1) & (self.cb_check2 == True):
                                        seatch = True
                                        break
                                    if (text.find("S") != -1) & (self.cb_check3 == True):
                                        seatch = True
                                        break
                                    if (text.find("A") != -1) & (self.cb_check4 == True):
                                        seatch = True
                                        break
                                    if self.cb_check5 == 1:
                                        seatch = True
                                        break

                                time.sleep(0.3)

                                # 좌석 유무를 검사한다.
                                if seatch == True:
                                    # 좌석이 있을 경우
                                    # 좌석 선택하기
                                    if self.seats_number < 2:
                                        self.driver.find_element_by_xpath(
                                            "//img[@title='" + seat['title'] + "']").click()
                                    else:
                                        seatnum = self.seats_number
                                        for j in range(0, seatnum):
                                            self.driver.find_element_by_xpath(
                                                "//img[@title='" + seatList[seatIndex+j]['title'] + "']").click()
                                            # print(seatIndex+j)

                                    # 2단계 프레임 받아오기
                                    self.driver.switch_to.default_content()
                                    frame = self.driver.find_element_by_id(
                                        'ifrmSeat')
                                    self.driver.switch_to.frame(frame)

                                    # 3단계 넘어가기
                                    self.driver.execute_script(
                                        "javascript:fnSelect();")

                                    # 활동로그
                                    # log("빈좌석 찾기 성공")

                                    # 페이지 로딩 대기
                                    time.sleep(0.3)
                                    break

                            # 좌석 존재 X, error O -> except 실행
                            except:
                                print('[ 미니맵 X / 구역 X ] 좌석이 존재하지 않습니다.')

                                # 2단계 프레임 받아오기
                                self.driver.switch_to.default_content()
                                frame = self.driver.find_element_by_id(
                                    'ifrmSeat')
                                self.driver.switch_to.frame(frame)

                                # 좌석 다시 선택 (새로고침)
                                self.driver.execute_script(
                                    "javascript:fnRefresh();")
                                print('좌석 업데이트했습니다(fnSeatUpdate();)')

                                # 페이지 로딩 대기
                                time.sleep(0.5)

                                # 좌석을 불러오기 경고창 감지
                                try:
                                    alert = self.driver.switch_to.alert()
                                    alert.accept()
                                    time.sleep(3)
                                except:
                                    elem = ''
                                continue

                except:
                    # 좌석 선택 단계가 없을 경우
                    elem = ''
        except:
            pass

        else:
            pass

    @QtCore.pyqtSlot(str)
    def run(self):
        # 로그인되지 않았다면 로그인
        if not self.is_logined:
            self.login()
            self.is_logined = True
        while True:
            if self.start_ticketing:
                self.selectSeat()  # 티켓팅 시작
                if not self.failed_to_get_ticket:  # 취켓팅인데 성공한 경우
                    self.start_ticketing = False
                if self.failed_to_get_ticket:  # 취켓팅인데 실패한 경우
                    pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
