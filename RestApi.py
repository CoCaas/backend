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
#TODO voir avec Quentin si on peut inclure le nodeID dans provider
from flask import Flask, url_for, Response, jsonify, session, make_response,request, send_from_directory
from passlib.apps import custom_app_context as pwd_context
from flask_httpauth import HTTPBasicAuth
import json
import managerDB
import dockerSwarm
app =Flask(__name__, static_url_path='')
app.secret_key = 'de la merde'
auth = HTTPBasicAuth()

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
    nbCPU = request.get_json(force=True)['nbCPU']
    nbMemory = request.get_json(force=True)['nbMemory']
    nbStockage = request.get_json(force=True)['nbStockage']
    username = request.get_json(force=True)['username']
    password = request.get_json(force=True)['password']
    nodeIP   = request.remote_addr

    if nbCPU is None or nbMemory is None or nbStockage is None or username is None or password is None or nodeIP is None:
        return  make_response(jsonify({'error': 'un argument est manquant'}), 403)

    numResult = managerDB.getUsersCollection().find({"user" : username}).count()
    if numResult == 0:
        return make_response(jsonify({'error': 'cet utilisateur n existe pas'}), 403)
    else:
        result =  managerDB.getUsersCollection().find_one({"user" : username})
        if pwd_context.verify(password, result['password']):
            managerDB.insertProvider(username,nbCPU,nbMemory,nbStockage,nodeIP)
            return make_response(jsonify({'nbCPU': nbCPU, 'nbMemory': nbMemory, 'nbStockage' :nbStockage, 'nodeIP' : nodeIP }), 202)
        else:
            return make_response(jsonify({'error': 'Le mot de passe est incorrect'}), 403)

#TODO Permet de recuperer les informations d un noeud grace a l id
@app.route('/Provider', methods = ['POST'])
def api_getProvider():
    if 'username' in session:
        managerDB.getProviderCollection().find_one( {"userId" : session['username']} )
        return  make_response(jsonify({'message': 'reussi'}), 202)
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


#Permet d obtenir la liste des containers d'un service precis
@app.route('/Services/Container')
def api_getServiceContainer():
    print "adresse IP "+request.remote_addr


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
            serviceGlobalName = username+"-"+name
            for num in range(1,int(nbReplicas) + 1):
                ServiceName = serviceGlobalName+"-"+str(num)
                serviceId = dockerSwarm.createService(ServiceName,image,commande)
                managerDB.insertService(username,serviceId,ServiceName,nbReplicas,image,commande,bindPorts)
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
            if result.count() == 0:
                make_response(jsonify({}), 202)
            else:
                JsondataGlobal =[]
                for num in range(0,int(result.count())):
                    serviceId = result[num]['serviceId']
                    if serviceId is not None:
                        service = dockerSwarm.getServiceById(serviceId)
                        if service is not None:
                            Jsondata = {}
                            serviceInfo = service.attrs
                            tasks = dockerSwarm.getServiceTasks(serviceId)
                            Jsondata['nodeId'] = tasks[0]['NodeID']
                            nodeInfo = dockerSwarm.getNode(tasks[0]['NodeID']).attrs

                            Jsondata['ports'] = result[num]['bindPorts']
                            Jsondata['nomMachine'] = nodeInfo['Description']['Hostname']
                            Jsondata['ipMachine'] = nodeInfo['Status']['Addr']
                            Jsondata['NomService'] = serviceInfo['Spec']['Name']
                            Jsondata['nomImage'] = serviceInfo['Spec']['TaskTemplate']['ContainerSpec']['Image']
                            Jsondata['commande'] = serviceInfo['Spec']['TaskTemplate']['ContainerSpec']['Command']
                            Jsondata['datecreation'] = serviceInfo['CreatedAt']
                            Jsondata['status'] = serviceInfo['UpdateStatus']
                            JsondataGlobal.append(Jsondata)

                infoJson = json.dumps(JsondataGlobal)
                return make_response(jsonify({'services': JsondataGlobal}), 202)
        else:
            return make_response(jsonify({'error': 'Docker swar n as pas demarrer'}), 403)
        return  make_response(jsonify({'message': 'reussi'}), 202)
    else:
        return  make_response(jsonify({'error': 'veuillez vous connecter svp'}), 403)


