'''
from src.exception import MyException
from from_root import from_root 
import os
try:
    result=1/0
except Exception as e:
    MyException("This error for testing purpose")'''
'''import os
from from_root import from_root
from src.data_access.telecom import fetch_data 
fd = fetch_data()
data=fd.fetch_data_from_database()
mongo_db_test_dir_path = os.path.join(from_root(), "mongodb_test")
os.makedirs(mongo_db_test_dir_path, exist_ok=True)
mongo_db_test_file_path = os.path.join(mongo_db_test_dir_path, "mongo_test.txt")
with open(mongo_db_test_file_path, "w") as file:
    file.write(str(data))'''