import re
from datetime import datetime

def validateEmail(email):
    x = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    return re.match(x,email)
 

def validatePassword(password):
    specialSym="$@#%"
    val = True
      
    if len(password) < 8:
        print('length should be at least 8')
        val = False
          
    if not any(char.isdigit() for char in password):
        print('Password should have at least one numeral')
        val = False
          
    if not any(char.isupper() for char in password):
        print('Password should have at least one uppercase letter')
        val = False
          
    if not any(char.islower() for char in password):
        print('Password should have at least one lowercase letter')
        val = False
          
    if not any(char in specialSym for char in password):
        print('Password should have at least one of the symbols '+specialSym)
        val = False
    return val

def validateDob(dob):
    try:
        date_of_birth = datetime.strptime(dob, "%Y-%m-%d")
        return True
    except:
        return False
    
def isFloat(n):
    try:
        float(n)
        return True
    except ValueError:
        return False

