from re import fullmatch
from numpy import number
import regex as re
def textget(inp):
        text= str(inp)
        email_pattern= r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        car_no_pattern= r'^[A-Za-z]{2}[ -][0-9]{1,2}(?: [A-Za-z])?(?: [A-Za-z]*)? [0-9]{4}$'
        number_pattern= r'^[6-9]\d{9}$'
        if (re.fullmatch(email_pattern,text)):
            print("email true")
        elif (re.fullmatch(car_no_pattern,text)):
            print("car true")
        elif re.fullmatch(number_pattern,text):
            print("numnber true")
        else:
            print("not true")

inp= input("Enter a string: ")
textget(inp)