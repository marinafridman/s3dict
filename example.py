#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
example code for testing and using class S3Dict, a class which allows you to 
access s3 with a dict-like interface
@author: marina
"""
from s3dict import S3Dict
import csv

# set AWS access credentials from file
with open('credentials.csv', newline='') as f:
    reader = csv.reader(f)
    creds = list(reader)
    
MY_BUCKET = creds[0][0]
ACCESS_KEY_ID = creds[1][0]
ACCESS_SECRET_KEY = creds[2][0]

# instantiate class
myS3dict = S3Dict(MY_BUCKET, ACCESS_KEY_ID, ACCESS_SECRET_KEY)

# add key-value pairs to bucket
key_value_pairs = [("apple",1),("acorn",2),("bob",3)]
for entry in key_value_pairs:
    myS3dict.put(entry[0],entry[1].to_bytes(8, byteorder='little'))
    
# return the value associated to key "acorn"
val = myS3dict.get("acorn")
print(f" Key: acorn; Value: {val}")

# retrieve all keys in bucket
keys = myS3dict.keys()
print("All keys currently in bucket: " + "; ".join(keys))

# retrieve all keys in bucket that start with the letter 'a'
keys_a = myS3dict.keys('a')
print("All keys in bucket starting with the letter a: " + "; ".join(keys_a))

# retrieve all keys-value pairs in bucket
kvp = myS3dict.items()
print("All key-value pairs in bucket: ")
print(kvp)

# retrieve all keys in bucket that start with the letter 'b'
kvp_b = myS3dict.items('b')
print("All key-value pairs in bucket: ")
print(kvp_b)

# remove the value with key "apple" and return it
popped_val = myS3dict.pop('apple')
print(f"{popped_val} has been removed from the bucket")

# retrieve all remaining keys in bucket
rem_keys = myS3dict.keys()
print("Remaining keys include: " + "; ".join(rem_keys))

# remove remaining keys from bucket
for key in rem_keys:
    myS3dict.pop(key)