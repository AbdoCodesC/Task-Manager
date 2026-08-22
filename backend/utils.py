import re

def valid_data(first, last, email, password):
  return first and len(first) > 3 and last and len(last) > 3 and re.match('r"^\S+@\S+\.\S+$"', email) and re.match(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", password)