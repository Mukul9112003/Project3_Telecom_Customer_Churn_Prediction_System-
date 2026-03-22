import logging
import os
from from_root import from_root
from datetime import datetime
from logging.handlers import SMTPHandler,RotatingFileHandler
FILE_DIR="log"
FILE_NAME=f"{datetime.now().strftime('%d_%m_%Y_%M_%S')}.log"
MAXBYTES=3*1024*1024
BACKUPCOUNT=5
file_dir_path=os.path.join(from_root(),FILE_DIR)
os.makedirs(file_dir_path,exist_ok=True)
file_name=os.path.join(file_dir_path,FILE_NAME)
def config_logging():
    logger=logging.getLogger()
    formatter=logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s] [%(message)s]")
    file_handler=RotatingFileHandler(file_name,maxBytes=MAXBYTES,backupCount=BACKUPCOUNT)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    console_handler=logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
config_logging()