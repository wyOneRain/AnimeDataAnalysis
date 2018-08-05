import requests
import json
import time
from bs4 import BeautifulSoup
from Bilili_Anime import DBHelper
from selenium import webdriver
import re

db = DBHelper.DBhelper()

# 模拟JS请求获取所有的番剧列表
for i in range(0,152):
    target_url = "https://bangumi.bilibili.com/media/web_api/search/result?season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&pub_date=-1&style_id=-1&order=3&st=1&sort=0&page={}&season_type=1&pagesize=20".format(i)
    json_link = requests.get(target_url).text
    json_link = json.loads(json_link)
    # 遍历字典
    AnimeData={}
    AnimeMX={}
    for link in json_link["result"]["data"]:
        #得到番剧列表  recommendnew->该番剧下某一集的具体信息
        # print("link : " , link["link"])
        print(link["link"])
        data = requests.get(link["link"]).text
        soup = BeautifulSoup(data, 'lxml')
        tags = soup.find("body").find("script")
        for tag in tags:
            js_data = json.loads(str(tag).split("function()")[0][:-2].replace("window.__INITIAL_STATE__=", ""))
            AnimeData["animeName"] = js_data["mediaInfo"]["title"]
            AnimeData["introText"] = js_data["mediaInfo"]["evaluate"].replace("\n","")
            AnimeData["score"] = js_data["mediaRating"]["score"]
            AnimeData["VA"] = js_data["mediaInfo"]["actors"].replace("\n","")
            AnimeData["STAFF"] = js_data["mediaInfo"]["staff"].replace("\n","")
            AnimeData["coinCount"] = js_data["mediaInfo"]["stat"]["coins"]
            AnimeData["danmuCount"] = js_data["mediaInfo"]["stat"]["danmakus"]
            AnimeData["fansCount"] = js_data["mediaInfo"]["stat"]["favorites"]
            AnimeData["playCount"] = js_data["mediaInfo"]["stat"]["views"]
            AnimeData["tags"] = str(js_data["mediaInfo"]["style"]).replace("'","")[1:-1]
            AnimeData["Country"] = js_data["mediaInfo"]["areas"][0]["name"]
            AnimeData["animeTime"] = js_data["epInfo"]["pub_real_time"]

            db.insert_data("AnimeInfo",AnimeData)

            for MXinfo in js_data["epList"]:
                AnimeMX["animeName"] = AnimeData["animeName"]
                AnimeMX["EpisodeName"] = MXinfo["index_title"]
                AnimeMX["avSec"] = MXinfo["aid"]
                AnimeMX["EpisodeNo"] = MXinfo["index"]

                js = json.loads(requests.get("https://api.bilibili.com/x/web-interface/archive/stat?aid={}".format(MXinfo["aid"])).text)
                AnimeMX["play"] = js["data"]["view"]
                AnimeMX["danmu"] = js["data"]["danmaku"]
                AnimeMX["coin"] = js["data"]["coin"]

                db.insert_data("AnimeMX", AnimeMX)


# soup = BeautifulSoup(data, 'lxml')
# tags = soup.find("body").find("script")
# for tag in tags:
#     js = json.loads(str(tag).split("function()")[0][:-2].replace("window.__INITIAL_STATE__=",""))
#     print(js["mediaInfo"])


