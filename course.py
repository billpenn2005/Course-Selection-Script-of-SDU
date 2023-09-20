'''
使用方法：
程序需使用三个文件:pwd.txt(用于登录),config.txt(计时器配置),course.txt(选课设置)

pwd.txt:
第一行:用户名
第二行:密码

config.txt:
第一行:小时
第二行:分钟

course_select.txt:
    标记(四个,后面必须加冒号):
        BX:                 必选
        XX:                 限选
        RX:                 任选
        QT:                 其他
    每个标记下面填写若干课程,格式为课程编号加空格加任课教师(也可选择不填任课教师)
    示例:
    BX:
    sd30210010
    sd02810460 陈家付
    XX:
    RX:
    QT:

'''
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.remote_connection import LOGGER
import re
import os
import time

url0="https://pass.sdu.edu.cn/cas/login"
url1="http://bkzhjx.wh.sdu.edu.cn/sso.jsp"

config_file=open("./config.txt")
alarm_hour=config_file.readline()
alarm_minute=config_file.readline()
config_file.close()

while ((int(time.localtime().tm_hour)<=int(alarm_hour))and(int(time.localtime().tm_min)<int(alarm_minute))):
    os.system('cls')
    print("\033[93m[.]Waiting "+time.strftime('%Y-%m-%d %H:%M:%S')+"\033[0m")

print("\033[92m[+]Timing completed!\033[0m")

chrome_options=Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('log-level=3')
driver=webdriver.Chrome(options=chrome_options)
driver.get(url0)

username=""
password=""

alarm_hour=int(0)
alarm_minute=int(0)

pwd_file=open("./pwd.txt")
username=pwd_file.readline()
password=pwd_file.readline()
pwd_file.close()

action=ActionChains(driver)

name_input=driver.find_element("id","un")
password_input=driver.find_element("id","pd")
login_button=driver.find_element("id","index_login_btn")

name_input.send_keys(username)
password_input.send_keys(password)
login_button.click()
print("\033[92m[+]Login successfully!\033[0m")

time.sleep(1)

driver.get(url1)

choose_button=driver.find_element(By.LINK_TEXT,"进入选课")
choose_button.click()

choose_button2=driver.find_element(By.XPATH,"/html/body/div/div[2]/div/table/tbody/tr/td[4]/span")
choose_button2.click()
print("\033[92m[+]Successfully entered the course selection page!\033[0m")
time.sleep(2)

course_select_file=open("./course_select.txt",encoding="utf-8")
courses=course_select_file.readlines()
driver.switch_to.frame(driver.find_elements(By.TAG_NAME,"iframe")[2])
class_num=0
success_num=0
for course in courses:
    if(course[:-1]=="BX:" or course=="BX:"):
        print("Compulsory courses:")
        driver.find_element(By.XPATH,"/html/body/div[2]/div/ul/li[2]").click()
    elif(course[:-1]=="XX:" or course=="XX:"):
        print("Limit courses:")
        driver.find_element(By.XPATH,"/html/body/div[2]/div/ul/li[3]").click()
    elif(course[:-1]=="RX:" or course=="RX:"):
        print("Optional courses:")
        driver.find_element(By.XPATH,"/html/body/div[2]/div/ul/li[4]").click()
    elif(course[:-1]=="QT:" or course=="QT:"):
        print("Other courses:")
        driver.find_element(By.XPATH,"/html/body/div[2]/div/ul/li[5]").click()
    else:
        class_num+=1
        course_id=course.split()[0]
        teacher=""
        if(len(course.split())>1):
            teacher=course.split()[1]
        print(course_id+" "+teacher)
        driver.switch_to.frame(driver.find_elements(By.TAG_NAME,"iframe")[0])
        driver.find_element(By.XPATH,'//*[@id="kcxx"]').clear()
        driver.find_element(By.XPATH,'//*[@id="skls"]').clear()
        driver.find_element(By.XPATH,'//*[@id="kcxx"]').send_keys(course_id)
        driver.find_element(By.XPATH,'//*[@id="skls"]').send_keys(teacher)
        driver.find_element(By.XPATH,"/html/body/div/div[9]/div[2]/span[1]").click()
        time.sleep(1)
        driver.find_element(By.LINK_TEXT,'选课').click()
        alt_txt=driver.switch_to.alert.text
        if(re.search("成功",alt_txt)):
            print("\033[92m[+]"+alt_txt+"\033[0m")
            success_num+=1
        else:
            print("\033[91m[-]"+alt_txt+"\033[0m")
        driver.switch_to.alert.accept()
        driver.switch_to.parent_frame()
driver.find_element(By.XPATH,"/html/body/div[2]/div/div[1]/span[3]").click()
print("\033[93m[.]Exiting...\033[0m")
driver.close()
print("\033[92m[+]Course selection completed, success rate: "+str(success_num)+"/"+str(class_num)+"\033[0m")
os.system("pause")