import requests
import json
import time
from bs4 import BeautifulSoup
from Bilili_Anime import DBHelper
import threading
from selenium import webdriver
import re

header={ "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
row = 0 #分页查询
R=threading.Lock() #加锁
def get_Anime():
        db = DBHelper.DBhelper()
        AnimeData = {}
        AnimeMX = {}
        global row
        while True:
            R.acquire()
            rs = db.select_data(
                "SELECT top 20 animeURL,isVisited FROM (SELECT animeURL,isVisited,ROW_NUMBER() OVER (ORDER BY animeURL) AS RowNumber FROM AnimeURL)  as A where A.RowNumber >= {}".format(
                    row))
            row = row + 20
            print(row)
            R.release()
            if len(rs) == 0:
                break
            for rs_data in rs:
                #获取番剧的基本信息
                try:
                    data = requests.get(rs_data[0],headers = header,timeout = 60).text
                    soup = BeautifulSoup(data, 'lxml')
                    tags = soup.find("body").find("script")
                    for tag in tags:
                        js_data = json.loads(str(tag).split("function()")[0][:-2].replace("window.__INITIAL_STATE__=", ""))
                        AnimeData["SeasonId"] = rs_data[0].split("ss")[1]
                        AnimeData["animeName"] = js_data["mediaInfo"]["title"]
                        AnimeData["introText"] = js_data["mediaInfo"]["evaluate"].replace("\n","")
                        AnimeData["score"] = js_data["mediaRating"]["score"] if "score" in js_data["mediaRating"].keys() else "-"
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
                        AnimeData.clear()

                        # 获取番剧下每一集的信息
                        try:
                            for MXinfo in js_data["epList"]:
                                AnimeMX["animeName"] = js_data["mediaInfo"]["title"]
                                AnimeMX["EpisodeName"] = MXinfo["index_title"]
                                AnimeMX["avSec"] = MXinfo["aid"]
                                AnimeMX["EpisodeNo"] = MXinfo["index"]
                                api_url = "https://api.bilibili.com/x/web-interface/archive/stat?aid={}".format(
                                    MXinfo["aid"])
                                js = json.loads(requests.get(api_url, headers=header, timeout=60).text)
                                if (js["code"] == 0):
                                    AnimeMX["play"] = 0 if js["data"]["view"] == "--" else js["data"]["view"]
                                    AnimeMX["danmu"] = js["data"]["danmaku"]
                                    AnimeMX["coin"] = js["data"]["coin"]
                                else:
                                    AnimeMX["play"] = -1
                                    AnimeMX["danmu"] = -1
                                    AnimeMX["coin"] = -1

                                db.insert_data("AnimeMX", AnimeMX)
                                AnimeMX.clear()
                        except Exception:
                            print(api_url)
                            DBHelper.Logger.write_log(api_url + "\n\n")
                except Exception:
                    print(rs_data[0])
                    DBHelper.Logger.write_log(rs_data[0] + "\n\n")
        print("结束一个线程")

if __name__ == '__main__':
    for i in range(0,50):
        ta = threading.Thread(target=get_Anime, args=())
        ta.start()


