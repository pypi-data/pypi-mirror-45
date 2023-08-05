# coding=utf-8
from easyuiautomator.driver.driver import Driver
import time

app = Driver.connect_device()
while True:
    app.find_element_by_xpath("//*")
    time.sleep(0.1)