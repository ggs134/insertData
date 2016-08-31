import requests
import json
import pymongo
import time

client = pymongo.MongoClient('127.0.0.1',27017)
DB = client["MiningPoolHub"]

def getDataAndInsert():
  while True:
    response = requests.get("http://ethereum.miningpoolhub.com/index.php?page=api&action=getuserworkers&api_key=a8c9f5ea1a4045f6809c9a47c4746f5ae4aa5e136bf96ec0ce4223734c96a128")
    response2 = requests.get("http://ethereum-classic.miningpoolhub.com/index.php?page=api&action=getuserworkers&api_key=a8c9f5ea1a4045f6809c9a47c4746f5ae4aa5e136bf96ec0ce4223734c96a128")
    json_response = response.json()
    json_response2 = response2.json()
    data = json_response["getuserworkers"]["data"]
    data2 = json_response2["getuserworkers"]["data"]
    DB["eth"].insert({"data":[data]})
    DB["etc"].insert({"data":[data2]})
    time.sleep(60)

if __name__ == "__main__":
  getDataAndInsert()  
