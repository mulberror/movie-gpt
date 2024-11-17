from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# 启动 WebDriver（假设你使用 Chrome 浏览器）
driver = webdriver.Chrome()  # 请替换为实际路径

# 打开 ChatGPT 网站
driver.get('https://chatgpt.com/')

# 等待页面加载，可能需要手动登录
time.sleep(5)  # 根据实际情况调整等待时间

# 找到对话框输入框（这是一个 contenteditable="true" 的 div 元素）
input_box = driver.find_element(By.ID, 'prompt-textarea')

# 清空输入框（如果有默认文本）
input_box.clear()

# 向输入框发送“你好”
input_box.send_keys('你好')

# 找到发送按钮并点击
send_button = driver.find_element(By.XPATH, '//button[@aria-label="发送提示"]')
send_button.click()

# 等待一段时间以便获取回复（视网站响应时间而定）
time.sleep(50)

# 获取回复结果，假设聊天回复出现在特定的 div 元素中
response = driver.find_element(By.CSS_SELECTOR, '.message-in').text  # 你可以根据实际情况调整 CSS 选择器

print('ChatGPT 的回复:', response)

# 关闭浏览器
driver.quit()
