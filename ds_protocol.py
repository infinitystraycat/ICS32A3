# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# NAME
# EMAIL
# STUDENT ID

import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
# TODO: update this named tuple to use DSP protocol keys
DataTuple = namedtuple('DataTuple', ["join","post", "bio"])

def extract_json(json_msg:str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  
  TODO: replace the pseudo placeholder keys with actual DSP protocol keys
  '''
  
  try:
    json_obj = json.loads(json_msg)
    username = json_obj["response"]['username']
    password = json_obj["response"]["password"]
    token = json_obj["response"]["token"]
  except json.JSONDecodeError as e:
    print("Json cannot be decoded.")
    print(e)

  return DataTuple(username, password, token)
