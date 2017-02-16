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
#    ipadress = ''
#}

#container {
#   userId = ''
#   ProviderIP=''
#   serviceName =''
#}

#service {
#   name = ''
#    replicas = ''
#    bindPorts: [...]
#}

#client {
#   username : ''
#   services : [service names]
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

def getProviderCollection():
    return db['providers']

def getServicesCollection():
    return db['services']

def getClientCollection():
    return db['clients']

def insertUser(username,password):
    user = {
    "user" : username,
    "password" : password
    }
    userId = getUsersCollection().insert_one(user).inserted_id
    return userId

def insertProvider(userId, cpuLimit,memorylimit,storageLimit):
    provider = {
    "username" : userId,
    "cpuLimit" : cpuLimit,
    "memorylimit" : memorylimit,
    "storageLimit" : storageLimit
    }

    providerId = getProviderCollection().insert_one(provider).inserted_id

    return providerId

def insertContainer(username,providerIP,serviceName):
    container = {
        "username" : username,
        "providerIP" : providerIP,
        "serviceName" : serviceName
    }
    containerId = getContainersCollection().insert_one(container).insert_id
    return containerId
def insertService(serviceName,replicas, bindPorts):
    service = {
        "serviceName" =serviceName,
        "replicas" = replicas,
        "bindPorts" = bindPorts
    }
    serviceId = getServicesCollection().insert_one(service).insert_id

    return serviceId

def insertclient
