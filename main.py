'''
Author        : Ethan
Contact       : han@hanlife02.com.cn
Date          : 2024-08-30 19:22:26
LastEditTime  : 2024-08-30 19:22:58
LastEditors   : Ethan
Description   : This is a script for automatic appointments for Peking University students
'''

import os
import time
import threading
from datetime import datetime
from dotenv import load_dotenv
from make_appointment import make_appointment
from selenium import webdriver
from selenium.webdriver.edge.service import Service

# 加载.env文件中的环境变量
load_dotenv()

year = int(os.getenv('YEAR'))
month = int(os.getenv('MONTH'))
day = int(os.getenv('DAY'))
hour = int(os.getenv('HOUR'))
min = int(os.getenv('MIN'))

username_str = os.getenv('MY_USERNAME')
password_str = os.getenv('PASSWORD')
edgedriver_path = os.getenv('EDGEDRIVER_PATH')
number = int(os.getenv('NUMBER'))  # 确保转换为整数

date_first = os.getenv('First_DATE_TEXT')
door_first = os.getenv('First_DOOR_TEXT')
time_first = os.getenv('First_TIME_TEXT')
name_first = os.getenv('First_NAME')
id_number_first = os.getenv('First_ID_NUMBER')
phone_first = os.getenv('First_PHONE')
purpose_first = os.getenv('First_PURPOSE')

date_second = os.getenv('Second_DATE_TEXT')
door_second = os.getenv('Second_DOOR_TEXT')
time_second = os.getenv('Second_TIME_TEXT')
name_second = os.getenv('Second_NAME')
id_number_second = os.getenv('Second_ID_NUMBER')
phone_second = os.getenv('Second_PHONE')
purpose_second = os.getenv('Second_PURPOSE')

secret = os.getenv('SECRET')

# 配置EdgeDriver路径
service = Service(edgedriver_path)

# 计算到特定日期的剩余秒数
def calculate_seconds_until(target_datetime):
    now = datetime.now()
    delta = target_datetime - now
    return delta.total_seconds()

# 设置目标日期和时间 (年, 月, 日, 时, 分)
target_date = datetime(year, month, day, hour, min)

# 创建一个线程来等待到指定时间并运行脚本
def schedule_task():
    time_until_target = calculate_seconds_until(target_date)
    interval = 10  # 每十秒输出一次

    while time_until_target > 0:
        if time_until_target > interval:
            print(f"Waiting for {time_until_target:.2f} seconds until {target_date}")
            time.sleep(interval)
            time_until_target -= interval
        else:
            print(f"Waiting for {time_until_target:.2f} seconds until {target_date}")
            time.sleep(time_until_target)
            time_until_target = 0
            
    # 添加等待时间，让页面有时间刷新为第二天的内容
    print("Waiting for page refresh...")
    time.sleep(5)  # 等待5秒让页面刷新
    
    # 第一次预约，关闭浏览器
    driver = webdriver.Edge(service=service)
    make_appointment(driver, date_first, door_first, time_first, name_first, id_number_first, phone_first, purpose_first, secret, close_driver=True)

    # 如果有第二次预约，重新启动浏览器，并预约
    if number == 2:
        # 重启浏览器
        driver = webdriver.Edge(service=service)
        time.sleep(0.3)
        make_appointment(driver, date_second, door_second, time_second, name_second, id_number_second, phone_second, purpose_second, secret, close_driver=True)

    # 结束后等待五分钟再关闭浏览器
    time.sleep(300)
    driver.quit()

# 启动线程
thread = threading.Thread(target=schedule_task)
thread.start()
