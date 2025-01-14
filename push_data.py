import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca = certifi.where() # trusted certificate authorities

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

# ETL Pipeline
class NetworkDataExtract():
    def __init__(self):
        try:

            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def cv_to_json_convert(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records = list(json.loads(data.T.to_json()).values()) # when converting in json, it should be in key:value pairs, here we are doing that
            #this key:value format is also supported by mongodb
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def insert_data_mongodb(self,records,database,collection):
        # collection is like a table in sql
        #we have to create everytime database in mongodb 
        try:
            self.database = database  #we can do this initialization in constructor __init__ as well , but here im doing on runtime , so this is also correct

            self.collection = collection
            self.records = records
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL,
                                                    socketTimeoutMS=90000,
                                                    connectTimeoutMS=9000    )
            # pymongo url connects python to mongodb

            self.database = self.mongo_client[self.database]
            self.collection = self.database[collection]
            self.collection.insert_many(self.records)
             
            return (len(self.records))





        except Exception as e:
            raise NetworkSecurityException(e,sys)

if __name__ == '__main__':
    FILE_PATH = "Network_Data/phisingData.csv"
    DATABASE = "ALI_AI"
    collection = "NetworkData"
    networkobj = NetworkDataExtract()
    records = networkobj.cv_to_json_convert(file_path=FILE_PATH)
    print(records)
    no_of_records = networkobj.insert_data_mongodb(records,DATABASE,collection)
    print(no_of_records)
