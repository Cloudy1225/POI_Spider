import random
import time

import requests
import csv
import settings
from Utils import location_convert

class SpiderMan_ID:

    def __init__(self):
        self.key_list = settings.Key_List # 初始化 key 列表

    # 爬虫主函数 传参：ID.csv路径、保存路径
    def crawl(self, id_path, store_path):
        print('poi数量')
        with open(store_path, "w", encoding='utf-8', errors="ignore", newline='') as csvfile:
            count = 0
            csv_writer = csv.writer(csvfile)
            titles = ['id', 'name', 'longitude', 'latitude', 'time', 'opentime', 'closetime', 'adname', 'type',
                      'typecode']
            csv_writer.writerow(titles)

            id_strs = self.get_id_strs(id_path)

            i = 0
            for id_str in id_strs:
                json = self.request_json(id_str)
                rows = self.json_parser(json)
                csv_writer.writerows(rows)
                count += len(rows)
                i += 1
                if i % 5 == 0: # 每爬5次，输出一下信息
                   print(count)
            csvfile.close()
        print('Over: ' + str(count) +' :)')

    # 发送 GET 请求，返回 JSON
    def request_json(self, id_str):
        global response
        url = 'https://restapi.amap.com/v5/place/detail?parameters'
        params = {
            'key': random.choice(self.key_list),
            'id': id_str,
            'show_fields': 'business'
        }
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
            'Connection': 'close'
        }

        while True:
            try:
                response = requests.get(url, params = params, headers=headers)
                return response.json()
            except:
                print("Connection refused by the server..")
                print("Let me sleep for 5 seconds")
                print("ZZzzzz...")
                time.sleep(5)
                print("Was a nice sleep, now let me continue...")
                continue

    # 对请求结果进行分析，提取出需要的信息并返回
    def json_parser(self, json):
        # 请求结果形式入下
        '''json = {
            "status": "1",
            "info": "OK",
            "infocode": "10000",
            "pois": [
                {
                    "name": "小香港(大厂店)",
                    "id": "B0FFH97TVD",
                    "location": "118.735851,32.214951",
                    "type": "餐饮服务;休闲餐饮场所;休闲餐饮场所",
                    "typecode": "050400",
                    "pname": "江苏省",
                    "cityname": "南京市",
                    "adname": "六合区",
                    "address": "大厂庭芳路泰亿步行街",
                    "pcode": "320000",
                    "citycode": "025",
                    "adcode": "320116",
                    "business": {
                        "business_area": "江北新区",
                        "tel": "15951655817",
                        "rectag": "蛋糕店",
                        "keytag": "蛋糕店",
                        "rating": "4.4",
                        "cost": "41.00",
                        "opentime_today": "08:00-21:00",
                        "opentime_week": "08:00-21:00"
                    },
                    "indoor": {
                        "indoor_map": "0"
                    }
                }
            ],
            "count": "1"
        }
        '''

        pois = json.get("pois")

        rows = []
        for poi in pois:
            id = poi.get('id')
            name = poi.get('name')
            location_gcj02 = poi.get('location')
            longitude_gcj02 = float(location_gcj02.split(',')[0])
            latitude_gcj02 = float(location_gcj02.split(',')[1])
            location_wgs84 = location_convert.gcj02_to_wgs84(longitude_gcj02, latitude_gcj02)
            longitude_wgs84 = location_wgs84[0]
            latitude_wgs84 = location_wgs84[1]
            type = poi.get('type')
            typecode = poi.get('typecode')
            adname = poi.get('adname')
            business = poi.get('business')
            opentime_week = business.get('opentime_week')

            # 获取营业时间
            opentime = None
            closetime = None
            if(opentime_week):
                opentime_week_list = opentime_week.split('-')
                if len(opentime_week_list) > 1 :
                    opentime = opentime_week.split('-')[0]
                    closetime = opentime_week.split('-')[1]

            row = [id, name, longitude_wgs84, latitude_wgs84, opentime_week, opentime, closetime, adname, type, typecode]
            rows.append(row)
        return rows

    # 读取 ID.csv 里的 ID，并每 9 个组织在一块，虽说 API 文档说最多10个，但经测试最多只有9个每次
    # id_str 形如：'B001907D7U|B001907D7U|B001907D7U|B001907D7U|B001907D7U|B001907D7U|B001907D7U|B001907D7U|B001907D7U|'
    def get_id_strs(self, id_path):
        ids = []
        id_strs = []
        with open(id_path, "r", encoding='utf-8', errors="ignore", newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                ids.append(row[0])
            i = 0
            id_str = ''
            id_num = len(ids)
            for id in ids:
                id_str = id_str + (id + '|')
                i += 1
                if (i % 9 == 0) or (i == id_num):
                    id_strs.append(id_str)
                    id_str = ''
            csvfile.close()
        return id_strs


if __name__ == '__main__':

    spiderman = SpiderMan_ID()

    id_path = r'ID/文艺id.csv'
    store_path = r'Downloads/文艺.csv'
    # id_path = r'ID/公园广场id.csv'
    # store_path = r'Downloads/公园广场.csv'
    # id_path = r'ID/运动id.csv'
    # store_path = r'Downloads/运动.csv'
    # id_path = r'ID/休闲娱乐id.csv'
    # store_path = r'Downloads/休闲娱乐.csv'
    # id_path = r'ID/购物id.csv'
    # store_path = r'Downloads/购物.csv'
    # id_path = r'ID/生活id.csv'
    # store_path = r'Downloads/生活.csv'
    # id_path = r'ID/餐饮id.csv'
    # store_path = r'Downloads/餐饮.csv'
    spiderman.crawl(id_path, store_path)




