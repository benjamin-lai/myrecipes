# !/usr/local/bin/python
# Python program to validate an Email
from re import search
 
# Function used to determine if provided email is valid or not
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
def validate_email(email):  
    if(search(regex,email)):
        return True

    else:
        return False

# reference: https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
