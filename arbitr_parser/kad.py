import time
import os
from pathlib import Path
from datetime import datetime
import random
from arbitr_parser.driver_staff import AccessoryClass

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium_stealth import stealth


class DriverScrapping(AccessoryClass):
    def signin(self):
        self.driver.get('https://kad.arbitr.ru')
        time.sleep((random.randint(1017, 1988)) / 1000)
        # decision_bank = self.driver.find_element(By.XPATH, '//*[@id="b-header"]/tbody/tr/td[2]/div/table/tbody/tr/td[3]/a')
        # self.actionchains(decision_bank)
        check_work = self.checkexistsbypath('//*[@id="js"]/div[13]/div[2]/div/div/div/div')
        if check_work:
            closecheckwork = self.driver.find_element(By.XPATH, '//*[@id="js"]/div[13]/div[2]/div/div/div/div/a[1]')
            self.actionchains(closecheckwork)
        search_button = self.driver.find_element(By.XPATH, '//*[@id="b-form-submit"]/div/button')
        field_court = self.driver.find_element(By.XPATH, '//*[@id="caseCourt"]/div/span/label/input')
        field_court.send_keys('АС Оренбургской области')
        time.sleep((random.randint(7009, 7976)) / 1000)
        self.actionchains(search_button)
        time.sleep(random.randint(944, 1026) / 1000)

    def main_page_scrapping(self):
        list_of_cases = []
        time.sleep(random.randint(4967, 5322) / 1000)
        find_cases = self.driver.find_elements(By.CLASS_NAME, 'num_case')
        for case in find_cases:
            case_no = case.text
            if not self.check_casenumber(case_no):
                self.case_numbers.add(case_no)
                list_of_cases.append(case)
        return list_of_cases

    def new_case_scrapping(self):
        time.sleep(random.randint(3346, 4576) / 1000)
        self.switchtowindow(-1)
        plus = self.plus_click()
        if plus == 'error':
            return 'error'
        time.sleep(random.randint(3573, 4625) / 1000)
        url = self.check_price()
        #if url == 'error':
        #    return 'error'
        if url != 'error pr':
            self.check_casenumber_on_cur_page()
            return url
        else:
            return False

    def scrap(self):
        try:
            self.signin()
            errors_counter = 0
            cur_page_num = 1
            case_type_paths = ['//*[@id="filter-cases"]/li[2]', '//*[@id="filter-cases"]/li[3]']
            # case_type_paths = ['//*[@id="filter-cases"]/li[2]']
            for path in case_type_paths:
                time.sleep(random.randint(3846, 5523) / 1000)
                case_type = self.driver.find_element(By.XPATH, path)
                self.actionchains(case_type)
                list_of_cases = [' ', ' ']
                while True:
                    list_of_cases = self.main_page_scrapping()
                    time.sleep(random.randint(4562, 5343) / 1000)
                    unchecked_casenumbres = self.case_numbers - self.checked_case_numbers
                    for case in list_of_cases:
                        case_no = case.text
                        if case_no in unchecked_casenumbres:
                            self.actionchains(case)
                            new_case = self.new_case_scrapping()
                            if new_case == 'error':
                                errors_counter += 1
                            elif new_case != False:
                                self.potential_urls.add(new_case)
                            self.driver.close()
                            self.switchtowindow(0)
                            self.driver.window_handles.pop()
                            if errors_counter >= 3:
                                self.write_to_txt('C:/Users/Дмитрий/Desktop/Арбитр бот/arbitr_parser/TXT_data.txt', self.checked_case_numbers)
                                self.write_to_txt('C:/Users/Дмитрий/Desktop/Арбитр бот/arbitr_parser/saved_url.txt', self.potential_urls)
                                break
                            time.sleep(random.randint(2786, 3253) / 1000)
                    self.write_to_txt('C:/Users/Дмитрий/Desktop/Арбитр бот/arbitr_parser/TXT_data.txt', self.checked_case_numbers)
                    self.write_to_txt('C:/Users/Дмитрий/Desktop/Арбитр бот/arbitr_parser/saved_url.txt', self.potential_urls)
                    if len(unchecked_casenumbres) == 0:
                        break
                    if errors_counter >= 3:
                        break
                    cur_page_num += 1
                    self.page_click(cur_page_num)
            pass
        except:
            pass

    """"def test(self):
        self.driver.get('https://kad.arbitr.ru/Card/d3e26ea9-f2b2-4217-b3db-03dfe52a1fd8')
        time.sleep(10)
        self.new_case_scrapping()"""

scrap = DriverScrapping()
scrap.scrap()
#scrap.test()