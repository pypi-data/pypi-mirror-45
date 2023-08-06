# coding=utf-8
import logging
import time
import os
from autotest.switch import Switch
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

    def __find_element(self, *loc):
        try:
            WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located(loc))
            return self.driver.find_element(*loc)
        except:
            logging.error(u"%s element was not found in the %s page" % (loc, self))

    def switch_frame(self, status=False, *loc):
        if status:
            self.driver.switch_to_frame(*loc)
        else:
            self.driver.switch_to_default_content()
        time.sleep(1.5)

    def script(self, src):
        self.driver.execute_script(src)
        time.sleep(1.5)

    def send_keys(self, loc, value):
        self.__find_element(*loc).send_keys(*value)
        time.sleep(1.3)

    def click(self, *loc):
        self.__find_element(*loc).click()
        time.sleep(1.5)

    def text(self, *loc):
        return self.__find_element(*loc).text

    def alert(self, opt, *loc):
        a = self.driver.switch_to_alert()
        for case in Switch(opt):
            if case(1):
                a.accept()
                break
            if case(2):
                a.dismiss()
                break
            if case(3):
                a.sendkeys(*loc)
                break
            if case():
                return a.text()

    def press_key(self, code):
        self.driver.press_keycode(code)  # 回车66

    def get_attribute(self, *loc, name):
        return self.__find_element(*loc).get_attribute(name)

    def size(self, *loc):
        return self.__find_element(*loc).size()

    def switch_content(self):
        self.driver.switch_to.context(None)

    def flick(self, start_x, start_y, end_x, end_y):
        self.driver.flick(start_x, start_y, end_x, end_y)

    def get_window_size(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return x, y

    def swipe_up(self, pagination):
        l = self.get_window_size()
        x1 = int(l[0] * 0.5)
        y1 = int(l[1] * 0.75)
        y2 = int(l[1] * 0.25)
        for i in range(pagination):
            self.driver.swipe(x1, y1, x1, y2, 800)

    def swipe_down(self, pagination):
        l = self.get_window_size()
        x1 = int(l[0] * 0.5)
        y1 = int(l[1] * 0.25)
        y2 = int(l[1] * 0.75)
        for i in range(pagination):
            self.driver.swipe(x1, y1, x1, y2, 800)

    def swipe_left(self):
        l = self.get_window_size()
        x1 = int(l[0] * 0.75)
        y1 = int(l[1] * 0.5)
        x2 = int(l[0] * 0.05)
        self.driver.swipe(x1, y1, x2, y1, 800)

    def swipe_right(self):
        l = self.get_window_size()
        x1 = int(l[0] * 0.05)
        y1 = int(l[1] * 0.5)
        x2 = int(l[0] * 0.75)
        self.driver.swipe(x1, y1, x2, y1, 800)
