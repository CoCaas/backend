#we will be using Flask for this api
#why using flask?
#Flask is a microframework for Python based on Werkzeug, a WSGI utility library.

#Flask is a good choice for a REST API because it is:

    #Written in Python (that can be an advantage);
    #Simple to use;
    #Flexible;
    #Multiple good deployment options;
    #RESTful request dispatching

#install flask : sudo pip install flask
#pip install passlib
#pip install Flask-HTTPAuth
#pip install pymongo
#pip install docker
from flask import Flask, url_for, Response, jsonify, session, make_response,request, send_from_directory
from passlib.apps import custom_app_context as pwd_context
from flask_httpauth import HTTPBasicAuth
import json
import pymongo
import managerDB
import dockerSwarm
app =Flask(__name__, static_url_path='')
app.secret_key = 'cocaas2017'
auth = HTTPBasicAuth()
SERVER_PORT = 80

@app.route('/')
def send_welcome_page():
    return send_from_directory('web/html', 'index.html')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('web/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('web/css', path)

@app.route('/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory('web/fonts', path)

@app.route('/html/<path:path>')
def send_html(path):
    return send_from_directory('web/html', path)


#Permet d enregistrer provider
#nbCPU : le nombre de cpu a alouer
#nbMemory : le nombre de memoire a alouer
#nbStockage: le nombre de disque a alouer
@app.route('/Provider/new', methods = ['POST'])
def api_setProvider():

    username = request.get_json(force=True)['username']
    password = request.get_json(force=True)['password']

    cpuLimit = request.get_json(force=True)['cpuLimit']
    memorylimit = request.get_json(force=True)['memorylimit']
    storageLimit = request.get_json(force=True)['storageLimit']

    cpuMachine = request.get_json(force=True)['cpuMachine']
    memoryMachine = request.get_json(force=True)['memoryMachine']
    storageMachine = request.get_json(force=True)['storageMachine']

    nodeIP   = request.remote_addr

    if nbCPU is None or nbMemory is None or nbStockage is None or username is None or password is None or nodeIP is None:
        return  make_response(jsonify({'error': 'un argument est manquant'}), 403)

    numResult = managerDB.getUsersCollection().find({"user" : username}).count()
    if numResult == 0:
        return make_response(jsonify({'error': 'cet utilisateur n existe pas'}), 403)
    else:
        result =  managerDB.getUsersCollection().find_one({"user" : username})
        if  result is not None:
            if pwd_context.verify(password, result['password']):
                providerResult = managerDB.getProviderCollection().find_one({"userId" : username})
                if providerResult is None:
                    managerDB.insertProvider(username,cpuMachine,memoryMachine,storageMachine, cpuLimit, memorylimit, storageLimit,nodeIP)
                else:
                    managerDB.getProviderCollection().update( { "userId": username},  { "$set": {"nodeIP" : nodeIP}})
                return make_response(jsonify({'nbCPU': nbCPU, 'nbMemory': nbMemory, 'nbStockage' :nbStockage, 'nodeIP' : nodeIP }), 202)
            else:
                return make_response(jsonify({'error': 'Le mot de passe est incorrect'}), 403)
        else:
            return make_response(jsonify({'error': 'Utilisateur non trouver'}), 403)

@app.route('/Provider/update', methods = ['POST'])
def api_updateProvider():
    cpuCurrent = request.get_json(force=True)['cpuCurrent']
    memoryCurrent = request.get_json(force=True)['memoryCurrent']
    storageCurrent = request.get_json(force=True)['storageCurrent']
    username = request.get_json(force=True)['username']
    password = request.get_json(force=True)['password']

    if cpuCurrent is None or memoryCurrent is None or storageCurrent is None or username is None or password is None:
        return  make_response(jsonify({'error': 'un argument est manquant'}), 403)

    numResult = managerDB.getUsersCollection().find({"user" : username}).count()
    if numResult == 0:
        return make_response(jsonify({'error': 'cet utilisateur n existe pas'}), 403)
    else:
        result =  managerDB.getUsersCollection().find_one({"user" : username})
        if  result is not None:
            if pwd_context.verify(password, result['password']):
                managerDB.getProviderCollection().update( { "userId": username},  { "$set": {"cpuCurrent" : cpuCurrent, "memoryCurrent" : memoryCurrent, "storageCurrent" : storageCurrent}})
                return make_response(jsonify({'message': 'reussi' }), 202)
            else:
                return make_response(jsonify({'error': 'Le mot de passe est incorrect'}), 403)
        else:
            return make_response(jsonify({'error': 'Utilisateur non trouver'}), 403)


@app.route('/Provider', methods = ['GET'])
def api_getProvider():
    if 'username' in session:
        result = managerDB.getProviderCollection().find_one( {"userId" : session['username']} )
        user = managerDB.getUsersCollection().find_one( {"user" : session['username']} )
        if result is None:
            return  make_response(jsonify({'message': 'Vous n avez pas soumis de provider'}), 403)
        else:
            if user is None:
                make_response(jsonify({'message': 'Ce nom d utilisateur n existe pas'}), 403)
            else:
                Jsondata = {}
                Jsondata['cpuLimit'] = result['cpuLimit']
                Jsondata['memorylimit'] = result['memorylimit']
                Jsondata['storageLimit'] = result['storageLimit']
                Jsondata['memoryCurrent'] = result['memoryCurrent']
                Jsondata['cpuCurrent'] = result['cpuCurrent']
                Jsondata['storageCurrent'] = result['storageCurrent']
                Jsondata['cpuMachine'] = result['cpuMachine']
                Jsondata['memoryMachine'] = result['memoryMachine']
                Jsondata['storageMachine'] = result['storageMachine']
                Jsondata['firstname'] = user['firstname']
                Jsondata['lastname'] = user['lastname']
                return  make_response(jsonify(Jsondata), 202)
    else:
        return  make_response ( jsonify({'error': 'veuillez vous connecter svp'}), 403 )

#permet de supprimer un provider
@app.route('/Provider/delete',methods =['POST'])
def api_deleteProvider():
    username = request.get_json(force=True)['username']
    password = request.get_json(force=True)['password']

    if username is None or password is None:
        return  make_response(jsonify({'error': 'un argument est manquant'}), 403)

    numResult = managerDB.getUsersCollection().find({"user" : username}).count()
    if numResult == 0:
        return make_response(jsonify({'error': 'cet utilisateur n existe pas'}), 403)
    else:
        result =  managerDB.getUsersCollection().find_one({"user" : username})
        if pwd_context.verify(password, result['password']):
            managerDB.getProviderCollection().delete_many({'username' :username})
            return make_response(jsonify({'message': 'reussi'}), 202)
        else:
            return make_response(jsonify({'error': 'Le mot de passe est incorrect'}), 403)

#Permet de verifier que un utilisateur existe
@app.route('/User/check',methods =['POST'])
def api_checkUser():
    username = request.get_json(force=True)['username']
    password = request.get_json(force=True)['password']

    if username is None or password is None:
        return  make_response(jsonify({'error': 'un argument est manquant'}), 403)

    numResult = managerDB.getUsersCollection().find({"user" : username}).count()
    if numResult == 0:
        return make_response(jsonify({'error': 'cet utilisateur n existe pas'}), 403)
    else:
        result =  managerDB.getUsersCollection().find_one({"user" : username})
        if pwd_context.verify(password, result['password']):
            return make_response(jsonify({'message': 'Utilisateur existe'}), 202)
        else:
            return make_response(jsonify({'error': 'Le mot de passe est incorrect'}), 403)


#permet de se connecter
#username: le nom d'utilisateur
#hash : le mot de passe de l'utilisateur
@app.route('/User/login', methods = ['POST'])
def api_connect():
    username = request.get_json(force=True)['username']
    password = request.get_json(force=True)['password']
    if username is None or password is None:
        return make_response(jsonify({'error': 'Pas de mot de passe ou de nom d utilisateur'}), 403)
    if 'username' in session:
        return  make_response(jsonify({'error': 'vous etes deja connecte'}), 202)
    else:
        numResult = managerDB.getUsersCollection().find({"user" : username}).count()
        if numResult == 0:
            return make_response(jsonify({'error': 'cet utilisateur n existe pas'}), 403)
        else:
            result =  managerDB.getUsersCollection().find_one({"user" : username})
            if pwd_context.verify(password, result['password']):
                session['username'] = username
                rep = make_response(jsonify({'success': 'vous etes connecte', 'firstname':result['firstname'], 'lastname' : result['lastname']}), 202)
                return rep
            else:
                return make_response(jsonify({'error': 'Le mot de passe est incorrect'}), 403)

#permet de se deconnecter
@app.route('/User/logout', methods = ['POST'])
def api_deconnect():
    if 'username' in session:
        session.pop('username', None)
        return  make_response(jsonify({'sucess': 'vous vous etes bien deconnecte'}), 202)
    else:
        return  make_response(jsonify({'error': 'vous n etes  pas connecte'}), 403)

#permet de modifier le mot de passe de l utilisateur
@app.route('/User/modifypassword', methods = ['POST'])
def api_modify_user_password():
    if 'username' in session:
        newpassword = request.get_json(force=True)['newpassword']
        oldpassword = request.get_json(force=True)['oldpassword']
        result =  managerDB.getUsersCollection().find_one({"user" : session['username']})
        if pwd_context.verify(oldpassword, result['password']):
            hash1 = pwd_context.encrypt(newpassword)
            result =  managerDB.getUsersCollection().update( { "user": session['username']},  { "$set": {"password" : hash1}}   )
            rep = make_response(jsonify({'success': 'Votre mot de passe a ete modifier'}), 202)
            return rep
        else:
            return make_response(jsonify({'error': 'Ancien mot de passe incorrect'}), 403)
    else:
        return  make_response(jsonify({'error': 'Vous devez etre connecter'}), 403)


#permet d'ajouter un nouvel utilisateur
#username: le nom d'utilisateur
#hash : le mot de passe de l'utilisateur
@app.route('/User/new', methods = ['POST'])
def api_addUser():
    username = request.get_json(force=True)['username']
    password = request.get_json(force=True)['password']
    lastname = request.get_json(force=True)['lastname']
    firstname = request.get_json(force=True)['firstname']
    if username is None or password is None:
        return make_response(jsonify({'error': 'Pas de mot de passe ou de nom d utilisateur'}), 403)

    numResult = managerDB.getUsersCollection().find({"user" : username}).count()
    if numResult == 0:
        hash = pwd_context.encrypt(password)
        managerDB.insertUser(username,hash,firstname,lastname)
        session['username'] = username
        return  make_response(jsonify({'sucess': 'Utilisateur bien ajouter', 'firstname':firstname, 'lastname' : lastname}), 202)
    else:
        return  make_response(jsonify({'error': 'cet utilisateur existe deja'}), 403)


#Permet d inserer un nouveau service
#name : le nom du services
#nbReplicas : le nombre de replicas
#image : le nom de l image
#commande : la commande a executer
#bindPorts : la liste des ports a binder > une liste d entiers > [122,455,789,445]
@app.route('/Services/new',methods = ['POST'])
def api_addService():
    name = request.get_json(force=True)['name']
    nbReplicas = request.get_json(force=True)['nbReplicas']
    image = request.get_json(force=True)['image']
    commande = request.get_json(force=True)['commande']
    bindPorts = request.get_json(force=True)['bindPorts']

    if name is None or nbReplicas is None or image is None or bindPorts is None:
        return make_response(jsonify({'error': 'Un des arguments est manquant'}), 403)

    if 'username' in session:
        if dockerSwarm.swarmExist() == True:
            username = session['username']
            serviceGlobalName = name

            result =  managerDB.getServicesCollection().find({"userId" : session['username'], "serviceName" : name})

            if result.count() == 0:
                containerId = managerDB.insertService(username,nbReplicas,name)
                for num in range(1,int(nbReplicas) + 1):
                    ServiceName =username+"-"+ serviceGlobalName+"-"+str(num)
                    serviceId = dockerSwarm.createService(ServiceName,image,commande)
                    if serviceId is not None:
                        managerDB.insertContainer(containerId,serviceId,ServiceName,image,commande,bindPorts)
                verifie = managerDB.getContainersCollection().find({"containerId" : containerId})
                if verifie is None:
                    managerDB.getServicesCollection().delete_one({"serviceName" : name})
            else:
                return make_response(jsonify({'error': 'Ce nom de service est daja pris.'}), 403)
        else:
            return make_response(jsonify({'error': 'Docker swar n as pas demarrer'}), 403)
        return  make_response(jsonify({'message': 'reussi'}), 202)
    else:
        return  make_response(jsonify({'error': 'veuillez vous connecter svp'}), 403)
    return temp

#Cette fonction renvoie la liste des services
#ip
#port
#nom de la machine
#nom des containers
#image
#commande
#date de creation
#status
@app.route('/User/services', methods =['GET'])
def getAllUserServices():
    if 'username' in session:
        if dockerSwarm.swarmExist() == True:
            result = managerDB.getServicesCollection().find({"userId" : session['username']})
            print result
            if result.count() == 0:
                return make_response(jsonify({}), 202)
            else:
                JsondataGlobal =[]
                for numService in range(0, int(result.count())):
                    containerId = result[numService]['_id']
                    containersBD = managerDB.getContainersCollection().find({"containerId" : containerId })
                    JsonService ={}
                    JsonService['serviceName'] = result[numService]['serviceName']
                    JsonService['replicas'] =  result[numService]['replicas']
                    JsonService['services'] =  []
                    for num in range(0,int(containersBD.count())):
                        serviceId = containersBD[num]['serviceId']
                        if serviceId is not None:
                            service = dockerSwarm.getServiceById(serviceId)
                            if service is not None:
                                Jsondata = {}
                                serviceInfo = service.attrs
                                tasks = dockerSwarm.getServiceTasks(serviceId)
                                try:
                                    Jsondata['nodeId'] = tasks[0]['NodeID']
                                    nodeInfo = dockerSwarm.getNode(tasks[0]['NodeID']).attrs

                                    Jsondata['ports'] = containersBD[num]['bindPorts']
                                    Jsondata['nomMachine'] = nodeInfo['Description']['Hostname']
                                    Jsondata['ipMachine'] = nodeInfo['Status']['Addr']
                                    Jsondata['NomService'] = serviceInfo['Spec']['Name']
                                    Jsondata['nomImage'] = serviceInfo['Spec']['TaskTemplate']['ContainerSpec']['Image']
                                    Jsondata['commande'] = serviceInfo['Spec']['TaskTemplate']['ContainerSpec']['Command']
                                    Jsondata['datecreation'] = serviceInfo['CreatedAt']
                                    Jsondata['status'] = serviceInfo['UpdateStatus']

                                except IndexError as err:
                                    print err
                                JsonService['services'].append(Jsondata)
                    JsondataGlobal.append(JsonService)
                infoJson = json.dumps(JsondataGlobal)
                return make_response(jsonify({'services': JsondataGlobal}), 202)
        else:
            return make_response(jsonify({'error': 'Docker swar n as pas demarrer'}), 403)
        return  make_response(jsonify({'message': 'reussi'}), 202)
    else:
        return  make_response(jsonify({'error': 'veuillez vous connecter svp'}), 403)



# Scale a service
# JSON params: serviceName, replicas
@app.route('/Services/scale', methods = ['POST'])
def api_scaleService():
    serviceName = request.get_json(force = True)['serviceName']

    if serviceName is None:
        return make_response(jsonify({'error': 'No service name provided'}), 403)


    # fail if client is not authenticated
    if 'username' not in session:
        return make_response(jsonify({'error': 'User not authenticated'}), 403)

    newReplicas = 0
    try:
        newReplicas = int(request.get_json(force = True)['replicas'])
        if newReplicas <= 0:
            raise ValueError('Invalid number of replicas')
    except ValueError:
        return make_response(jsonify({'error': 'Invalid number of replicas'}), 403)

    username = session['username']
    serv = managerDB.getServicesCollection().find_one({'userId': username, 'serviceName': serviceName})

    if serv is None:
        return make_response(jsonify({'error': 'Could not find the service ' + serviceName}), 403)

    oldReplicas = int(serv['replicas'])
    if newReplicas < oldReplicas:
        # delete oldReplicas - newReplicas containers
        nbDeleted = 0
        for i in range(oldReplicas - newReplicas):
            cntnr = managerDB.getContainersCollection().find_one({'containerId': serv['_id']})
            dockerServiceID = cntnr['serviceId']
            if dockerSwarm.deleteServiceById(dockerServiceID):
                managerDB.getContainersCollection().delete_one({'serviceId': dockerServiceID})
                nbDeleted += 1
        managerDB.getServicesCollection().update_one({'_id': serv['_id']}, {'$set': {'replicas': oldReplicas - nbDeleted}})

    if newReplicas > oldReplicas:
        # add newReplicas - oldReplicas containers
        nbAdded = 0
        cursr = managerDB.getContainersCollection().find({'containerId': serv['_id']}).sort('ContainerNumber', pymongo.DESCENDING).limit(1)
        cntnrWithMaxCounter = None
        for c in cursr:
            cntnrWithMaxCounter = c
        splittedCntnrName = cntnrWithMaxCounter['ContainerName'].split('-')
        maxCounter = int(splittedCntnrName[len(splittedCntnrName) - 1])
        for i in range(newReplicas - oldReplicas):
            someCntnr = managerDB.getContainersCollection().find_one({'containerId': serv['_id']})
            currCounter = maxCounter + i + 1
            newServiceName = username + '-' + serviceName + '-' + str(currCounter)
            dockerServiceID = dockerSwarm.createService(newServiceName, someCntnr['image'], someCntnr['cmd'])
            if dockerServiceID is not None:
                managerDB.insertContainer(serv['_id'], dockerServiceID, username + '-' + serviceName + '-' + str(currCounter),
                    someCntnr['image'], someCntnr['cmd'], someCntnr['bindPorts'])
                nbAdded += 1
        managerDB.getServicesCollection().update_one({'_id': serv['_id']}, {'$set': {'replicas': oldReplicas + nbAdded}})
    return make_response(jsonify({'success': 'Service scaled to ' + str(newReplicas) + ' replicas'}), 202)


#Permet d'obtenir les informations concernant le swarm
@app.route('/swarm',methods = ['GET'])
def api_getSwarm():
    if dockerSwarm.swarmExist() == True:
        swarmId = dockerSwarm.getSwarmId()
        swarmToken = dockerSwarm.getSwarmToken()
        swarmDate = dockerSwarm.getSwarmCreatedDate()
        swarm = {
            "ID" : swarmId,
            "swarmToken" : swarmToken,
            "swarmDate" : swarmDate
        }
        return make_response(jsonify(swarm), 202)
    else:
        return  make_response(jsonify({'error': 'Pas de swarm sur ce serveur'}), 403)

@auth.verify_password
def verify_password(username, password):
    numResult = managerDB.getUsersCollection().find({"user" : username}).count()
    if numResult == 0:
        return False
    else:
        result =  managerDB.getUsersCollection().find_one({"user" : username})
        if pwd_context.verify(password, result['password']):
            session['username'] = username
            return True
        else:
            return False

#cette fonction permet de supprimer tous les services
@app.route('/Services/delete',methods = ['POST'])
def deleteAllContainers():
    serviceName = request.get_json(force=True)['nameservice']
    result =  managerDB.getServicesCollection().find({"userId" : session['username'], "serviceName" : serviceName})

    if result == None:
        return make_response(jsonify({'error': 'aucun service de ce nom n existe'}), 403)
    else:
        try:
            containerId = result[0]['_id']
            containersBD = managerDB.getContainersCollection().find({"containerId" : containerId })
            for numContainer in range(0,containersBD.count()):
                dockerSwarm.deleteServiceById(containersBD[0]['serviceId'])
                managerDB.getContainersCollection().delete_one({"serviceId": containersBD[0]['serviceId']})
            managerDB.getServicesCollection().delete_one({"_id": containerId})
        except IndexError as err:
            print err
        return make_response(jsonify({'success': 'Tous les services on ete supprimer'}), 202)


#cette fonction permet de supprimer tous les services
@app.route('/Services/alldelete',methods = ['POST'])
def deleteAllServices():
    result =  managerDB.getServicesCollection().find({"userId" : session['username']})

    if result.count() == 0:
        return make_response(jsonify({'error': 'aucun service n existe'}), 403)
    else:
        try:
            for num in range(0,result.count()):
                containerId = result[0]['_id']
                containersBD = managerDB.getContainersCollection().find({"containerId" : containerId })
                for numContainer in range(0,containersBD.count()):
                    dockerSwarm.deleteServiceById(containersBD[0]['serviceId'])
                    managerDB.getContainersCollection().delete_one({"serviceId": containersBD[0]['serviceId']})
                managerDB.getServicesCollection().delete_one({"_id": containerId})
        except IndexError as err:
            print err
        return make_response(jsonify({'success': 'Tous les services on ete supprimer'}), 202)

#cette fonction permet de supprimer un service grace au nom
@app.route('/Containers/delete',methods = ['POST'])
def deleteService():
    serviceName = request.get_json(force=True)['nameservicedocker']
    servicedb   = managerDB.getContainersCollection().find_one({"ContainerName" : serviceName})
    if servicedb is None:
        return make_response(jsonify({'error': 'aucun service de ce nom n existe'}), 403)
    else:
        dockerSwarm.deleteServiceById(servicedb['serviceId'])
        service   = managerDB.getServicesCollection().find_one({ "_id": servicedb['containerId']})
        newReplicas = int(service['replicas']) -1
        managerDB.getServicesCollection().update( { "_id": servicedb['containerId']},  { "$set": {"replicas" :str(newReplicas)}})
        managerDB.getContainersCollection().delete_one({"ContainerName" : serviceName})
        return make_response(jsonify({'success': 'Service bien supprimer'}), 202)


#cette fonction verifie si l utilisateur est deja connecte
@app.route('/User/checkconnection',methods = ['POST'])
def checkconnection():
    if 'username' in session:
        result =  managerDB.getUsersCollection().find_one({"user" : session['username']})
        return make_response(jsonify({'success': 'utilisateur connecte', 'firstname' : result['firstname'], 'lastname' : result['lastname']}), 202)
    else:
        return make_response(jsonify({'success': 'utilisateur non connecte'}), 403)


@app.route('/Providers/services', methods =['GET'])
def getAllProviderServices():

    if 'username' not in session:
        return make_response(jsonify({'error': 'User not authenticated'}), 403)

    username = session['username']
    providerRecord = managerDB.getProviderCollection().find_one({'userId': username})
    if providerRecord is None:
        return make_response(jsonify({'error': 'User is not a registered provider'}), 403)
    # do we suppose we always have the nodeID for a given provider ?
    providerNodeID = providerRecord['nodeID']
    providerNode = dockerSwarm.getNode(providerRecord['nodeID'])
    providerTasks = dockerSwarm.lowLvlClient.tasks({'node': providerNodeID, 'desired-state': 'running'})

    serviceDict = {}
    serviceDict['services'] = []
    foundLogicalServicesNames = {}
    getProviderInfo = True
    for t in providerTasks:
        # get the name of the logical service that this task belongs to
        dockerServiceID = t['ServiceID']
        dockerServiceRecord = managerDB.getContainersCollection().find_one({'serviceId': dockerServiceID})
        if dockerServiceRecord is not None:
            # get the logical service that this docker service belongs to
            logicalServiceRecord = managerDB.getServicesCollection().find_one({'_id': dockerServiceRecord['containerId']})
            if logicalServiceRecord is not None:
                if getProviderInfo:
                    serviceDict['username'] = logicalServiceRecord['userId']
                    serviceDict['hostname'] = providerNode.attrs['Description']['Hostname']
                    serviceDict['OS']       = providerNode.attrs['Description']['Platform']['OS']
                    serviceDict['ipAddr']   = providerNode.attrs['Description']['Hostname']
                lsrNameWithUser = logicalServiceRecord['userId'] + '-' + logicalServiceRecord['serviceName']
                already = False
                if lsrNameWithUser in foundLogicalServicesNames:
                    already = True
                else:
                    foundLogicalServicesNames[lsrNameWithUser] = len(serviceDict['services'])

                if not already:
                    serviceDict['services'].append(
                        {
                            'serviceName': logicalServiceRecord['serviceName'],
                            'replicas': logicalServiceRecord['replicas'],
                            'containers': [
                                {
                                    'containerName': dockerServiceRecord['ContainerName'],
                                    'image': dockerServiceRecord['image'],
                                    'command': dockerServiceRecord['cmd'],
                                    'creationDate': t['CreatedAt']
                                }
                            ]

                        }
                    )
                else:
                    servIndex = foundLogicalServicesNames[lsrNameWithUser]
                    serviceDict['services'][servIndex]['containers'].append(
                        {
                            'containerName': dockerServiceRecord['ContainerName'],
                            'image': dockerServiceRecord['image'],
                            'command': dockerServiceRecord['cmd'],
                            'creationDate': t['CreatedAt']
                        }
                    )
    return make_response(jsonify(serviceDict), 202)




if __name__ == '__main__':
    if(dockerSwarm.swarmExist() == False):
        state = dockerSwarm.createSwarm()
        if state == True or state is None:
            swarmId = dockerSwarm.getSwarmId()
            swarmToken = dockerSwarm.getSwarmToken()
            swarmDate = dockerSwarm.getSwarmCreatedDate()
            managerDB.insertSwarm(swarmId,swarmToken,swarmDate)
            print "docker swarm ID : "+swarmId
            print "docker swarm Token : "+swarmToken
            print "docker swarm created date :"+swarmDate
            print "Initiation de dockerSwarm reussi"
            app.run(host = '0.0.0.0', port = SERVER_PORT)
        else:
            print "Un probleme avec l initiation du swarm"
    else:
        print "Utilisation du docker existant"
        app.run(host = '0.0.0.0', port = SERVER_PORT)
