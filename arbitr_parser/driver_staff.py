import time
import random
import os
from pathlib import Path
from datetime import datetime

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium_stealth import stealth

import arbitr_parser.driver_path as driver_path

class AccessoryClass:
    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")
        # chrome_options.add_argument("--js-flags=--noexpose_wasm")
        self.case_numbers = set()
        self.checked_case_numbers = self.read_file('C:/Users/Дмитрий/Desktop/Арбитр бот/arbitr_parser/TXT_data.txt')
        self.potential_urls = self.read_file('C:/Users/Дмитрий/Desktop/Арбитр бот/arbitr_parser/saved_url.txt')
        self.possible_non_exitent_urls = self.read_file('C:/Users/Дмитрий/Desktop/Арбитр бот/arbitr_parser/possible_non_existent_url.txt')
        path_to_driver = Path(driver_path.path).resolve()
        s = Service(str(path_to_driver))
        self.driver = webdriver.Chrome(service=s, options=chrome_options)
        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

    def read_file(self, name_of_file):
        file = open(name_of_file, 'r')
        str_to_read = file.read()
        file.close()
        if len(str_to_read) != 0:
            result = eval(str_to_read)
        else:
            result = set()
        return result

    def actionchains(self, element: object) -> object:
        action = ActionChains(self.driver)
        return action.move_to_element(element).click(element).perform()

    def switchtowindow(self, i):
        window_after = self.driver.window_handles[i]
        self.driver.switch_to.window(window_after)

    def checkexistsbypath(self, path):
        try:
            self.driver.find_element(By.XPATH, path)
        except selenium.common.exceptions.NoSuchElementException:
            return False
        return True

    def checkexistsbyclassname(self, class_name):
        try:
            self.driver.find_elements(By.CLASS_NAME, class_name)
        except selenium.common.exceptions.NoSuchElementException:
            return False
        return True

    def check_casenumber(self, casename):
        casenumber = self.case_numbers
        for el in casenumber:
            if el == casename:
                return True
        return False

    def check_casenumber_on_cur_page(self):
        path_to_casenumber = '//*[@id="b-case-header"]/ul[1]/li/span'
        casenumber = self.driver.find_element(By.XPATH, path_to_casenumber)
        self.checked_case_numbers.add(casenumber.text)

    def check_is_float(self, str):
        try:
            float(str)
            return True
        except ValueError:
            return False

    def plus_click(self):
        time.sleep(random.randint(7547, 9483) / 1000)
        plus_bottom_list = self.driver.find_elements(By.CLASS_NAME, 'b-collapse.js-collapse')
        left_col_class = 'l-col'
        left_col_list = self.driver.find_elements(By.CLASS_NAME, left_col_class)
        left_col_list_text = [left_col_list[i].text for i in range(len(left_col_list))]
        left_col_right_name = 'Первая инстанция'
        if self.checkexistsbyclassname('b-collapse.js-collapse') and left_col_right_name in left_col_list_text:
            plus_bottom = plus_bottom_list[0]
            self.actionchains(plus_bottom)
            return True
        if self.checkexistsbyclassname('b-collapse.js-collapse') == False or len(plus_bottom_list) == 0:
            print('error plus')
            return 'error'
        time.sleep(random.randint(2567, 3432) / 1000)
        return False

    def check_price(self):
        price_class = 'additional-info'
        if self.checkexistsbyclassname(price_class):
            price_list = self.driver.find_elements(By.CLASS_NAME, price_class)
            for price in price_list:
                price_output = price.text
                price_output_with_point = ''.join([ch if ch != ',' else '.' for ch in price_output])
                time.sleep(random.randint(2253, 3162) / 1000)
                price = price_output_with_point[27:]
                if len(price_output_with_point) > 0 and self.check_is_float(price):
                    if float(price) >= float(1000000):
                        return self.driver.current_url
            return False
        print('error price')
        return 'error pr'

    def write_to_txt(self, name_of_file, type_of_write):
        file = open(name_of_file, 'w')
        str_to_write = str(type_of_write)
        file.write(str_to_write)
        file.close()
        pass

    def page_click(self, i):
        page_link = self.driver.find_element(By.XPATH, '//*[@id="pages"]/li[' + str(i + 1) + ']/a')
        self.actionchains(page_link)
        pass