"""
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 #
# @Time    : 2021/12/15 10:35
# @Author  : zicliang
# @Email   : hybpjx@163.com
# @File    : Invoking.py
# @Software: PyCharm
"""
import httpx
import time

from pkg.api_manager.script_api import APIManager
from pkg.api_manager.script_data import SpiderData
from settings.log_conf import *


class ApiInvok(object):

    def __init__(self, is_update: bool = True):
        # True 是允许数据重复 False 是不允许数据重复
        self.is_update = is_update

    # 生成title id
    def data_update(self, api_data):
        api = APIManager()
        sd = SpiderData()
        logger.info(f"标题链接：{api_data['title_url']},标题名称：{api_data['title_name']},标题时间：{api_data['title_date']}")

        # 调用生成id 与key的方法
        try:
            api_data['title_date'] = sd.getTitleDate(str(api_data['title_date']))

            api_data['title_date'] = ''.join(api_data['title_date'])
        except ValueError:
            logger.error(f"网站名为：{api_data['title_name']}网站地址为：{api_data['site_path_url']} 日期校验失败")
            raise ValueError()

        data = {
            # 网站 ID
            "site_id": api_data['site_id'],
            "title_name": api_data['title_name'],
            "title_url": api_data['title_url'],
            "content_html": str(api_data['content_html']),
            "title_date": api_data["title_date"],
            "update_time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "site_name": api_data['site_name'],
            "title_type": api_data['title_type'],
            "site_path_name": api_data['site_path_name'],
            "site_path_url": api_data['site_path_url'],
            "title_source": api_data['title_source'],
            "update_user": "lzc",
        }

        if data["title_type"] == '国家部委':
            # 国家部委链接
            api.updateConfigZfbw(site_id=data['site_id'], run_user=data['update_user'])
            ser = api.addDataToZfbwDB(data)
            self.repeat_print(ser, api_data)
        elif data["title_type"] == '拟在建项目':
            # 拟在建链接
            api.updateConfigNzj(site_id=data['site_id'], run_user=data['update_user'])
            ser = api.addDataToNzjDB(data)
            self.repeat_print(ser, api_data)
        elif data["title_type"] == '矿山企业':
            # 企业网站
            api.updateConfigKscp(site_id=data['site_id'], run_user=data['update_user'])
            ser = api.addDataToKscpDB(data)
            self.repeat_print(ser, api_data)
        elif data["title_type"] == '新闻媒体':
            # 新闻媒体
            api.updateConfigNews(site_id=data['site_id'], run_user=data['update_user'])
            ser = api.addDataToNewsDB()
            self.repeat_print(ser, api_data)
        else:
            # 临时数据表
            ser = api.addDataToTempDB(data)  # 临时数据表
            self.repeat_print(ser, api_data)

    def repeat_print(self, ser, api_data):
        if self.is_update:
            if ser[0] == 200:
                logger.warning(f"网站：{api_data['site_path_url']} 的数据重复 \n {ser}")
            if ser[0] == 201:
                logger.info(f"网站：{api_data['site_path_url']} 数据添加成功 \n {ser}")
        else:
            # false 抛出异常
            if ser[0] == 200:
                logger.warning(f"网站：{api_data['site_path_url']} 的数据重复 \n {ser}")
                raise RuntimeError(f"网站：{api_data['site_path_url']} 的数据重复了")
