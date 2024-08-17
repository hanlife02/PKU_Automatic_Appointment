import os
import time
import threading
import subprocess
from datetime import datetime
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

year = int(os.getenv('YEAR'))
month = int(os.getenv('MONTH'))
day = int(os.getenv('DAY'))
hour = int(os.getenv('HOUR'))
min = int(os.getenv('MIN'))

# 运行你的 appointment.py 脚本
def run_appointment_script():
    subprocess.run(["python", "appointment.py"])

# 计算到特定日期的剩余秒数
def calculate_seconds_until(target_datetime):
    now = datetime.now()
    delta = target_datetime - now
    return delta.total_seconds()

# 设置目标日期和时间 (年, 月, 日, 时, 分)
target_date = datetime(year, month, day, hour, min)  # 修改为你需要的日期和时间

# 创建一个线程来等待到指定时间并运行脚本
def schedule_task():
    time_until_target = calculate_seconds_until(target_date)
    if time_until_target > 0:
        print(f"Waiting for {time_until_target} seconds until {target_date}")
        time.sleep(time_until_target)
    run_appointment_script()

# 启动线程
thread = threading.Thread(target=schedule_task)
thread.start()
