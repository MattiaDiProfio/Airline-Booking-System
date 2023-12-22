import re

# Check for valid email format 
def email_is_valid(email):
    pattern = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")
    match = pattern.match(email)
    return True if match else False

# Check for valid password format
def password_is_valid(password):
    pattern = re.compile(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!?@])[\w\d@!?]{5,30}$")
    match = pattern.match(password)
    return True if match else False

# Check for valid username format
def username_is_valid(username):
    pattern = re.compile(r"^[a-zA-Z0-9]{5,30}$")
    match = pattern.match(username)
    return True if match else False

# Check for valid fullname format
def fullname_is_valid(fullname):
    pattern = re.compile(r"^[a-zA-Z ]{5,30}$")
    match = pattern.match(fullname)
    return True if match else False