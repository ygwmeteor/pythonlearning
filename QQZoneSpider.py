#coding:utf-8

import unittest
import time
from selenium import webdriver
from bs4 import BeautifulSoup


class seleniumTest(unittest.TestCase):
    user = ''  # 你的QQ号
    pw = ''  # 你的QQ密码

    def setUp(self):
        # 调试的时候用firefox比较直观
        # self.driver = webdriver.PhantomJS()
        self.driver = webdriver.Firefox()

    def testEle(self):
        driver = self.driver
        # 浏览器窗口最大化
       # driver.maximize_window()
        # 浏览器地址定向为qq登陆页面
        driver.get("http://haijia.bjxueche.net/")
        # 很多时候网页由多个<frame>或<iframe>组成，webdriver默认定位的是最外层的frame，
        # 所以这里需要选中一下frame，否则找不到下面需要的网页元素
       # driver.switch_to.frame("login_frame")
        # 自动点击账号登陆方式
       # driver.find_element_by_id("switcher_plogin").click()
        # 账号输入框输入已知qq账号
        driver.find_element_by_id("txtUserName").send_keys(self.user)
        # 密码框输入已知密码
        driver.find_element_by_id("txtPassword").send_keys(self.pw)
        time.sleep(10)
        # 自动点击登陆按钮
        driver.find_element_by_id("BtnLogin").click()
        while 1 :
        	driver.get("http://haijia.bjxueche.net/ych2.aspx")
        	time.sleep(20)

        # 如果登录比较频繁或者服务器繁忙的时候，一次模拟点击可能失败，所以想到可以尝试多次，
        # 但是像QQ空间这种比较知名的社区在多次登录后都会出现验证码，验证码自动处理又是一个
        # 大问题，本例不赘述。本例采用手动确认的方式。即如果观察到自动登陆失败，手动登录后
        # 再执行下列操作。
       
    def tearDown(self):
        print('down')

if __name__ == "__main__":
    unittest.main()
