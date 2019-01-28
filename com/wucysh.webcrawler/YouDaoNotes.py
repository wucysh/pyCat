# -*- coding: utf-8 -*-
import logging
from datetime import datetime

from selenium import webdriver
import sys
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

"""
贝壳二手房交易信息
"""


class HouseInfo():
    def __init__(self):
        self.mark = ''  # 简介
        self.name = ''  # 小区
        self.roomType = ''  # 户型
        self.roomArea = ''  # 面积
        self.listingPrice = ''  # 挂牌价
        self.dealPrice = ''  # 成交价格
        self.dealCycle = ''  # 成交周期
        self.isOneMonth = ''  # 30天成交标志

    def __str__(self):
        return self.mark + "^|^" + str(self.name) + "^|^" + self.roomType + "^|^" + self.roomArea + "^|^" + self.listingPrice + "^|^" + self.dealPrice + "^|^" + self.dealCycle + "^|^" + self.isOneMonth


class YouDaoNotes():
    def __init__(self):
        self.browser = webdriver.Chrome("/Users/wucysh/Desktop/Tengern/Python/soft/chromedriver")  # 驱动浏览器
        # self.url = 'http://127.0.0.1:44040/jobs/?page=1&items=50&latest=-1'
        self.browser.implicitly_wait(20)  # seconds
        self.url = 'https://note.youdao.com/web/#/file/recent/markdown/WEBd469718ac644042b26edc68d6147a2f5/'


    def getHtml(self):
        self.driver.get(self.url)
        try:
            print("Job info......")
            time.sleep(5)

            # fm_info_name = self.driver.find_element_by_xpath('/html/body/div[2]/table[3]').text  # 爬取基金经理名字 段世华
            # print("fm_info_name: ", fm_info_name)

            # self.allParse()  # 抓取私募基金数据

            self.parseInfo()  # 解析

        except BaseException as e:
            logging.exception(e)

    def parseInfo(self):
        try:

            # jobs_tables = self.driver.find_elements_by_css_selector("table[class=\"table table-bordered table-striped table-condensed sortable\"]")
            house_info_list = self.driver.find_element_by_class_name("listContent").find_elements_by_tag_name("li")
            for house_info in house_info_list:
                houseInfo = HouseInfo()
                for text in str(house_info.text).split("\n"):
                    print(text)
                    if "平米" in text:
                        houseInfo.mark = text.strip().replace("  ", " ")
                        houseInfo.name = houseInfo.mark.split(" ")[0]
                        houseInfo.roomType = houseInfo.mark.split(" ")[1]
                        houseInfo.roomArea = houseInfo.mark.split(" ")[2].strip().replace("平米", '')
                    if "30天内成交" in text and "万" in text:
                        houseInfo.isOneMonth = "1"
                        houseInfo.dealPrice = text[text.find("30天内成交") + 6:].replace("万", "").replace("*", "0")
                    if "挂牌" in text and "周期" in text:
                        houseInfo.listingPrice = text[:text.find("万")].replace("挂牌", "")
                        houseInfo.dealCycle = text[text.find("周期") + 2:].replace("天", "")

                print(houseInfo)


        except BaseException as e:
            logging.exception(e)

    def nextPage(self, pageNum):  # pageNum
        # 多次点击
        # self.driver.find_element_by_xpath('/html/body/div[2]/div[3]/ul/li[15]/a').click()  # 翻页

        self.url = self.url.replace('pg' + str(pageNum - 1), 'pg' + str(pageNum))
        print(self.url)

    def allParse(self):
        for pageNum in range(1, 2):  # 共39414 条记录 每页20条记录 39414/20
            self.nextPage(pageNum)  # 翻页
            self.getHtml()
        self.driver.close()

    def isElementExist(self, element):
        try:
            self.driver.find_element_by_css_selector(element)
            return True
        except:
            return False

    def get_cookies(self):
        """
            解析获取的cookie 用于登录
        :return:
        """
        cookiestr = """ 
                       {'domain': 'note.youdao.com', 'expiry': 2178894070, 'httpOnly': False, 'name': 'JSESSIONID', 'path': '/', 'secure': True, 'value': 'aaa8dPA4AImzv-X75wYHw'}
                {'domain': 'note.youdao.com', 'expiry': 1579705057, 'httpOnly': False, 'name': '__yadk_uid', 'path': '/', 'secure': True, 'value': 'QkAm0RPeZphqq9eUqjG4I5evpGOi42ZO'}
                {'domain': '.note.youdao.com', 'expiry': 1555945068.192352, 'httpOnly': True, 'name': 'YNOTE_PERS', 'path': '/', 'secure': True, 'value': 'v2|cqq||YNOTE||web||7776000000||1548169068024||101.245.245.182||qqD45C593515C0660698ADBB00C99BF5A4||QL0f6u6Lpz0Jz0fzWhMYMRqunfgZhfTL0JZ0MUWRLJu0kEPLOGOMgF0PyhHOmOMUG0pK0MQLP4eFRll0Lp4hMOfR'}
                {'domain': '.youdao.com', 'expiry': 2494249058.422083, 'httpOnly': False, 'name': 'OUTFOX_SEARCH_USER_ID', 'path': '/', 'secure': True, 'value': '"612147484@10.168.11.11"'}
                {'domain': '.youdao.com', 'expiry': 1611241058, 'httpOnly': False, 'name': 'OUTFOX_SEARCH_USER_ID_NCOO', 'path': '/', 'secure': True, 'value': '551172216.555068'}
                {'domain': '.youdao.com', 'expiry': 1611246071, 'httpOnly': False, 'name': '_ga', 'path': '/', 'secure': False, 'value': 'GA1.2.1236913433.1548169073'}
                {'domain': '.note.youdao.com', 'httpOnly': False, 'name': 'YNOTE_CSTK', 'path': '/', 'secure': False, 'value': 'ajOcS6mb'}
                {'domain': '.note.youdao.com', 'expiry': 2178894070, 'httpOnly': False, 'name': 'YNOTE_LOGIN', 'path': '/', 'secure': True, 'value': '3||1548169068126'}
                {'domain': '.note.youdao.com', 'expiry': 2178894070, 'httpOnly': True, 'name': 'YNOTE_SESS', 'path': '/', 'secure': True, 'value': 'v2|1j1JHiR_rRlGRLP4kMTuRkEkMYY6LgF0kEhHJF0fwK0zA64UY0fpu0kEhHpSO4zW0zmO4QuRMlMRll0MzEh4Uf0OYOfwBhfYm0'}
                {'domain': '.youdao.com', 'expiry': 1548174131, 'httpOnly': False, 'name': '_gat', 'path': '/', 'secure': False, 'value': '1'}
                {'domain': '.youdao.com', 'expiry': 1548260471, 'httpOnly': False, 'name': '_gid', 'path': '/', 'secure': False, 'value': 'GA1.2.29221930.1548169073'}
                {'domain': '.note.youdao.com', 'httpOnly': False, 'name': 'Hm_lpvt_53c97531c41019c3315b44853946c2c9', 'path': '/web/', 'secure': False, 'value': '1548174071'}
                {'domain': '.note.youdao.com', 'expiry': 1579710070, 'httpOnly': False, 'name': 'Hm_lvt_53c97531c41019c3315b44853946c2c9', 'path': '/web/', 'secure': False, 'value': '1548169070'}
               """
        cookies = list()
        for line in cookiestr.strip().split('\n'):
            line = line.strip().replace('\t', '')
            line = eval(line)
            # print(line)
            cookies.append(line)
        return cookies

    def open_ydn_main_page(self):
        """
        通过cookie 登录有道云笔记
        第一次设置等待时间，手动登录获取cookie信息
        :return:
        """
        self.browser.get(self.url)
        self.browser.implicitly_wait(10)
        self.browser.maximize_window()
        # 设置cookie
        for cookie in self.get_cookies():
            self.browser.add_cookie(cookie)
        self.browser.get(self.url)
        self.browser.implicitly_wait(10)
        print('-----打印cookies  共下次登录使用')
        for cookie in self.browser.get_cookies():
            print(cookie)

    def getRoot(self):
        """
        获取notes 根目录
        :return:
        """
        #  一级目录 我的文件夹
        self.getDirName('', self.browser.find_element_by_tag_name('tree-root'))

    def getDirName(self, path, elem):
        """
            循环获取下级目录
        :param elem:
        :return:
        """
        for li in elem.find_elements_by_tag_name('li'):
            title = li.find_element_by_class_name('file-name').get_attribute('title')
            print(path + '/' + str(title))
            try:
                li.find_element_by_class_name('arrow').click()
                self.getDirName(path + '/' + str(title), li.find_element_by_class_name('tree-container'))
            except:
                pass
            # 获取笔记名称
            self.getDirFileName(path + '/' + str(title), li)

    def getDirFileName(self, path, elem):
        """
            获取目录下的文件名
        :param path:
        :param elem:
        :return:
        """
        try:
            elem.click()
            self.browser.implicitly_wait(10)
            file_view = self.browser.find_element_by_tag_name('file-view')
            for li in file_view.find_elements_by_tag_name('li'):
                title = li.find_element_by_class_name('file-name').find_element_by_tag_name('span').text
                print(path + '/' + str(title))
                self.getNotesInfo(path + '/' + str(title), li)
        except BaseException as e:
            logging.exception(e)
            print("ERROR:" + path)

    def getNotesInfo(self, path, elem):
        """
            获取目录下的文件名
        :param path:
        :param elem:
        :return:
        """
        try:
            elem.click()  # 打开笔记
            self.browser.implicitly_wait(10)
            iframe = self.browser.find_element_by_class_name('detail-container').find_element_by_tag_name('iframe')
            self.browser.switch_to_frame(iframe)
            detail_container = self.browser.find_element_by_tag_name('body')
            print(detail_container.text)
        except BaseException as e:
            logging.exception(e)
            print("ERROR Note: " + path)
        finally:
            self.browser.switch_to_default_content()


if __name__ == "__main__":
    youdaonotes = YouDaoNotes()
    # jobsInfo.job_Parse()
    # youdaonotes.allParse()
    youdaonotes.get_cookies()

    youdaonotes.open_ydn_main_page()
    youdaonotes.getRoot()

    youdaonotes.browser.quit()
