# coding=utf-8
from easyuiautomator.driver.driver import Driver
from easyuiautomator.common.exceptions import DeviceNotFound
import time
import unittest

app = Driver.connect_device()
app.find_element_by_id("tt")