#Permet de supprimer tous les services lies a un client
@app.route('/Services/delete/<idClient>')
def api_deleteServices(idClient):
    return temp
#permet de supprimer un service particulie lie e un client
@app.route('/Services/delete/<idService>/<idClient>')
def api_deleteServiceContainer(idService,idClient):
    return temp

#Retourne la liste des service cree par un client
@app.route('/Services',methods = ['GET'])
#@auth.login_required
def api_getAllServices():
    return "none"

#Permet de reScale un service en particulier
@app.route('/Services/scale/<nbReplicas>/<idService>/<idClient>')
def api_scaleService(nbReplicas,idService,idClient):
    return temp

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
    serviceName = session['username']+"-"+serviceName
    result =  managerDB.getServicesCollection().find({"userId" : session['username']})

    if result == None:
        return make_response(jsonify({'error': 'aucun service de ce nom n existe'}), 403)
    else:

        for num in range(0,result.count()):
            if serviceName in result[num]['serviceName']:
                dockerSwarm.deleteServiceById(result[num]['serviceId'])
                managerDB.getServicesCollection().delete_one({"serviceId": result[num]['serviceId']})
        return make_response(jsonify({'success': 'Tous les services on ete supprimer'}), 202)

#cette fonction permet de supprimer tous les services
@app.route('/Services/alldelete',methods = ['POST'])
def deleteAllServices():
    serviceName = session['username']+"-"+serviceName
    result =  managerDB.getServicesCollection().find({"userId" : session['username']})

    if result == None:
        return make_response(jsonify({'error': 'aucun service de ce nom n existe'}), 403)
    else:

        for num in range(0,result.count()):
            dockerSwarm.deleteServiceById(result[num]['serviceId'])
            managerDB.getServicesCollection().delete_one({"serviceId": result[num]['serviceId']})
        return make_response(jsonify({'success': 'Tous les services on ete supprimer'}), 202)

#cette fonction permet de supprimer un service grace au nom
@app.route('/Containers/delete',methods = ['POST'])
def deleteService():
    serviceName = request.get_json(force=True)['nameservicedocker']
    serviceName = session['username']+"-"+serviceName
    servicedb   = managerDB.getServicesCollection().find_one({"serviceName" : serviceName})
    #managerDB.getServicesCollection().update( { "user": session['username']},  { "$set": {"password" : hash1}}   )
    if servicedb == None:
        return make_response(jsonify({'error': 'aucun service de ce nom n existe'}), 403)
    else:
        dockerSwarm.deleteServiceById(servicedb['serviceId'])
        managerDB.getServicesCollection().delete_one({"serviceId": servicedb['serviceId']})

        result =  managerDB.getServicesCollection().find({"userId" : session['username']})
        if result == None:
            print "Plus de service"
        else:
            for num in range(0,result.count()):
                if serviceName in result[num]['serviceName']:
                    managerDB.getServicesCollection().update( { "serviceName": result[num]['serviceName']},  { "$inc": {"replicas" : int(-1)}}   )
        return make_response(jsonify({'success': 'Service bien supprimer'}), 202)

#cette fonction verifie si l utilisateur est deja connecte
@app.route('/User/checkconnection',methods = ['POST'])
def checkconnection():
    if 'username' in session:
        result =  managerDB.getUsersCollection().find_one({"user" : session['username']})
        return make_response(jsonify({'success': 'utilisateur connecte', 'firstname' : result['firstname'], 'lastname' : result['lastname']}), 202)
    else:
        return make_response(jsonify({'success': 'utilisateur non connecte'}), 403)

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
            app.run()
        else:
            print "Un probleme avec l initiation du swarm"
    else:
        print "Utilisation du docker existant"
        app.run()
