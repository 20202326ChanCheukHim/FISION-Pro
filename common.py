
import pymongo
from pymongo import MongoClient
from flask import jsonify
import yaml

def read_config():
    with open("config.yaml") as stream:
        config = yaml.safe_load(stream)
    stream.close()
    return config

#=====================================================================================================================================
# Manage Mongodb client, create a connection object for the first time, then reuse the object
def mongodb_connect():
    config = read_config()
    # username = config["username"]
    # password = config["password"]
    # auth_source = config["auth_source"]
    mongo_db = "mongodb+srv://{}:{}@cluster0.6jkg6p8.mongodb.net/?authMechanism={}".format(config["mongodb_user"], config["mongodb_password"],config["auth_source"]) # Replace with your MongoDB server URL
    # mongo_db = "mongodb://{}:{}@{}:{}/?authMechanism=SCRAM-SHA-1&authSource=project".format(
    #             config["mongodb_user"], config["mongodb_password"], config["mongo_ip"], config["mongo_port"])
    myclient = pymongo.MongoClient(mongo_db)
    db = myclient["FitionSwift"]
    # collection = db["User_Inventory"]# Replace with the name of your collection
    return db



mongodb_connect()




# ==========================================================================================================
# Password Storage using one-way hash function
# Converting the password string to its binary representation, 
# manipulating the binary representation, 
# Performing modular exponentiation with specific parameters.



def simple_hash(password, pad=7):
    return pow(1279 ** 2, run_back(convert_bin(password, pad)) * 7654321, 11233333)



# e.g. pad = 7,    X = pad - noOfBit ,     add X leading zeros 
def convert_to_bit(n, pad):
    result = ""
    while n > 0:
        if n % 2 == 0:
            result = "0" + result
        else:
            result = "1" + result
        n = n // 2
    while len(result) < pad:
        result = "0" + result
    return result


def convert_bin(string, pad):
    output = ""
    for i in string:
        output = output + convert_to_bit(ord(i), pad)
    return output

def run_back(_):
    longbit = str(_[0])
    for i in range(len(_) - 1):
        longbit = longbit + str(_[i + 1])
    return int(longbit, 2)



