#! /usr/bin/env python3
# -*- coding:utf-8 -*-
"""
====================================================================
Project Name: mining spider
File description:
Author: Liao Heng
Create Date: 2021-08-22
====================================================================
"""
import time
import os
import socket
import platform
import datetime

from pkg.api_manager.api_request import APIRequest
from pkg.api_manager.script_data import SpiderData


class APIManager(object):
    def __init__(self):
        self.api_request = APIRequest()
        self.script_data = SpiderData()
        self.local_info = self.getLocalInfo()
        self.api_url_dict = {
            "spider_nzj_config": "http://mykyls.xyz:38080/api/spider_nzj_config/",
            "spider_nzj_data": "http://mykyls.xyz:38080/api/spider_nzj_data/",

            "spider_zfbw_config": "http://mykyls.xyz:38080/api/spider_zfbw_config/",
            "spider_zfbw_data": "http://mykyls.xyz:38080/api/spider_zfbw_data/",

            "spider_news_config": "http://mykyls.xyz:38080/api/spider_news_config/",
            "spider_news_data": "http://mykyls.xyz:38080/api/spider_news_data/",

            "spider_kscp_config": "http://mykyls.xyz:38080/api/spider_kscp_config/",
            "spider_kscp_data": "http://mykyls.xyz:38080/api/spider_kscp_data/",

            "spider_temp_data": "http://mykyls.xyz:38080/api/spider_temp_data/",
            "spider_ckq_data": "http://mykyls.xyz:38080/api/spider_ckq_data/",
            "spider_tkq_data": "http://mykyls.xyz:38080/api/spider_tkq_data/",

            "spider_qcc_config": "http://mykyls.xyz:38080/api/spider_qcc_config/",
            "spider_qcc_news": "http://mykyls.xyz:38080/api/spider_qcc_news/",
            "spider_qcc_other": "http://mykyls.xyz:38080/api/spider_qcc_other/",
            "spider_qcc_tender": "http://mykyls.xyz:38080/api/spider_qcc_tender/",
        }

    def getLocalInfo(self):
        local_info = []
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        os_ver = platform.system()
        local_info.append("%s (%s) %s" % (hostname, local_ip, os_ver))
        local_info.append("%s" % os.getcwd())
        local_info.append("%s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return "\n".join(local_info)

    def __getConfigData(self, url_params={}, table_name="spider_nzj_config"):
        # 获取目标网站数据
        try:
            url = self.api_url_dict[table_name]
            status, return_data = self.api_request.get(url, url_params)
            results = return_data.get("results", [])
            # print("getConfigData %s: %s, %s" % (status, url, return_data))
        except Exception as e:
            print("getConfigData error:", str(e))
            results = []
        return results

    def __updateConfigData(self, site_id, run_status="正在更新", run_message="运行中...", run_user="test",
                           table_name="spider_nzj_config"):
        # 更新目标网站数据
        run_status_list = ["错误", "等待更新", "正在更新", "结束"]
        if not site_id or run_status not in run_status_list:
            return 404, "updateConfigData error: site_id(%s) or run_status(%s)" % (site_id, run_status)
        config_data = self.__getConfigData({"site_id": site_id}, table_name)
        if config_data:
            config_data = config_data[0]
        else:
            return 404, "updateConfigData error：site_id %s" % site_id
        update_data = {
            'site_id': config_data['site_id'],
            'site_name': config_data['site_name'],
            "run_status": run_status,
            "run_message": self.local_info + "\n运行信息：%s" % run_message,
            "run_time": int(time.time()),
            "update_user": run_user
        }
        url = self.api_url_dict[table_name] + str(config_data["id"]) + "/"
        api_data = self.api_request.put(url, update_data)
        return api_data

    def __addDataToDB(self, title_dict={}, table_name="spider_nzj_config"):
        # 发送数据
        if not title_dict["site_name"] or not title_dict["title_url"] or not title_dict["site_path_url"]:
            return 404, {'status': False, 'message': 'title_data error'}
        title_data1 = self.script_data.analysisTitleData(title_dict)
        url = self.api_url_dict[table_name]
        result = self.api_request.post(url, title_data1)
        return result

    # 拟在建项目
    def getConfigNzj(self, url_params={}):
        # 拟在建项目 目标网站
        table_name = "spider_nzj_config"
        return self.__getConfigData(url_params, table_name)

    def updateConfigNzj(self, site_id, run_status="正在更新", run_message="运行中...", run_user="test"):
        # 拟在建项目 目标网站
        table_name = "spider_nzj_config"
        return self.__updateConfigData(site_id, run_status, run_message, run_user, table_name)

    def addDataToNzjDB(self, title_dict={}):
        # 拟在建项目 爬虫数据
        table_name = "spider_nzj_data"
        return self.__addDataToDB(title_dict, table_name)

    # 政府部委
    def getConfigZfbw(self, url_params={}):
        # 政府部委 目标网站
        table_name = "spider_zfbw_config"
        return self.__getConfigData(url_params, table_name)

    def updateConfigZfbw(self, site_id, run_status="正在更新", run_message="运行中...", run_user="test"):
        # 政府部委 目标网站
        table_name = "spider_zfbw_config"
        return self.__updateConfigData(site_id, run_status, run_message, run_user, table_name)

    def addDataToZfbwDB(self, title_dict={}):
        # 政府部委 爬虫数据
        table_name = "spider_zfbw_data"
        return self.__addDataToDB(title_dict, table_name)

    # 新闻媒体
    def getConfigNews(self, url_params={}):
        # 新闻媒体 目标网站
        table_name = "spider_news_config"
        return self.__getConfigData(url_params, table_name)

    def updateConfigNews(self, site_id, run_status="正在更新", run_message="运行中...", run_user="test"):
        # 新闻媒体 目标网站
        table_name = "spider_news_config"
        return self.__updateConfigData(site_id, run_status, run_message, run_user, table_name)

    def addDataToNewsDB(self, title_dict={}):
        # 新闻媒体 爬虫数据
        table_name = "spider_news_data"
        return self.__addDataToDB(title_dict, table_name)

    # 矿山企业
    def getConfigKscp(self, url_params={}):
        # 矿山企业 目标网站
        table_name = "spider_kscp_config"
        return self.__getConfigData(url_params, table_name)

    def updateConfigKscp(self, site_id, run_status="正在更新", run_message="运行中...", run_user="test"):
        # 矿山企业 目标网站
        table_name = "spider_kscp_config"
        return self.__updateConfigData(site_id, run_status, run_message, run_user, table_name)

    def addDataToKscpDB(self, title_dict={}):
        # 矿山企业 爬虫数据
        table_name = "spider_kscp_data"
        return self.__addDataToDB(title_dict, table_name)

    # 其他数据
    def addDataToTempDB(self, title_dict={}):
        # 临时数据 爬虫数据
        table_name = "spider_temp_data"
        return self.__addDataToDB(title_dict, table_name)

    def addDataToCkqDB(self, title_dict={}):
        # 采矿权 爬虫数据
        table_name = "spider_ckq_data"
        return self.__addDataToDB(title_dict, table_name)

    def addDataToTkqDB(self, title_dict={}):
        # 探矿权 爬虫数据
        table_name = "spider_tkq_data"
        return self.__addDataToDB(title_dict, table_name)

    # 企查查
    def getConfigQcc(self, url_params={}):
        # 企查查 目标网站
        table_name = "spider_qcc_config"
        return self.__getConfigData(url_params, table_name)

    def updateConfigQcc(self, site_id, run_status="正在更新", run_message="运行中...", run_user="test"):
        # 企查查 目标网站
        table_name = "spider_qcc_config"
        return self.__updateConfigData(site_id, run_status, run_message, run_user, table_name)

    def addDataToQccNewsDB(self, title_dict={}):
        # 企查查 新闻 爬虫数据
        table_name = "spider_qcc_news"
        return self.__addDataToDB(title_dict, table_name)

    def addDataToQccOtherDB(self, title_dict={}):
        # 企查查 其他 爬虫数据
        table_name = "spider_qcc_other"
        return self.__addDataToDB(title_dict, table_name)

    def addDataToQccTenderDB(self, title_dict={}):
        # 企查查 招投标 爬虫数据
        table_name = "spider_qcc_tender"
        return self.__addDataToDB(title_dict, table_name)


if __name__ == "__main__":
    api = APIManager()
    url_params = { "script_name": "script_qgj", "ordering": "run_time"}
    data = api.getConfigNzj(url_params)
    print(data)
    # 正在更新
    data = api.updateConfigNzj(site_id="B4BEBF05C1", run_status="正在更新", run_message="正在更新", run_user="test")
    print(data)
    # 运行结束
    #data = api.updateConfigNzj(site_id="B4BEBF05C1", run_status="结束", run_message="结束", run_user="test")
    title_data = {
        "title_date": "2022-08-27",
        "title_name": "测试数据",
        "site_id": "123",
        "site_name": "测试数据",
        "title_type": "",
        "title_url": "http://zrzy.hebei.gov.cn/heb/gongk/gkml/gggs/qtgg/zfj/10636259671725203456.html",
        "title_source": "",
        "site_path_name": "公告公示",
        "site_path_url": "http://zrzy.hebei.gov.cn/heb/gongk/gkml/gggs/",
        "content_html": "<html><body><div>测试数据矿2022-01-27</div></body></html>",
        "update_user": "",
    }
    data = api.addDataToNzjDB(title_data)
    print(data)




