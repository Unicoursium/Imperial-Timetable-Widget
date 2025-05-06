from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
import time
from selenium.webdriver.common.by import By

# 设置正确的驱动路径
service = ChromeService(executable_path="C:/chromedriver/chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument(r'--user-data-dir=C:\ChromeUserData')
driver = webdriver.Chrome(service=service, options=options)
l = []
# 打开一个网站
driver.get("https://www.imperial.ac.uk/timetabling/calendar/cal?vt=agendaDay&dt=Today&et=student&fid0=02606654")
time.sleep(1.3)
elements = driver.find_elements(By.CLASS_NAME, "fc-content")

for element in elements:
    e = element.text.split("\n")
    l.append(e[0]+'\n'+e[1]+'\n'+e[4])
    #print(element.text)
for i in l:
    print(i)
# 关闭浏览器
driver.quit()
