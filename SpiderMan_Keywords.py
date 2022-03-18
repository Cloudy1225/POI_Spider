import random

import requests
import csv
import settings
from Utils import location_convert

class SpiderMan_Keywords:

    def __init__(self):
        self.key_list = settings.Key_List   # 初始化 key 列表
        self.adcode_list = settings.Adcode_List  # 初始化城市列表
        self.typecode_list = settings.Typecode_List # 初始化类型列表

    # 爬虫主函数 传参：类型码、保存路径
    def crawl(self, store_path):
        count = 0
        print('Over: typecode, adcode')
        with open(store_path, "w", encoding='utf-8', errors="ignore", newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            titles = ['id', 'name', 'longitude', 'latitude', 'time', 'opentime', 'closetime', 'adname', 'type', 'typecode']
            csv_writer.writerow(titles)
            for typecode in self.typecode_list:
                for adcode in self.adcode_list:
                    for page_num in range(1, 41):
                        json = self.request_json(typecode, adcode, page_num)
                        count += int(json.get('count'))
                        if(json.get('count') == '0'):
                            message = 'Over: '+typecode+', '+str(adcode)
                            print(message)
                            break
                        rows = self.json_parser(json)
                        csv_writer.writerows(rows)
        csvfile.close()
        print('共获取：', end='')
        print(count)

    # 用于测试，也可以爬取 传参：类型码 城市码 保存路径
    def crawl_test(self, typecode_list, adcode_list, store_path):
        count = 0
        with open(store_path, "w", encoding='utf-8', errors="ignore", newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            titles = ['id', 'name', 'longitude', 'latitude', 'time', 'opentime', 'closetime', 'adname', 'type', 'typecode']
            csv_writer.writerow(titles)
            for typecode in typecode_list:
                for adcode in adcode_list:
                    for page_num in range(1, 41): # 25 * 40 = 1000 这是上限
                        json = self.request_json(typecode, adcode, page_num)
                        count += int(json.get('count'))
                        if(json.get('count') == '0'):
                            message = 'Over: '+typecode+', '+str(adcode)+', '+str(page_num)
                            print(message)
                            break
                        rows = self.json_parser(json)
                        csv_writer.writerows(rows)
        csvfile.close()
        print('共获取：', end='')
        print(count)


    # 发送 GET 请求，返回 JSON
    def request_json(self, typecode, adcode, page_num):
        url = 'https://restapi.amap.com/v5/place/text?parameters'
        params = {
            'key': random.choice(self.key_list),
            'types': typecode,
            'region': adcode,
            'city_limit': True,
            'show_fields': 'business',
            'page_size': 25,
            'page_num': page_num
        }
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        }
        response= requests.get(url = url, params = params, headers = headers)
        return response.json()

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

            # 获取营业时间
            opentime_week = business.get('opentime_week')
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


if __name__ == '__main__':

    spiderman = SpiderMan_Keywords()
    store_path = r'Downloads/运动.csv'
    spiderman.crawl(store_path)

