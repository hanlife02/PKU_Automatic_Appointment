import schedule
import time
import subprocess
from datetime import datetime
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

year = os.getenv('YEAR')
month = os.getenv('MONTH')
day = os.getenv('DAY')
hour = os.getenv('HOUR')
min = os.getenv('MIN')


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

# 等待直到目标时间
time_until_target = calculate_seconds_until(target_date)
if time_until_target > 0:
    print(f"Waiting for {time_until_target} seconds until {target_date}")
    time.sleep(time_until_target)

# 在指定日期和时间运行脚本
run_appointment_script()
