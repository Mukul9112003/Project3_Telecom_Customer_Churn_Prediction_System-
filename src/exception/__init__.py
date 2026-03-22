import os
import sys
from datetime import date
from src.components.logger import logging
def get_message_details(error):
    _,_,tb_exc=sys.exc_info()
    if tb_exc is None:
        return "not error"
    else:
        file_name=tb_exc.tb_frame.f_code.co_filename
        line_number=tb_exc.tb_lineno
        message=f"The error in file {file_name} at line number {line_number} {error}"
        logging.info(f"{date.today()} : {message}")
        return message
class MyException(Exception):
    def __init__(self,error):
        super().__init__(error)
        self.message=get_message_details(error)
        logging.info("Exception work well")
    def __str__(self):
        return self.message