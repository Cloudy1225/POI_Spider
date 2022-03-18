# POI_Spider
以南京市为例，通过高德地图API获取POI

## 项目文件结构：

```bash
POI_Spider:
│  .gitignore    
│  LICENSE
│  README.md
│  settings.py # 配置 key 池，城市编码adcoode池，POI类型typecode池                
│  SpiderMan_ID.py # 通过 ID 爬取
│  SpiderMan_Keywords.py # 通过关键字爬取
│
│
├─Downloads
│      文艺.csv # ID爬取结果示例
│      运动.csv # 关键字爬取结果示例
│
├─ID
│      文艺id.csv # 通过 ID 爬取所需的id来源
│
├─Utils
       AMap_adcode_citycode_20210406.xlsx # 高德地图城市编码表
       amap_poicode.xlsx # 高德地图 POI 类型编码表
       location_convert.py # 坐标转换工具
```

## 采集策略：

- Keywords：以南京市为例，为尽可能多的爬取，将南京市细分为几个区，POI类型细分到小类
- ID：若已知待爬取 POI 的 id ，直接调用相关接口爬取
- 多边形搜索：将南京市划分为很多小网格，然后调用高德地图 多边形区域搜索 接口来爬取（未实现）

## 项目启动：

- 根据爬取策略配置信息
  - Keywords：在 settings.py 文件中配置你的 key 值、城市列表、类型列表
  - ID：在 ID 目录下增添要爬取的 id.csv 文件，在 settings.py 文件中配置你的 key 值
- 程序入口在爬取策略对应的 .py 文件中

## 缺陷：

- Keywords：南京市有11个区，经测试一次最多获取的POI数不超过900，所以对于一个小类来说，最多可获取9000多条数据，若该小类数量超10000，必然获取不全
- ID：缺陷就是你不知道ID

## 关于：

我参加的大创需要获取与夜间经济有关的POI数据。对于南京市来说，若想获取所有POI，需要将南京市划分为很多小网格，然后调用高德地图 多边形区域搜索 接口来爬取。由于尝试用 ArcGIS 绘制渔网图失败，故放弃。后灵光一闪，去淘宝买了南京市的 POI 数据。导入数据库处理后，得到了所需的POIs。后来又希望知道营业时间，但买回的数据中并没有，所以将 POI 的 id 导了出来，通过调用 ID搜索 接口来提取营业时间。
