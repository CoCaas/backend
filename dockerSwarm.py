import docker
import subprocess
import json


client = docker.from_env()
lowLvlClient = docker.APIClient(base_url='unix://var/run/docker.sock')


#Ouverture du fichier de configuration
with open('config.json') as configFile:
    config = json.load(configFile)

#fonction pur quitter un swarm
def leaveSwarm():
    result =False
    try:
        result = client.swarm.leave(force =True)
    except docker.errors.APIError as err:
        result = None
    return result

#fonction pour initier un swarm
def createSwarm():
    result = False
    try:
        result = client.swarm.init(advertise_addr=config['swarm']['interface_addr'])
    except docker.errors.APIError as err:
        result = False
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

        if DockerInfo.get('ID') is not None:
            return True
        else:
            return False
    except AttributeError as err:
        return False
#cree un service
def createService(nom, imagee, commande, portsToExpose):
    #specPorts = []
    #for p in portsToExpose:
        #specPorts.append({None: p})
    #endpointSpec = docker.types.EndpointSpec(mode = 'vip', ports = specPorts)
    #try:
        #service = client.services.create(image = imagee, name = nom, command = commande, endpoint_spec = endpointSpec)
    # portArg = []
    # for p in portsToExpose:
    #     portArg.append("-p")
    #     portArg.append(p)
    
    # #args = "service create --name " + nom + " --replicas 1 " + portArg + " " + imagee + " " +commandArg
    # args = ['docker', 'service', 'create', '--name', nom, '--replicas', '1']
    # args = args + portArg
    # args.append(imagee)
    # if commande is not None
    #     args.append(commande)
    # process = subprocess.Popen(args = args,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
    # outdata, outerr = process.communicate()
    # if outerr is not None:
    #     return None
    # return outdata
        #return service.id
    #except docker.errors.APIError as err:
        #return None
    specPorts = []
    for p in portsToExpose:
        specPorts.append({p: None})
    endpointSpec = docker.types.EndpointSpec(mode = 'vip', ports = specPorts)
    try:
        service = client.services.create(image = imagee, name = nom, command = commande, endpoint_spec = endpointSpec)
    except:
        return None
    return service.id

def getServicePublishedPorts(serviceID):
    service = None
    try:
        service = client.services.get(serviceID)    
    except:
        return None

    ports = []
    portsArray = service.attrs['Endpoint']['Ports']
    for p in portsArray:
        ports.append(int(p['PublishedPort']))
    return ports

#renvoie une lise d objet service
def allServices():
    try:
        return client.services.list()
    except docker.errors.APIError as err:
        return None

#informations about the service
def serviceInfos(serviceId):
    try:
        service = client.services.get(serviceId)
        print service.attrs
    except docker.errors.APIError as err:
        print err

def getServiceById(serviceId):
    try:
        return client.services.get(serviceId)
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

def getServiceTasks(serviceId):
    try:
        return getServiceById(serviceId).tasks({"desired-state" : "running"})
    except docker.errors.APIError as err:
        return None

def getNode(nodeId):
    try:
        return client.nodes.get(nodeId)
    except docker.errors.APIError as err:
        return None
