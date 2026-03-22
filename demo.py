from src.exception import MyException
try:
    result=1/0
except Exception as e:
    MyException("This error for testing purpose")