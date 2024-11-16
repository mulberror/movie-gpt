from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import re
import random

LOADTIME = 0.8


def loadtime():
    global LOADTIME
    return (random.random() + 0.5) * LOADTIME


def trans_date(birthday):
    if birthday:
        try:
            new_time = datetime.strptime(birthday, '%Y年%m月%d日').strftime('%Y-%m-%d')
            return new_time
        except ValueError:
            return birthday
    else:
        return ""


class DataFetch(object):

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.not_found_this_person = True

    def get_link0(self, name):
        search_url = f'https://www.douban.com/search?q={name}'
        self.driver.get(search_url)
        time.sleep(loadtime())  # 等待页面加载
        try:
            link_element = self.driver.find_element(By.CLASS_NAME, 'DouWeb-SR-person-card-name')
            link = link_element.get_attribute('href')
            self.not_found_this_person = False
            return link
        except Exception as e:
            print(f'Error occurred for {name}: {e}')
            return None

    def get_link1(self, name):
        search_url = f"https://www.douban.com/search?cat=1065&q={name}"
        self.driver.get(search_url)
        time.sleep(loadtime())  # 等待页面加载
        try:
            content_div = self.driver.find_element(By.CLASS_NAME, 'content')
            element = content_div.find_element(By.CSS_SELECTOR, '.title a')
            url = element.get_attribute('href')
            self.not_found_this_person = False
            # print(url)
            return url
        except Exception as e:
            return ""
            # print(f'Error occurred for {name}: {e}')

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

    def get_info_from_url(self, name, url):
        self.driver.get(url)
        time.sleep(loadtime())
        try:
            current_url = self.driver.current_url
            match = re.search(r'/personage/(\d+)/', current_url)
            pid = ""
            if match:
                pid = match.group(1)

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

            data = {
                'pid': pid,
                'sex': sex,
                'birthday': trans_date(birthday),
                'birthplace': birthplace,
                'summary': summary
            }

            # print(data)

            return data

        except Exception as e:
            print(f'Error occurred for {name}: {e}')
            return None

    def get_inner_info(self, name):
        try:
            url = self.get_link1(name)
            info = self.get_info_from_url(name, url)
            return info
        except Exception as e:
            try:
                url = self.get_link0(name)
                info = self.get_info_from_url(name, url)
                return info
            except Exception as e:
                return None


    def get_info(self, name):
        for _ in range(3):
            self.not_found_this_person = True
            result = self.get_inner_info(name)
            if result is None:
                self.driver.quit()
                time.sleep(10)
                self.driver = webdriver.Chrome()
            else:
                return result

        return None

# fetch = DataFetch()
# print(fetch.get_info('袁祥仁 Cheung-Yan Yuen'))
