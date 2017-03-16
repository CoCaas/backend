import docker
import json
import os
import time



client = docker.from_env()
# A client for the Docker low-level API
# This is used for more fine-grained interaction with the Docker daemon
lowLvlClient = docker.APIClient(base_url='unix://var/run/docker.sock')


with open('config.json') as configFile:
    config = json.load(configFile)


"""
Leave any running Docker swarm
Return True if operation was successful, False otherwise
"""
def leaveSwarm():
    result =False
    try:
        result = client.swarm.leave(force =True)
    except docker.errors.APIError as err:
        result = None
    return result


"""
Create a swarm
Return True if operation was successful, otherwise leave the swarm and return False
"""
def createSwarm():
    result = False
    try:
        result = client.swarm.init(advertise_addr=config['swarm']['interface_addr'])
    except docker.errors.APIError as err:
        result = False
        leaveSwarm()
    return result


"""
Return the token used by workers to join the swarm, None if operation fails
"""
def getSwarmToken():
    DockerInfo = client.swarm.attrs
    try:
        return DockerInfo.get('JoinTokens').get('Worker')
    except:
        return None


"""
Return the swarm ID
"""
def getSwarmId():
    DockerInfo = client.swarm.attrs
    try:
        return DockerInfo.get('ID')
    except:
        return None


"""
Return the swarm's creation date, None if the operation fails
"""
def getSwarmCreatedDate():
    DockerInfo = client.swarm.attrs
    try:
        return DockerInfo.get('CreatedAt')
    except:
        return None


"""
Check if a swarm exists
Return True if it does, False if not or the operation fails
"""
def swarmExist():
    DockerInfo = client.swarm.attrs
    try:
        if DockerInfo.get('ID') is not None:
            return True
        else:
            return False
    except:
        return False


"""
Create a Docker service
Arguments:
    name: str - the service's name
    image: str - the service's image
    command: str - the command to run on the created service
    portsToExpose: list - a list of ports to expose on the service
Return the service ID if the service was successfully created, None otherwise
"""
def createService(name, image, command, portsToExpose):
    cmd = ""
    portArg = ""
    
    if command is not None :
        cmd = command
    
    for p in portsToExpose:
        portArg = portArg + ("-p ") + str(p) + " "
    portArg = portArg[:-1]
    args = "docker service create --name " + name + " --replicas 1 " + portArg + " " + image + " " + cmd
    proc = os.popen(args)
    serviceID = proc.readline().split('\n')[0]
    exitCode = proc.close()

    if exitCode is not None:
        return None
    else:
        return serviceID
    

"""
Get the published ports on a service.
These are the ports by which the service is accessible on the swarm.
Arguments:
    serviceID: str - the service ID
Return a list of ports (int), None if the operation fails.
"""
def getServicePublishedPorts(serviceID):
    time.sleep(3)
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


"""
Return a list of all the services on the swarm, None if the operation fails.
"""
def allServices():
    try:
        return client.services.list()
    except docker.errors.APIError as err:
        return None


"""
Print information about a service
Arguments:
    serviceId: str - the service ID
"""
def serviceInfos(serviceId):
    try:
        service = client.services.get(serviceId)
        print service.attrs
    except docker.errors.APIError as err:
        print err


"""
Get a sservice by its ID
Arguments:
    serviceId - str - the service ID
"""
def getServiceById(serviceId):
    try:
        return client.services.get(serviceId)
    except docker.errors.APIError as err:
        print err


"""
Delete a service by its ID
Arguments:
    serviceId: str - the service ID
Return True if deletion was successful, False otherwise
"""
def deleteServiceById(serviceId):
    try:
        service = client.services.get(serviceId)
        service.remove()
        return True
    except docker.errors.APIError as err:
        return False


"""
Deprecated
"""
def updateServicePort(serviceId,ListPort):
    try:
        service = client.services.get(serviceId)
        endpoint = docker.types.EndpointSpec(mode="vip",ports = ListPort)
        service.update(name = service.name,endpoint_spec = endpoint)
    except docker.errors.APIError as err:
        print err


"""
Return all runnings tasks belonging to a service
Arguments:
    serviceId: str - the service ID
Return a list of tasks dictionaries, None if operation fails.
"""
def getServiceTasks(serviceId):
    try:
        return getServiceById(serviceId).tasks({"desired-state" : "running"})
    except docker.errors.APIError as err:
        return None

"""
Get a swarm node by the node's ID
Arguments:
    nodeId: str - the node ID
Return a Node object, None if the operation fails
"""
def getNode(nodeId):
    try:
        return client.nodes.get(nodeId)
    except docker.errors.APIError as err:
        return None


"""
Get a node ID given its IP address
"""
def getNodeID(nodeIP):
    try:
        allNodes = client.nodes.list()
    except docker.errors.APIError:
        return None

    for node in allNodes:
        if node['Status']['Addr'] == nodeIP:
            return node['ID']
