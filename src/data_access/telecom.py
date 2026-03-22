from src.configuration.mongo_db_connection import MongoDBClient
from src.exception import MyException
from src.constants import COLLECTION_NAME
from typing import Optional
import pandas as pd
import numpy as np
class fetch_data:
    def __init__(self):
        try:
            self.connection=MongoDBClient()
        except Exception as e:
            raise MyException(e)
    def fetch_data_from_database(self,database_name:Optional[str]=None,collection_name=COLLECTION_NAME):
        try:
            if database_name is None:
                collection=self.connection.database[collection_name]
            else:
                collection=self.connection.client[database_name][collection_name]
            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df.drop(["_id"],axis=1,inplace=True)
            df.replace({"na":np.nan})
            return df
        except Exception as e:
            raise MyException(e)