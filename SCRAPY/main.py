
from .api_manager.script_api import APIManager
from .api_manager.script_data import SpiderData


api = APIManager()
sd = SpiderData()


class xxxx:
        def __init__(self):
        # 网站名
        self.site_name = None
        # 栏目名
        self.site_type = None

        def process_item(self, item, spider):

            # 写好网站url
            if spider.name == 'xxxx':
                # 政府单位名
                self.site_name = 'xxx人民政府'
                # 栏目名
                self.site_type = '拟在建项目'
                #  # 调用API 并写入
                self.currency(item=item, spider=spider)
                # 写好网站 ID

            def currency(self, item, spider):
        # 调用spider 生成id 与key的方法
        logger.info(f"目前运行的文件为：{spider.name}")

        # 调用生成id 与key的方法
        try:
            item['title_date'] = sd.getTitleDate(str(item['title_date']))

            item['title_date'] = ''.join(item['title_date'])
        except ValueError:
            logger.error(f"网站名为：{item['title_name']}网站地址为：{item['site_path_url']} 日期校验失败")
            raise ValueError()

        data = {
            "title_date": item["title_date"],
            "title_name": item['title_name'],
            "update_time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "site_name": self.site_name,
            "title_type": self.site_type,
            "title_url": item['title_url'],
            "title_source": self.site_name,
            "site_path_name": item['site_path_name'],
            "site_path_url": item['site_path_url'],
            "content_html": item['content_html'],
            "update_user": "lzc",
            'site_id': item['site_id']
        }

        if data["title_type"] == '国家部委':
            # 国家部委链接
            api.updateConfigZfbw(site_id=data['site_id'],run_user=data['update_user'])
            ser = api.addDataToZfbwDB(data)
            self.repeat_print(ser, item)
        elif data["title_type"] == '拟在建项目':
            # 拟在建链接
            api.updateConfigNzj(site_id=data['site_id'],run_user=data['update_user'])
            ser = api.addDataToNzjDB(data)
            self.repeat_print(ser, item)
        elif data["title_type"] == '矿山企业':
            # 企业网站
            api.updateConfigKscp(site_id=data['site_id'],run_user=data['update_user'])
            ser = api.addDataToKscpDB(data)
            self.repeat_print(ser, item)
        elif data["title_type"] == '新闻媒体':
            # 新闻媒体
            api.updateConfigNews(site_id=data['site_id'],run_user=data['update_user'])
            ser = api.addDataToNewsDB(data)
            self.repeat_print(ser, item)
        else:
            # 临时数据表
            ser = api.addDataToTempDB(data)  # 临时数据表
            self.repeat_print(ser, item)


    def repeat_print(self, ser, item):
        if ser[0] == 200:

            logger.info(f"\033[33m1. !!! {item['title_name'], item['title_date'], item['title_url']}>> 更新成功  !!! \033[0m"
                        f"\n"
                        f"{ser}")
        elif ser[0] == 201:
            logger.info(f"{item['title_name'], item['title_date'], item['title_url']}>> 添加成功"
                        f"\n"
                        f"{ser}")
        else:
            logger.error(ser)

    def status(self, data, ser):
        if ser.__contains__(404):
            logger.error(f"{data['site_path_url']} | {data['site_path_url']} 网站错误")

    def update_print(self, ser, data):
        print("*" * 30)
        logger.info(f"\033[33m1. !!! {data['title_name'], data['title_date'], data['title_url']}\n |{ser}>> 更新成功  !!! \033[0m")

    def add_print(self, ser, data):
        print("*" * 30)
        logger.info(f"{data['title_name'], data['title_date'], data['title_url']}\n |{ser}>> 添加成功")
        # logger.info(f"\033[32m1. ### {data['title_name'], data['title_date'], data['title_url']}\n |{ser}>> 添加成功  ### \033[0m")
