import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QSystemTrayIcon, QMenu
)
from PySide6.QtGui import (
    QIcon, QFont, QAction, QPixmap
)
from PySide6.QtCore import Qt
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import base64
from selenium.webdriver.support import expected_conditions as EC
import schedule
import threading

# Note: Replace 'xxxxxxxx' with your actual Imperial College student ID or faculty ID.
# Example: "https://www.imperial.ac.uk/timetabling/calendar/cal?vt=agendaDay&dt=Today&et=student&fid0=xxxxxxxx"

def icon_from_base64(data: str) -> QIcon:
    byte_data = base64.b64decode(data)
    pixmap = QPixmap()
    pixmap.loadFromData(byte_data)
    return QIcon(pixmap)

b64 = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAFo9M/3AAAACXBIWXMAAA7DAAAOwwHHb6hkAAAAz0lEQVR4nLRTbQ6DIAwF4wlMvKMH8K/xeC6zy3aEJct2CoFREKgdRrZkTZ5ofZTXD4QQF+NhH2hbT3zpurv73TRX7+j7h3O07Y1SyRattVFKJUddM0YwdtzZYiIATvCh0s4PwWCkhJUA+Qh5lBOowIkTZpc4FmBZtFulzBwxji+7nvY1HBDADMOTFYlo4FZV36f5KzYfc5yWPcMpSvKyCiD2FZP2vQ2J0x4fpICTg2X1AXhp/xdgdlcojAUCDccj+PBqpTHJKuA3g6OwBqV4AwAA//8NLAylAAAABklEQVQDAH5LIM/fEiVjAAAAAElFTkSuQmCC"

def ifilogin():
    driver_path = os.path.join(os.path.dirname(__file__), "chromedriver", "chromedriver.exe")
    chrome_path = os.path.join(os.path.dirname(__file__), "mnch", "bin","chrome.exe")
    service = ChromeService(executable_path=driver_path)
    #service = ChromeService(executable_path="C:/chromedriver/chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.binary_location = chrome_path
    #options.add_argument('headless')
    options.add_argument(r'--user-data-dir=C:\ChromeUserData')
    options.add_argument(r'--user-data-dir=' + os.path.join(os.path.dirname(__file__), "user_data"))
    driver = webdriver.Chrome(service=service, options=options)
    # 打开一个网站
    driver.get("https://www.imperial.ac.uk/timetabling/calendar/cal?vt=agendaDay&dt=Today&et=student&fid0=xxxxxxxx")
    time.sleep(1.3)
    iflogin = driver.find_elements(By.CLASS_NAME, "login-paginated-page")
    print("didiflogin" + str(len(iflogin)))
    if len(iflogin) != 0:
        driver.quit()
        loginpage()
    else:
        driver.quit()

def loginpage():
    driver_path = os.path.join(os.path.dirname(__file__), "chromedriver", "chromedriver.exe")
    chrome_path = os.path.join(os.path.dirname(__file__), "mnch", "bin","chrome.exe")
    service = ChromeService(executable_path=driver_path)
    #service = ChromeService(executable_path="C:/chromedriver/chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.binary_location = chrome_path
    #options.add_argument('headless')
    options.add_argument(r'--user-data-dir=C:\ChromeUserData')
    options.add_argument(r'--user-data-dir=' + os.path.join(os.path.dirname(__file__), "user_data"))
    driver = webdriver.Chrome(service=service, options=options)
    # 打开一个网站
    driver.get("https://www.imperial.ac.uk/timetabling/calendar/cal?vt=agendaDay&dt=Today&et=student&fid0=xxxxxxxx")
    time.sleep(1.3)
    iflogin = driver.find_elements(By.CLASS_NAME, "login-paginated-page")
    print(len(iflogin))
    if len(iflogin) != 0:
        WebDriverWait(driver, 600).until(
        EC.presence_of_element_located((By.ID, "eventFilter"))  # 你登录后页面才会出现的元素
        )
        s = driver.find_elements(By.CLASS_NAME, "small")[0].text
        print(s)
        number = s.split(" ")[-1]
        print(number)
        with open("C:/ChromeUserData/imperial.txt", "w") as f:
            f.write(number)
    driver.quit()

