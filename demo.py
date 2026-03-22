'''
CHECK LOG AND EXCEPTION HANDLING
'''
from src.exception import MyException
try:
    result=1/0
except Exception as e:
    raise MyException("The error is just for testing purpose") 