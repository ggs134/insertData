#-*- coding: utf-8 -*-

import pymongo
import json
import requests
import get24mined
import time

mongoClient = pymongo.MongoClient("127.0.0.1",27017)
mongoDB = mongoClient.di

miners_farm1 = [1,2,3,4,5,6,8,14]
miners_farm2 = [9,10,11,12]
miners_farm3 = [i for i in range(15,39) if i is not 37 ]
miner_list = miners_farm1 + miners_farm2 + miners_farm3

data1 = []
data2 = []
for i in miners_farm1:
  try:
    res = mongoDB["miner"+str(i)].find(sort=[("_id",-1)]).limit(1).next()
    # print res
    # print res["hashrate"]
    # rs = {"hash":res["hashrate"]+res["hashrateC"], "temp":res["gpuTemprature"], "fanspeed":res["fanspeed"]}
    # print res
    temp = [int(j) for j in res["gpuTemperature"].strip("[]").split(",")]
    averageTemp = sum(temp) / float(len(temp))
    boot_hour = (time.time() - float(res["bootTime"]))/3600
    rs = {"boot_hour":boot_hour, "username": res["username"], "hash":(res["hashrate"]+res["hashrateC"])/1000.0, "temp":temp, "average_temp": averageTemp, "gpu_num":len(temp)}
    # print rs
    data1.append(rs)
  except Exception as e:
    print e

for i in miners_farm3:
  try:
    res = mongoDB["miner"+str(i)].find(sort=[("_id",-1)]).limit(1).next()
    # print res
    # print res["hashrate"]
    # rs = {"hash":res["hashrate"]+res["hashrateC"], "temp":res["gpuTemprature"], "fanspeed":res["fanspeed"]}
    # print res
    temp = [int(j) for j in res["gpuTemperature"].strip("[]").split(",")]
    averageTemp = sum(temp) / float(len(temp))
    boot_hour = (time.time() - float(res["bootTime"]))/3600
    rs = {"boot_hour":boot_hour, "username": res["username"], "hash":(res["hashrate"]+res["hashrateC"])/1000.0, "temp":temp, "average_temp": averageTemp, "gpu_num":len(temp)}
    # print rs
    data2.append(rs)
  except Exception as e:
    print e

total_data = data1 + data2
average_list1 = [i["average_temp"] for i in data1 ]
average_list2 = [ i["average_temp"] for i in data2 ]
total_average_list = average_list1 + average_list2
total_average = sum(total_average_list) / float(len(total_average_list))
average1 = sum(average_list1) / float(len(average_list1))
average2 = sum(average_list2) / float(len(average_list2))

max_temp = max(max([i["temp"] for i in total_data]))
max_list = [i["username"] for i in total_data if max_temp in i["temp"]]
# print total_data
# print total_data[0]["gpu_num"]
total_gpu_num = sum([int(i["gpu_num"]) for i in total_data])
hash_per_gpu = sum([int(i["hash"]) for i in total_data]) / float(total_gpu_num)

#profit related info
minedETH = get24mined.getMinedEther()
minedETC = get24mined.getMinedEtc()
prices = get24mined.priceTicker()

#weather realted info
weather = get24mined.getWeatherInfo()

profit = {"ETH_price": prices["eth"], "ETC_price":prices["etc"], "BTC_price":prices["btc"], "minedETH":minedETH, "minedETC":minedETC}

statistics = {"total_average":total_average, "average1":average1, "average2":average2, \
"max_list":max_list , "max_temp": max_temp, "total_gpu_num":total_gpu_num, "hash_per_gpu": hash_per_gpu}

mongoDB["statistics"].insert(statistics)
mongoDB["profit"].insert(profit)
mongoDB["weather"].insert(weather)
mongoDB["statusData1"].insert({"data": data1})
mongoDB["statusData2"].insert({"data": data2})
