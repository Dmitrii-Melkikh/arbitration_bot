import time
import os
from pathlib import Path
from datetime import datetime
import random
from arbitr_parser.driver_staff import AccessoryClass
import requests

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium_stealth import stealth


class Processing(AccessoryClass):
    def find_opred(self):
        opred_num = []
        right_name_of_pdf_file = ["Принять к производству", "Принять к рассмотрению", "О принятии к рассмотрен",
                                  "О принятии к производс", "Рассмотреть дело по об", "Привлечь к участию в д"]
        exception_name_of_pdf_file = ["Оставить без движения "]
        name_class = 'js-judges-rollover'
        find_casetype = self.driver.find_elements(By.CLASS_NAME, 'case-type')
        for i in range(len(find_casetype)):
            c_type = find_casetype[i].text
            if c_type == 'Определение':
                opred_num.append(i)
        find_name = self.driver.find_elements(By.CLASS_NAME, name_class)
        for i in opred_num:
            name_of_pdf = find_name[i].text
            for right_name in right_name_of_pdf_file:
                if name_of_pdf.find(right_name):
                    time.sleep(random.randint(3122, 4375) / 1000)
                    self.actionchains(find_name[i])
                    self.switchtowindow(-1)
                    time.sleep(random.randint(4753, 5219) / 1000)
                    url_of_pdf = self.driver.current_url
                    self.driver.close()
                    self.switchtowindow(0)
                    self.driver.window_handles.pop()
                    time.sleep(random.randint(2452, 3362) / 1000)
                    return url_of_pdf
            for exception_name in exception_name_of_pdf_file:
                if not name_of_pdf.find(exception_name):
                    time.sleep(random.randint(3258, 4853) / 1000)
                    return 'wrong name'
        return False

    def update_data(self, other_numbers):
        self.checked_case_numbers = other_numbers
        self.write_to_txt('C:/Users/Дмитрий/Desktop/Арбитр бот/arbitr_parser/TXT_data.txt', self.checked_case_numbers)
        self.write_to_txt('C:/Users/Дмитрий/Desktop/Арбитр бот/arbitr_parser/saved_url.txt', self.potential_urls)
        pass


    def check_url(self, url_to_check):
        response = requests.get(url_to_check)
        time.sleep(5)
        status_code = response.status_code
        if status_code >= 400:
            return False
        return True

    def scrap_checked_case(self):
        path_to_casenumber = '//*[@id="b-case-header"]/ul[1]/li/span'
        right_urls = []
        other_numbers = set()
        self.driver.get('https://kad.arbitr.ru')
        possible_non_exisitent_urls = self.possible_non_exitent_urls
        for url in possible_non_exisitent_urls:
            if not self.check_url(url):
                self.potential_urls.remove(url)
        urls = self.potential_urls
        for url in urls:
            if self.check_url(url):
                self.driver.get(url)
                plus_click = self.plus_click()
                if plus_click:
                    time.sleep(random.randint(2645, 3512) / 1000)
                    opred_url = self.find_opred()
                    casenumber = self.driver.find_element(By.XPATH, path_to_casenumber)
                    if opred_url != False and opred_url != 'wrong':
                        right_urls.append([url, opred_url])
                        self.potential_urls.remove(url)
                    if opred_url != False and opred_url == 'wrong name':
                        self.potential_urls.remove(url)
                    other_numbers.add(casenumber.text)
            else:
                self.possible_non_exitent_urls.add(url)
            time.sleep(random.randint(7461, 8574) / 1000)
        print(right_urls)
        self.update_data(other_numbers)
        return right_urls

# proc = Processing()
# #proc.scrap_checked_case()
# proc.check_url()