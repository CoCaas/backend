#importation pour la gestion des fichiers json
import json
from pymongo import MongoClient

#user {
#    username :''
#    password : ''
#}

#provider {
#    userId = ''
#    cpuLimit = ''
#    memorylimit= ''
#    storageLimit =''
#}

#container {
#
#}

#service {
#
#}

#client {
#
#}

def check_database_exist(client):
    trouve = 'false'
    for base in client.database_names():
        if base == client[config['database']['name']]:
            return trouve
    return trouve

with open('config.json') as configFile:
    config = json.load(configFile)

client = MongoClient(config['database']['host'],int(config['database']['port']))
db = client[config['database']['name']]

def getUsersCollection():
    return db['users']

def getContainersCollection():
    return db['containers']

def getServicesCollection():
    return db['services']

def getClientCollection():
    return db['clients']
