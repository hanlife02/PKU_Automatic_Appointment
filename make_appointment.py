from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
import os
import time
import pyotp

# 加载.env文件中的环境变量
load_dotenv()

# 从环境变量中获取用户名、密码、EdgeDriver路径和日期文本
username_str = os.getenv('MY_USERNAME')
password_str = os.getenv('PASSWORD')
edgedriver_path = os.getenv('EDGEDRIVER_PATH')

date_text = os.getenv('MY_DATE_TEXT')
door_text = os.getenv('MY_DOOR_TEXT')
time_text = os.getenv('MY_TIME_TEXT')
name_text = os.getenv('MY_NAME')
id_number_text = os.getenv('MY_ID_NUMBER')
phone_text = os.getenv('MY_PHONE')
purpose_text = os.getenv('MY_PURPOSE')
secret = os.getenv('SECRET')

def make_appointment(driver,date_text,door_text,time_text,name_text,id_number_text,phone_text,purpose_text,secret,close_driver) :
    # 打开登录页面
    login_url = 'https://iaaa.pku.edu.cn/iaaa/oauth.jsp?appID=portal2017&appName=%E5%8C%97%E4%BA%AC%E5%A4%A7%E5%AD%A6%E6%A0%A1%E5%86%85%E4%BF%A1%E6%81%AF%E9%97%A8%E6%88%B7%E6%96%B0%E7%89%88&redirectUrl=https%3A%2F%2Fportal.pku.edu.cn%2Fportal2017%2FssoLogin.do'
    driver.get(login_url)

    # 等待页面加载完成
    WebDriverWait(driver, 30).until(lambda d: d.execute_script("return document.readyState") == "complete")

    # 等待用户名输入框出现
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'user_name')))

    # 输入用户名
    username = driver.find_element(By.ID, 'user_name')
    username.send_keys(username_str)

    # 输入密码
    password = driver.find_element(By.ID, 'password')
    password.send_keys(password_str)

    # 提交表单
    password.send_keys(Keys.RETURN)

    # 等待页面跳转并加载完成
    WebDriverWait(driver, 30).until(lambda d: d.execute_script("return document.readyState") == "complete")

    time.sleep(1)

    # 获取页面的宽度和高度
    page_width = driver.execute_script("return document.body.scrollWidth")
    page_height = driver.execute_script("return document.body.scrollHeight")

    # 计算页面正中心偏上的位置（高度为页面中心的30%处）
    center_x = page_width // 2
    center_y = page_height * 0.1

    # 使用ActionChains在该位置点击
    actions = ActionChains(driver)
    actions.move_by_offset(center_x, center_y).click().perform()

    time.sleep(1)

    # 查找并点击文本为“学生预约访客”的链接或按钮
    appointment_link = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '学生预约访客')]")))
    appointment_link.click()

    # 获取当前所有窗口句柄
    windows = driver.window_handles

    # 切换到新窗口（假设新窗口是最后一个打开的）
    driver.switch_to.window(windows[-1])

    # 等待新窗口的页面加载完成
    WebDriverWait(driver, 30).until(lambda d: d.execute_script("return document.readyState") == "complete")

    # 使用CSS选择器查找“预约”按钮并点击
    try:
        button_css_selector = "body > div > section > div > div > div.el-col.el-col-24.el-col-xs-24.el-col-sm-24.el-col-md-24.el-col-lg-24 > main > div.el-card.box-card.varia-main-card.is-never-shadow > div.el-card__header > div > div > button"
        appointment_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, button_css_selector)))
        
        # 滚动页面以确保按钮可见
        driver.execute_script("arguments[0].scrollIntoView();", appointment_button)
        
        # 点击按钮
        driver.execute_script("arguments[0].click();", appointment_button)
        print("Button clicked using JavaScript.")
    except Exception as e:
        print(f"Error locating or clicking button: {e}")

    # 等待须知页面加载完成
    WebDriverWait(driver, 30).until(lambda d: d.execute_script("return document.readyState") == "complete")

    # 勾选复选框
    try:
        checkbox_css_selector = "body > div > section > div > div > div.el-col.el-col-24.el-col-xs-24.el-col-sm-24.el-col-md-24.el-col-lg-24 > main > div.el-card.box-card.is-never-shadow > div.el-card__body > div > div:nth-child(10) > label"
        checkbox = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, checkbox_css_selector)))
        checkbox.click()
        print("Checkbox selected.")
    except Exception as e:
        print(f"Error selecting checkbox: {e}")

    # 点击“开始预约”按钮
    try:
        start_button_css_selector = "body > div > section > div > div > div.el-col.el-col-24.el-col-xs-24.el-col-sm-24.el-col-md-24.el-col-lg-24 > main > div.el-card.box-card.is-never-shadow > div.el-card__body > div > div:nth-child(11) > button.el-button.el-button--primary.el-button--small"
        start_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, start_button_css_selector)))
        start_button.click()
        print("Clicked '开始预约' button.")
    except Exception as e:
        print(f"Error clicking '开始预约' button: {e}")

    # 等待进入预约页面
    WebDriverWait(driver, 30).until(lambda d: d.execute_script("return document.readyState") == "complete")

    # 点击日期选择器图标
    try:
        date_picker_icon = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.app-wrapper > section > div > div > div.el-col.el-col-24.el-col-xs-24.el-col-sm-24.el-col-md-24.el-col-lg-24 > main > div.el-card.box-card.is-never-shadow > div.el-card__body > form > div:nth-child(6) > div:nth-child(1) > div > div > div > div > span > span > i")))
        date_picker_icon.click()
        print("Date picker icon clicked.")
    except Exception as e:
        print(f"Error clicking date picker icon: {e}")

    time.sleep(0.6) 

    # 等待日期选择器展开并选择日期
    try:
        # 使用从环境变量读取的日期文本
        date_option = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{date_text}')]")))
        date_option.click()
        print("Date selected.")
    except Exception as e:
        print(f"Error selecting date: {e}")

    time.sleep(0.6) 

    # 点击预约的门下拉菜单，确保展开选项
    try:
        door_dropdown_css_selector = "body > div.app-wrapper > section > div > div > div.el-col.el-col-24.el-col-xs-24.el-col-sm-24.el-col-md-24.el-col-lg-24 > main > div.el-card.box-card.is-never-shadow > div.el-card__body > form > div:nth-child(6) > div:nth-child(3) > div > div > div > div > span > span > i"
        door_dropdown = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, door_dropdown_css_selector)))
        door_dropdown.click()
        print("Door dropdown clicked.")
    except Exception as e:
        print(f"Error clicking door dropdown: {e}")

    time.sleep(0.6) 

    # 选择特定的门
    try:
        door_option = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{door_text}')]")))
        door_option.click()
        print(f"Selected the door: {door_text}")
    except Exception as e:
        print(f"Error selecting the door: {e}")

    time.sleep(0.6) 

    # 点击时间选择器图标以展开选项
    try:
        time_picker_icon_css_selector = "body > div.app-wrapper > section > div > div > div.el-col.el-col-24.el-col-xs-24.el-col-sm-24.el-col-md-24.el-col-lg-24 > main > div.el-card.box-card.is-never-shadow > div.el-card__body > form > div:nth-child(6) > div:nth-child(2) > div > div > div.el-date-editor.el-input.el-input--prefix.el-input--suffix.el-date-editor--time-select > span.el-input__prefix > i"
        time_picker_icon = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, time_picker_icon_css_selector)))
        time_picker_icon.click()
        print("Time picker icon clicked.")
    except Exception as e:
        print(f"Error clicking time picker icon: {e}")

    time.sleep(0.6) 

    # 逐步滚动并选择具体的时间选项
    try:
        time_picker_panel_css_selector = "body > div.el-picker-panel.time-select.el-popper > div.el-scrollbar > div.el-picker-panel__content.el-scrollbar__wrap"
        time_picker_panel = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, time_picker_panel_css_selector)))
        
        # 尝试向下滚动并查找目标时间选项
        for _ in range(10):  # 尝试10次
            try:
                time_option_xpath = f"//div[contains(@class, 'time-select-item') and text()='{time_text}']"
                time_option = driver.find_element(By.XPATH, time_option_xpath)
                time_option.click()
                print(f"Selected the time: {time_text}")
                break
            except:
                # 如果未找到，向下滚动
                driver.execute_script("arguments[0].scrollTop += 100;", time_picker_panel)
                time.sleep(0.5)  # 等待0.5秒以确保滚动完成

        # 如果向下滚动未找到，尝试向上滚动
        for _ in range(10):  # 尝试10次
            try:
                time_option_xpath = f"//div[contains(@class, 'time-select-item') and text()='{time_text}']"
                time_option = driver.find_element(By.XPATH, time_option_xpath)
                time_option.click()
                print(f"Selected the time: {time_text}")
                break
            except:
                # 如果未找到，向上滚动
                driver.execute_script("arguments[0].scrollTop -= 100;", time_picker_panel)
                time.sleep(0.5)  # 等待0.5秒以确保滚动完成
    except Exception as e:
        print(f"Error selecting the time: {e}")

    time.sleep(0.3) 

    # 输入人的姓名
    try:
        name_input = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.app-wrapper > section > div > div > div.el-col.el-col-24.el-col-xs-24.el-col-sm-24.el-col-md-24.el-col-lg-24 > main > div.el-card.box-card.is-never-shadow > div.el-card__body > form > div:nth-child(6) > div:nth-child(4) > div > div > div.el-input > input"))
        )
        name_input.send_keys(name_text)
        print(f"Entered name: {name_text}")
    except Exception as e:
        print(f"Error entering name: {e}")

    time.sleep(0.3)

    # 输入证件号
    try:
        id_number_input = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.app-wrapper > section > div > div > div.el-col.el-col-24.el-col-xs-24.el-col-sm-24.el-col-md-24.el-col-lg-24 > main > div.el-card.box-card.is-never-shadow > div.el-card__body > form > div:nth-child(6) > div:nth-child(5) > div > div > div > input"))
        )
        id_number_input.send_keys(id_number_text)
        print(f"Entered ID number: {id_number_text}")
    except Exception as e:
        print(f"Error entering ID number: {e}")

    time.sleep(0.3)

    # 输入电话号码
    try:
        phone_input = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.app-wrapper > section > div > div > div.el-col.el-col-24.el-col-xs-24.el-col-sm-24.el-col-md-24.el-col-lg-24 > main > div.el-card.box-card.is-never-shadow > div.el-card__body > form > div:nth-child(6) > div:nth-child(6) > div > div > div > input"))
        )
        phone_input.send_keys(phone_text)
        print(f"Entered phone number: {phone_text}")
    except Exception as e:
        print(f"Error entering phone number: {e}")

    time.sleep(0.3)

    # 输入预约事由
    try:
        purpose_input = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.app-wrapper > section > div > div > div.el-col.el-col-24.el-col-xs-24.el-col-sm-24.el-col-md-24.el-col-lg-24 > main > div.el-card.box-card.is-never-shadow > div.el-card__body > form > div:nth-child(6) > div:nth-child(7) > div > div > div.el-textarea > textarea"))
        )
        purpose_input.send_keys(purpose_text)
        print(f"Entered purpose: {purpose_text}")
    except Exception as e:
        print(f"Error entering purpose: {e}")

    time.sleep(0.3)

    # 点击联系人
    try:
        button_selector = "body > div > section > div > div > div.el-col.el-col-24.el-col-xs-24.el-col-sm-24.el-col-md-24.el-col-lg-24 > main > div.el-card.box-card.is-never-shadow > div.el-card__body > form > div:nth-child(2) > div.el-col.el-col-24.el-col-xs-24.el-col-sm-24.el-col-md-24 > div > div > button"
        target_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector)))
        
        # 滚动页面以确保按钮可见
        driver.execute_script("arguments[0].scrollIntoView();", target_button)
        
        target_button.click()
        print("Clicked the button successfully.")
    except Exception as e:
        print(f"Error clicking the button: {e}")

    time.sleep(0.5)

    # 点击联系人
    try:
        contact_item_selector = "body > div > section > div > div > div.el-col.el-col-24.el-col-xs-24.el-col-sm-24.el-col-md-24.el-col-lg-24 > main > div > div.el-card__body > div > div > div.contactItem"
        contact_item = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, contact_item_selector)))
        
        # 滚动页面以确保元素可见
        driver.execute_script("arguments[0].scrollIntoView();", contact_item)
        
        contact_item.click()
        print("Clicked the contact item successfully.")
    except Exception as e:
        print(f"Error clicking the contact item: {e}")

    time.sleep(0.5)

    # 点击保存
    try:
        button_selector = "body > div.app-wrapper > section > div > div > div.el-col.el-col-24.el-col-xs-24.el-col-sm-24.el-col-md-24.el-col-lg-24 > main > div.el-card.box-card.is-never-shadow > div.el-card__body > form > div:nth-child(6) > div:nth-child(8) > div > div > button:nth-child(1)"
        button_element = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector)))
        
        # 滚动页面以确保元素可见
        driver.execute_script("arguments[0].scrollIntoView();", button_element)
        
        button_element.click()
        print("Clicked the button successfully.")
    except Exception as e:
        print(f"Error clicking the button: {e}")

    time.sleep(1)

    # 点击申请
    try:
        alert_button_selector = "body > div.el-message-box__wrapper > div > div.el-message-box__btns > button.el-button.el-button--default.el-button--small.el-button--primary"
        alert_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, alert_button_selector)))
        
        alert_button.click()
        print("Clicked the alert confirmation button.")
    except Exception as e:
        print(f"Error clicking the alert confirmation button: {e}")

    # 生成 TOTP 对象
    totp = pyotp.TOTP(secret)

    # 获取当前的 TOTP 令牌
    token = totp.now()

    time.sleep(0.3)

    # 尝试点击指定元素并输入 token
    try:
        input_field_selector = "body > div.app-wrapper > section > div > div > div.el-col.el-col-24.el-col-xs-24.el-col-sm-24.el-col-md-24.el-col-lg-24 > main > div:nth-child(3) > div > div.el-dialog__body > div.el-input.el-input--suffix > input"
        input_field = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, input_field_selector)))
        
        # 点击输入框
        input_field.click()
        print("Input field clicked successfully.")
        
        # 输入 token 变量的值
        input_field.send_keys(token)
        print("Token entered successfully.")
    except Exception as e:
        print(f"Error interacting with the input field: {e}")

    time.sleep(0.3)

    # 点击提交
    try:
        button_selector = "body > div.app-wrapper > section > div > div > div.el-col.el-col-24.el-col-xs-24.el-col-sm-24.el-col-md-24.el-col-lg-24 > main > div:nth-child(3) > div > div.el-dialog__footer > span > button.el-button.el-button--primary"
        button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector)))
        
        # 点击按钮
        button.click()
        print("Button clicked successfully.")
    except Exception as e:
        print(f"Error clicking the button: {e}")

    time.sleep(0.3)

    # 点击确定
    try:
        button_selector = "body > div.el-message-box__wrapper > div > div.el-message-box__btns > button.el-button.el-button--default.el-button--small.el-button--primary"
        button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector)))
        
        # 点击按钮
        button.click()
        print("预约成功.")
    except Exception as e:
        print(f"预约失败: {e}")
    
    time.sleep(1)
    
    if close_driver == True:
        driver.quit()
    
    else :
        time.sleep(300)
        driver.quit()

