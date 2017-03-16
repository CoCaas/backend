from pymongo import MongoClient
import json


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

def getSwarmCollection():
    return db['swarm']


def insertUser(username,password,firstname,lastname):
    user = {
        "user" : username,
        "password" : password,
        "firstname" : firstname,
        "lastname" : lastname
    }
    userId = getUsersCollection().insert_one(user).inserted_id
    return userId


def insertProvider(userId, cpuMachine, memoryMachine, storageMachine, cpuLimit, memorylimit, storageLimit, nodeIP):
    provider = {
        "userId" : userId,
        "cpuMachine" : cpuMachine,
        "memoryMachine" : memoryMachine,
        "storageMachine" : storageMachine,
        "cpuLimit" : cpuLimit,
        "memorylimit" : memorylimit,
        "storageLimit" : storageLimit,
        "cpuCurrent" : "0",
        "memoryCurrent" : "0",
        "storageCurrent" : "0",
        "nodeIP"      : nodeIP,
        "nodeID"      : ""
    }

    providerId = getProviderCollection().insert_one(provider).inserted_id

    return providerId


def insertService(userId,replicas,serviceName):
    service = {
        "userId" : userId,
        "replicas" : replicas,
        "serviceName" : serviceName
    }
    ServiceDBId = getServicesCollection().insert_one(service).inserted_id
    return ServiceDBId


def insertContainer(containerId,serviceId,ContainerName,image,cmd, bindPorts):
    splittedName = ContainerName.split('-')
    num = int(splittedName[len(splittedName) - 1])
    container = {
        "containerId": containerId,
        "ContainerName" : ContainerName,
        "ContainerNumber" : num,
        "image" : image,
        "cmd" : cmd,
        "bindPorts" : bindPorts,
        "serviceId" : serviceId
    }
    containerId = getContainersCollection().insert_one(container).inserted_id
    return containerId


def insertClient(username,services):
    client = {
        "username" : username,
        "services" : services
    }
    clientId = getClientCollection().insert_one(client).inserted_id
    return clientId


def insertSwarm(id,token,createdDate):
    swarm = {
        "id" : id,
        "token" : token,
        "createdDate" : createdDate
    }
    numResult = getUsersCollection().count()
    swarmId = 0
    if numResult == 0:
        swarmId = getSwarmCollection().insert_one(swarm).inserted_id
    else:
        # only one swarm can exist
        getSwarmCollection().delete_many({})
        swarmId = getSwarmCollection().insert_one(swarm).inserted_id
    return swarmId