def gettt():
    ifilogin()
    with open("C:/ChromeUserData/imperial.txt", "r") as f:
        number = f.read()
    ws = "https://www.imperial.ac.uk/timetabling/calendar/cal?vt=agendaDay&dt=Today&et=student&fid0=" + number
    driver_path = os.path.join(os.path.dirname(__file__), "chromedriver", "chromedriver.exe")
    chrome_path = os.path.join(os.path.dirname(__file__), "mnch", "bin","chrome.exe")
    service = ChromeService(executable_path=driver_path)
    #service = ChromeService(executable_path="C:/chromedriver/chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.binary_location = chrome_path
    #options.add_argument('headless')
    options.add_argument(r'--user-data-dir=C:\ChromeUserData')
    options.add_argument(r'--user-data-dir=' + os.path.join(os.path.dirname(__file__), "user_data"))
    driver = webdriver.Chrome(service=service, options=options)
    l = []
    #driver.get("https://www.imperial.ac.uk/timetabling/calendar/cal?vt=agendaDay&dt=2025-05-06&et=student&fid0=xxxxxxxx")
    driver.get(ws)
    time.sleep(1.3)
    iflogin = driver.find_elements(By.CLASS_NAME, "login-paginated-page")
    print(len(iflogin))
    if len(iflogin) != 0:
        return 'Need to login'
    elements = driver.find_elements(By.CLASS_NAME, "fc-content")
    #print(elements[0].text)
    if len(elements) == 0:
        driver.quit()
        return 'NO classes today' 
    for element in elements:
        e = element.text.split("\n")
        if len(e) <= 4:
            driver.quit()
            return 'NO classes today'
        l.append(e[0]+'\n'+e[1]+'\n'+e[4])
    j = ''
    for i in l:
        j += (i + '\n')
    # 关闭浏览器
    driver.quit()
    return j



class FloatingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnBottomHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.8)
        self.resize(1920, 1080)
        screen = QApplication.primaryScreen().availableGeometry()
        self.move((screen.width() - self.width()) // 2, 0)

        self.label = QLabel(gettt(), self)
        self.label.setFont(QFont('Arial', 10))
        self.label.setStyleSheet("color: white; background: transparent;")
        self.label.move(screen.width() / 2, 0)
        self.label.setAlignment(Qt.AlignCenter)

        self.start_schedule_loop()  # 启动定时任务

    def update_label(self):
        print("⏰ 正在更新课程内容...")
        self.label.setText(gettt())

    def start_schedule_loop(self):
        #schedule.every().day.at("07:00").do(self.update_label)  # 可改时间
        self.update_label()
        schedule.every().hour.do(self.update_label)
        def run_schedule():
            while True:
                schedule.run_pending()
                time.sleep(60)

        threading.Thread(target=run_schedule, daemon=True).start()

class TrayApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = FloatingWidget()

        # 创建托盘图标
        icon = icon_from_base64(b64)
        self.tray = QSystemTrayIcon(icon)
        self.tray.setVisible(True)

        # 创建托盘菜单
        self.menu = QMenu()
        self.show_action = QAction("Show")
        self.hide_action = QAction("Hide")
        self.quit_action = QAction("Exit")

        self.show_action.triggered.connect(self.window.show)
        self.hide_action.triggered.connect(self.window.hide)
        self.quit_action.triggered.connect(self.exit_app)

        self.menu.addAction(self.show_action)
        self.menu.addAction(self.hide_action)
        self.menu.addSeparator()
        self.menu.addAction(self.quit_action)

        self.tray.setContextMenu(self.menu)

    def exit_app(self):
        self.tray.hide()
        self.window.close()
        sys.exit()

    def run(self):
        self.window.show()
        self.app.exec()

if __name__ == "__main__":
    app = TrayApp()
    app.run()
