#!/usr/bin/python
# -*- coding: utf8 -*-

# author: yuzhengyang

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from PIL import Image

driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub',
         desired_capabilities=DesiredCapabilities.CHROME)

def get_pic():
    driver.get("https://online.vfsglobal.com/Global-Appointment/Account/RegisteredLogin?q=shSA0YnE4pLF9Xzwon/x/LuAvjd+x1cqVjY35ISPuGkygRZxO42Eb9Tvk53sBx29pA1X96p5xzS1CkcwCkeEXg==")
    for index in range(100, 200):
        element = driver.find_element_by_xpath('//*[@id="CaptchaImage"]')

        driver.save_screenshot('screenshot.png')

        left = element.location['x']
        top = element.location['y']
        right = element.location['x'] + element.size['width']
        bottom = element.location['y'] + element.size['height']

        im = Image.open('screenshot.png')
        im = im.crop((left, top, right, bottom))
        im.save('pic/' + str(index) + '.png')

        driver.refresh()
    driver.close()

if __name__ == '__main__':
    get_pic()
