import requests
import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import re



#模拟JS请求获取所有的番剧列表
# for i in range(0,200):
#     target_url = "https://bangumi.bilibili.com/media/web_api/search/result?season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&pub_date=-1&style_id=-1&order=3&st=1&sort=0&page={}&season_type=1&pagesize=20".format(i)
#     json_str = requests.get(target_url).text
#     json_dict = json.loads(json_str)
#     # 遍历字典
#     for dic in json_dict["result"]["data"]:
#         #得到番剧列表  recommendnew->该番剧下某一集的具体信息
#         print("link : " , dic["link"])
#         season_id = dic["link"].split("ss")[1]




service_args = []
service_args.append('--load-images=no')  ##关闭图片加载
service_args.append('--disk-cache=yes')  ##开启缓存
service_args.append('--ignore-ssl-errors=true')  ##忽略https错误

driver = webdriver.PhantomJS(service_args=service_args)
driver.get("https://bangumi.bilibili.com/anime/3461")
time.sleep(3)

# img_req = requests.get(url=target_url, headers=header)
# img_req.encoding = 'utf-8'
soup = BeautifulSoup(driver.page_source, 'lxml')
AnimeData = {}
AnimeData["animeName"] = soup.find(attrs={'class': 'media-info-title-t'}).get_text()

tags = ""
for x in soup.find_all(attrs={'class': 'media-tag'}):
    tags = tags + x.get_text() + ","
AnimeData["tags"] = tags[:-1]
AnimeData["animeTime"] = soup.find_all(attrs={'class': 'media-info-time'}).get_text()
AnimeData["IsEnd"] = soup.find_all(attrs={'class': 'media-info-time'})
AnimeData["Episodes"] = soup.find_all(attrs={'class': 'media-info-time'})
AnimeData["introText"] = soup.find_all(attrs={'class': 'media-info-intro-text'})
AnimeData["score"] = soup.find_all(attrs={'class': 'media-info-score-content'})
AnimeData["VA"] = ""
AnimeData["STAFF"] = ""

data = json.loads(requests.get("https://bangumi.bilibili.com/ext/web_api/season_count?season_id=3461&season_type=1").text)
AnimeData["coinCount"] = data["result"]["coins"]
AnimeData["danmuCount"] = data["result"]["danmakus"]
AnimeData["fansCount"] = data["result"]["favorites"]
AnimeData["palyCount"] = data["result"]["views"]
print(AnimeData)





