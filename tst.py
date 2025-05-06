from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction
import sys

app = QApplication([])

tray = QSystemTrayIcon(QIcon("your_icon.png"))  # 改成你本地的图标文件路径
tray.setVisible(True)

menu = QMenu()
quit_action = QAction("退出程序")
quit_action.triggered.connect(app.quit)
menu.addAction(quit_action)

tray.setContextMenu(menu)

app.exec()
