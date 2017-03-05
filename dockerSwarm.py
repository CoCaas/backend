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
#verifie si un swarm exixt sur la machine
def swarmExist():
    DockerInfo = client.swarm.attrs
    try:
        DockerInfo.get('ID')
        return True
    except AttributeError as err:
        return False
#cree un service
def createService(nom, imagee, commande):
    try:
        service = client.services.create(image = imagee, name=nom,command=commande)
        return service.id
    except docker.errors.APIError as err:
        print err
        return None
#renvoie une lise d objet service
def allServices():
    try:
        return client.services.list()
    except docker.errors.APIError as err:
        print err

#informations about the service
def serviceInfos(serviceId):
    try:
        service = client.services.get(serviceId)
        print service.attrs
    except docker.errors.APIError as err:
        print err

#delete a service knowing he's id
def deleteServiceById(serviceId):
    try:
        service = client.services.get(serviceId)
        service.remove()
        return True
    except docker.errors.APIError as err:
        print err
        return False
#update the ports of a service
#the list is in a format {80:90,100:20}
def updateServicePort(serviceId,ListPort):
    try:
        service = client.services.get(serviceId)
        endpoint = docker.types.EndpointSpec(mode="vip",ports = ListPort)
        service.update(name = service.name,endpoint_spec = endpoint)
    except docker.errors.APIError as err:
        print err
