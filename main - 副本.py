import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QSystemTrayIcon, QMenu
)
from PySide6.QtGui import QIcon, QFont, QAction, QPixmap
from PySide6.QtCore import Qt
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import base64
from selenium.webdriver.support import expected_conditions as EC
import schedule

ws = "https://www.imperial.ac.uk/timetabling/calendar/cal?vt=agendaDay&dt=Today&et=student&fid0=02606654"


def icon_from_base64(data: str) -> QIcon:
    byte_data = base64.b64decode(data)
    pixmap = QPixmap()
    pixmap.loadFromData(byte_data)
    return QIcon(pixmap)

b64 = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAFo9M/3AAAACXBIWXMAAA7DAAAOwwHHb6hkAAAAz0lEQVR4nLRTbQ6DIAwF4wlMvKMH8K/xeC6zy3aEJct2CoFREKgdRrZkTZ5ofZTXD4QQF+NhH2hbT3zpurv73TRX7+j7h3O07Y1SyRattVFKJUddM0YwdtzZYiIATvCh0s4PwWCkhJUA+Qh5lBOowIkTZpc4FmBZtFulzBwxji+7nvY1HBDADMOTFYlo4FZV36f5KzYfc5yWPcMpSvKyCiD2FZP2vQ2J0x4fpICTg2X1AXhp/xdgdlcojAUCDccj+PBqpTHJKuA3g6OwBqV4AwAA//8NLAylAAAABklEQVQDAH5LIM/fEiVjAAAAAElFTkSuQmCC"

def ifilogin():
    service = ChromeService(executable_path="C:/chromedriver/chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument(r'--user-data-dir=C:\ChromeUserData')
    driver = webdriver.Chrome(service=service, options=options)
    # 打开一个网站
    driver.get(ws)
    time.sleep(1.3)
    iflogin = driver.find_elements(By.CLASS_NAME, "login-paginated-page")
    if len(iflogin) != 0:
        driver.quit()
        loginpage()
    else:
        driver.quit()

def loginpage():
    service = ChromeService(executable_path="C:/chromedriver/chromedriver.exe")
    options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    options.add_argument(r'--user-data-dir=C:\ChromeUserData')
    driver = webdriver.Chrome(service=service, options=options)
    # 打开一个网站
    driver.get(ws)
    time.sleep(1.3)
    iflogin = driver.find_elements(By.CLASS_NAME, "login-paginated-page")
    print(len(iflogin))
    if len(iflogin) != 0:
        WebDriverWait(driver, 600).until(
        EC.presence_of_element_located((By.CLASS_NAME, "fc-content"))  # 你登录后页面才会出现的元素
        )
    driver.quit()

def gettt():
    ifilogin()
    service = ChromeService(executable_path="C:/chromedriver/chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument(r'--user-data-dir=C:\ChromeUserData')
    driver = webdriver.Chrome(service=service, options=options)
    l = []
    #driver.get("https://www.imperial.ac.uk/timetabling/calendar/cal?vt=agendaDay&dt=2025-05-06&et=student&fid0=02606654")
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
        label = QLabel(gettt(), self)
        label.setFont(QFont('Arial', 10))
        label.setStyleSheet("color: white; background: transparent;")
        label.move(screen.width()/2, 0)
        label.setAlignment(Qt.AlignCenter)

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
