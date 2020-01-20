#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
#@author: Mr Zeng
#date: 2018-10-14
 
from splinter.browser import Browser
from time import sleep
import os
import sys

 
import httplib2
from urllib import parse

class BuyTicket(object):
  def __init__(self, username, passwd, order, passengers, seatType, ticketType, daytime, starts, ends):
    # 用户名 密码
    self.username = username
    self.passwd = passwd
    # 车次,选择第几趟,0则从上之下依次点击
    self.order = order
    # 乘客名
    self.passengers = passengers
    # 席位
    self.seatType = seatType
    self.ticketType = ticketType
    # 时间格式2018-02-05
    self.daytime = daytime
    # 起始地和终点
    self.starts = starts
    self.ends = ends
 
    self.login_url = 'https://kyfw.12306.cn/otn/login/init'
    self.initMy_url = 'https://kyfw.12306.cn/otn/index/initMy12306'
    self.ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
    self.confirm_url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
    # 浏览器名称
    #self.driver_name = 'firefox' # chrome firefox
    #chrome
    self.driver_name = 'chrome'
    self.executable_path = '/usr/local/bin/chromedriver'
    # 火狐浏览器第三方驱动
    #self.executable_path = os.getcwd()+'/geckodriver' # 获取工程目录下的火狐驱动 chromedriver

    # 座位类型所在td位置
    if seat_type == '商务座特等座':
        seat_type_index = 1
        seat_type_value = 9
    elif seat_type == '一等座':
        seat_type_index = 2
        seat_type_value = 'M'
    elif seat_type == '二等座':
        seat_type_index = 3
        seat_type_value = 0
    elif seat_type == '高级软卧':
        seat_type_index = 4
        seat_type_value = 6
    elif seat_type == '软卧':
        seat_type_index = 5
        seat_type_value = 4
    elif seat_type == '动卧':
        seat_type_index = 6
        seat_type_value = 'F'
    elif seat_type == '硬卧':
        seat_type_index = 7
        seat_type_value = 3
    elif seat_type == '软座':
        seat_type_index = 8
        seat_type_value = 2
    elif seat_type == '硬座':
        seat_type_index = 9
        seat_type_value = 1
    elif seat_type == '无座':
        seat_type_index = 10
        seat_type_value = 1
    elif seat_type == '其他':
        seat_type_index = 11
        seat_type_value = 1
    else:
        seat_type_index = 7
        seat_type_value = 3
    self.seat_type_index = seat_type_index
    #self.seat_type_value = seat_type_value

  def send_sms(self, mobile, sms_info):
    """发送手机通知短信，用的是-互亿无线-的测试短信"""
    host = "106.ihuyi.com"
    sms_send_uri = "/webservice/sms.php?method=Submit"
    account = "C59782899"
    pass_word = "19d4d9c0796532c7328e8b82e2812655"
    params = parse.urlencode(
      {'account': account, 'password': pass_word, 'content': sms_info, 'mobile': mobile, 'format': 'json'}
    )
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib2.HTTPConnectionWithTimeout(host, port=80, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str
  def login(self):
    # 访问登录网址
    self.driver.visit(self.login_url)
    # 填充用户名
    self.driver.fill("loginUserDTO.user_name", self.username)
    # sleep(1)
    # 填充密码
    self.driver.fill("userDTO.password", self.passwd)
    #logbticket.info("请手动输入验证码...")
    print('请手动输入验证码...') # 目前没有自动验证码
    # 循环等待登录，登录成功，跳出循环
    while True:
      if self.driver.url != self.initMy_url:
        sleep(1)
      else:
        break
 
  def start_buy(self):
    # 这些设置都是必要的
    # chrome_options = Options()
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-setuid-sandbox")
    # chrome_options.add_argument("disable-infobars") # 禁用网页上部的提示栏
    # self.driver = Browser(driver_name=self.driver_name, options=chrome_options, executable_path=self.executable_path)
    self.driver = Browser(driver_name=self.driver_name,
               executable_path=self.executable_path)
    # 设置窗口大小尺寸
    self.driver.driver.set_window_size(1000, 800)
    # 用户登录
    self.login()
    # 进入选票网站
    ##self.driver.visit(self.ticket_url)
    exit_state = 0
    while exit_state == 0:
      self.driver.visit(self.ticket_url)
      try:
        print("开始刷票....")
        # sleep(1)
        # 加载查询信息
        self.driver.cookies.add({"_jc_save_fromStation": self.starts})
        self.driver.cookies.add({"_jc_save_toStation": self.ends})
        self.driver.cookies.add({"_jc_save_fromDate": self.daytime})
   
        self.driver.reload()
   
        count = 0
        if self.order != 0:
          while self.driver.url == self.ticket_url:
            self.driver.find_by_text("查询").click()
            count = count+1
            print("第 %d 次点击查询..." % count)
            # sleep(1)
            try:
              self.driver.find_by_text("预订")[self.order - 1].click() 
              sleep(1.5)
            except Exception as e:
              print(e)
              print("预订失败...")
              continue
        else:
          while self.driver.url == self.ticket_url:
            self.driver.find_by_text("查询").click()
            count += 1
            print("第 %d 次点击查询..." % count)
            state = 0
            sleep(1)
            try:
              for i in self.driver.find_by_xpath("//tbody[@id='queryLeftTable']/tr/td/a[contains(text(), '预订')]"):#self.driver.find_by_text("预订"):
                current_tr = i.find_by_xpath("./../..")
                if current_tr.find_by_tag('td')[self.seat_type_index].text == '--':
                  print('无此座位类型出售，继续尝试...')
                  #sys.exit(1)
                elif current_tr.find_by_tag('td')[self.seat_type_index].text == '无':
                  print('无票，继续尝试...')
                else:
                  print('查询到火车票')
                  state = 1
                  i.click()
                  break
                sleep(1)
              if state == 1:
                break
            except Exception as e:
              print(e)
              print("预订失败...")
              continue
   
        print("开始预订...")
        # self.driver.reload()
        #sleep(1)
        if self.driver.find_by_id("content_defaultwarningAlert_hearder").text.strip() == '当前时间不可以订票':
          print('当前时间不可以订票')
          sys.exit(1)
        while True:
          if self.driver.url == self.confirm_url:
            break
          else:
            sleep(1)
        if self.driver.is_text_present('splinter.readthedocs.io'):
          print("开始选择乘客...")
        #sleep(5)
        if self.driver.url == self.confirm_url:
          for p in self.passengers:
            pg = self.driver.find_by_xpath("//ul[@id='normal_passenger_id']/li/label[contains(text(), '"+p+"')]") #.last.click()
            pg.last.click()
        print("乘客选择完毕...\n")

        print("开始选座...")
        sleep(1)
        i = 0
        while len(self.passengers) > 0:
          i = i + 1
          seat_id_string = "seatType_" + str(i)
          ticket_id_string = "ticketType_" + str(i)
          self.driver.find_by_xpath('//select[@id="%s"]/option[@value="%s"]'
                       % (seat_id_string, self.seatType)).first._element.click()
          self.driver.find_by_xpath('//select[@id="%s"]//option[@value="%s"]'
                       % (ticket_id_string, self.ticketType)).first._element.click()
          # self.driver.select("confirmTicketType", "3")
          self.passengers.pop()
          sleep(1)
        self.driver.find_by_id("submitOrder_id").click()
        sleep(1.5)
        print("选座完毕...\n")

        print("提交订单...")
        ##input('按任意键继续:')
        sleep(1)
        self.driver.find_by_id("qr_submit_id").click()
        if self.driver.is_text_present('splinter.readthedocs.io'):
          print('正在检查余票...')
        if self.driver.find_by_id("orderResultInfo_id").find_by_tag('div').text.strip() == '出票失败!':
          print(self.driver.find_by_id("orderResultInfo_id").find_by_tag('p')[0].text)
        else:
          print('火车票订票成功，请速度支付订单！\n')
          exit_state = 1 
          input('按任意键继续:')
      except Exception as e:
        print(e)
        exit_state = 0
 
city = {"深圳": "%u6DF1%u5733%2CSZQ",
    "武汉": "%u6B66%u6C49%2CWHN",
    "随州": "%u968F%u5DDE%2CSZN",
    '恩施': '%u6069%u65BD%2CESN',}
 
seatT = {"硬卧": "3",
     "软卧": "4",
     "硬座": "1",
     "二等座": "O",
     "一等座": "M",
     "商务座": "9",
     "无座": '1'}
 
if __name__ == '__main__':
  # 用户名
  username = "XXX" #你的12306用户名
  # 密码
  password = "XXX" #你的12306登陆密码
  # 车次选择，0代表所有车次
  order = 0
  # 乘客名，比如passengers = ['丁小红', '丁小明']
  passengers = ["XXX"]
  # 日期，格式为：'2018-01-20'
  daytime = "2018-10-07"
  # 出发地(需填写cookie值)
  starts = city["恩施"] # 武汉
  # 目的地(需填写cookie值)
  ends = city["武汉"] # 北京
  # 席别
  seat_type = "无座"
  seatType = seatT[seat_type] # 二等座
  # 票种
  ticketType = "1" # 成人票
 
  BuyTicket(username, password, order, passengers, seatType, ticketType, daytime, starts, ends).start_buy()