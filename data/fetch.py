from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from datetime import datetime


class DataFetch(object):
    def __init__(self):
        self.driver = webdriver.Chrome()

    def get_link(self, name):
        search_url = f'https://www.douban.com/search?q={name}'
        self.driver.get(search_url)
        time.sleep(1)  # 等待页面加载
        try:
            link_element = self.driver.find_element(By.CLASS_NAME, 'DouWeb-SR-person-card-name')
            link = link_element.get_attribute('href')
            return link
        except Exception as e:
            print(f'Error occurred for {name}: {e}')
            return None

    def click_expand(self):
        try:
            expand_button = self.driver.find_elements(By.CLASS_NAME, 'fold-switch')
            if expand_button:
                expand_button[0].click()  # 点击第一个匹配的“展开”按钮
                time.sleep(1)  # 等待页面刷新或内容展开
        except Exception as e:
            print(f"Error occurred when clicking the expand button: {e}")

    def get_summary(self):
        try:
            # 点击展开按钮
            self.click_expand()

            # 提取 summary
            summary_element = self.driver.find_element(By.CLASS_NAME, 'content')
            summary = summary_element.text
            return summary
        except Exception as e:
            print(f"Error occurred when extracting summary: {e}")
            return None

    def get_info(self, name):
        # print(url)
        url = self.get_link(name)
        self.driver.get(url)
        time.sleep(1)
        try:
            sex_elements = self.driver.find_elements(By.XPATH,
                                                     '//li[span[contains(text(),"性别")]]/span[@class="value"]')
            sex = sex_elements[0].text if sex_elements else ""  # 返回空字符串

            # 提取出生日期
            birthday_elements = self.driver.find_elements(By.XPATH,
                                                          '//li[span[contains(text(),"出生日期")]]/span[@class="value"]')
            birthday = birthday_elements[0].text if birthday_elements else ""  # 返回空字符串

            # 提取出生地
            birthplace_elements = self.driver.find_elements(By.XPATH,
                                                            '//li[span[contains(text(),"出生地")]]/span[@class="value"]')
            birthplace = birthplace_elements[0].text if birthplace_elements else ""  # 返回空字符串

            summary = self.get_summary()
            return {
                'sex': sex,
                'birthday': datetime.strptime(birthday, '%Y年%m月%d日').strftime('%Y-%m-%d') if birthday else "",
                'birthplace': birthplace,
                'summary': summary
            }
        except Exception as e:
            print(f'Error occurred for {name}: {e}')
            return None
