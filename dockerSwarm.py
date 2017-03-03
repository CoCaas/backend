import docker
import json
client = docker.from_env()


#Ouverture du fichier de configuration
with open('config.json') as configFile:
    config = json.load(configFile)

#fonction pur quitter un swarm
def leaveSwarm():
    result =False
    try:
        result = client.swarm.leave(force =True)
    except docker.errors.APIError as err:
        print err
    return result

#fonction pour initier un swarm
def createSwarm():
    result = False
    try:
        result = client.swarm.init(advertise_addr=config['swarm']['interface_addr'])
    except docker.errors.APIError as err:
        print err
        leaveSwarm()
    return result

#obtenir le token du swarm
def getSwarmToken():
    DockerInfo = client.swarm.attrs
    try:
        return DockerInfo.get('JoinTokens').get('Worker')
    except AttributeError as err:
        return "Error: Vous devez initier un swarm"

#Obtenir l Id du swarm
def getSwarmId():
    DockerInfo = client.swarm.attrs
    try:
        return DockerInfo.get('ID')
    except AttributeError as err:
        return "Error: Vous devez initier un swarm"

#Obtenir la date de creation
def getSwarmCreatedDate():
    DockerInfo = client.swarm.attrs
    try:
        return DockerInfo.get('CreatedAt')
    except AttributeError as err:
        return "Error: Vous devez initier un swarm"
