# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

if __name__ == "__main__":
    browser = webdriver.Firefox()
    browser.get('https://www.baidu.com')
    print browser.title
    assert '百度' in browser.title
    elem = browser.find_element_by_name('wd')
    elem.send_keys('seleniumhq' + Keys.RETURN)
    time.sleep(10)
    try:
        browser.find_element_by_xpath('//a[contains(@href,"http://www.seleniumhq.org")]')
    except NoSuchElementException:
        print "can't find seleniumhq"
    browser.close()
