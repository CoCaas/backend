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
import managerDB
import dockerSwarm
app =Flask(__name__, static_url_path='')
app.secret_key = 'de la merde'
auth = HTTPBasicAuth()

@app.route('/')
def send_welcome_page():
    return send_from_directory('web', 'index.html')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('web/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('web/css', path)

@app.route('/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory('web/fonts', path)

@app.route('/about.html')
def send_about_page():
    return send_from_directory('web', 'about.html')

@app.route('/client.html')
def send_client_page():
    return send_from_directory('web', 'client.html')

@app.route('/provider.html')
def send_provider_page():
    return send_from_directory('web', 'provider.html')

@app.route('/preferences.html')
def send_preferences_page():
    return send_from_directory('web', 'preferences.html')

@app.route('/create-dialog.html')
def send_create_dialog_page():
    return send_from_directory('web', 'create-dialog.html')

@app.route('/login-dialog.html')
def send_login_dialog_page():
    return send_from_directory('web', 'login-dialog.html')

@app.route('/delete-docker-machine.html')
def send_delete_docker_machine_page():
    return send_from_directory('web', 'delete-docker-machine.html')

@app.route('/demand-ressource.html')
def send_demand_ressource_page():
    return send_from_directory('web', 'demand-ressource.html')

@app.route('/insert-docker-machine.html')
def send_insert_docker_machine_page():
    return send_from_directory('web', 'insert-docker-machine.html')

@app.route('/users-containers.html')
def send_users_containers_page():
    return send_from_directory('web', 'users-containers.html')

@app.route('/Containers/<idClient>', methods = ['POST'])
def api_getAllContainer(idClient):
    return resp

#retourne les informations d'un container specifique grace au idClient et au idContainer
@app.route('/Containers/<idClient>/<idContainer>', methods = ['POST'])
def api_getContainer(idClient, idContainer):

    return resp

#Permet d enregistrer provider
#nbCPU : le nombre de cpu a alouer
#nbMemory : le nombre de memoire a alouer
#nbStockage: le nombre de disque a alouer
@app.route('/Providers/new', methods = ['POST'])
def api_setProvider(nbCPU,nbMemory,nbStockage):
    nbCPU = request.get_json(force=True)['nbCPU']
    nbMemory = request.get_json(force=True)['nbMemory']
    nbStockage = request.get_json(force=True)['nbStockage']

    if nbCPU is None or nbMemory is None or nbStockage is None:
        return  make_response(jsonify({'error': 'un argument est manquant'}), 403)

    if 'username' in session:
        managerDB.insertProvider(session['username'],nbCPU,nbMemory,nbStockage)
        return  make_response(jsonify({'message': 'reussi'}), 202)
    else:
        return  make_response(jsonify({'error': 'veuillez vous connecter svp'}), 403)


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
@app.route('/Services/Container/<idService>/<idClient>')
def api_getServiceContainer(idService,idClient):
    return temp

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
            serviceGlobalName = username+"."+name
            for num in range(1,int(nbReplicas)):
                ServiceName = serviceGlobalName+"."+num
                serviceId = createService(ServiceName,image,commande)
                managerDB.insertService(username,serviceId,ServiceName,nbReplicas,image,commande,bindPorts)
        else:
            return make_response(jsonify({'error': 'Docker swar n as pas demarrer'}), 403)
        return  make_response(jsonify({'message': 'reussi'}), 202)
    else:
        return  make_response(jsonify({'error': 'veuillez vous connecter svp'}), 403)
    return temp

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
@app.route('/services/delete',methods = ['POST'])
def deleteAllServices():
    serviceName = request.get_json(force=True)['nameservice']
    serviceName = session['username']+"."+serviceName+".1"
    result =  managerDB.getServicesCollection().find_one({"serviceName" : serviceName})

    if result == None:
        return make_response(jsonify({'error': 'aucun service de ce nom n existe'}), 403)
    else:
        nbreplicas = int(result['replicas'])
        for num in range(1,nbreplicas):
            servicedb = managerDB.getServicesCollection().find_one({"serviceName" : serviceName+"."+num})
            dockerSwarm.deleteServiceById(servicedb['serviceId'])
            managerDB.getServicesCollection().delete_many({"serviceId": servicedb['serviceId']})
        return make_response(jsonify({'success': 'Tous les services on ete supprimer'}), 202)

#cette fonction permet de supprimer un service grace au nom
@app.route('/services/delete',methods = ['POST'])
def deleteService():
    serviceName = request.get_json(force=True)['nameservicedocker']
    serviceName = session['username']+"."+serviceName
    servicedb   = managerDB.getServicesCollection().find_one({"serviceName" : serviceName})
    if servicedb == None:
        return make_response(jsonify({'error': 'aucun service de ce nom n existe'}), 403)
    else:
        dockerSwarm.deleteServiceById(servicedb['serviceId'])
        managerDB.getServicesCollection().delete_many({"serviceId": servicedb['serviceId']})
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
    #state = dockerSwarm.createSwarm()
    #if state == True or state is None:
    #    swarmId = dockerSwarm.getSwarmId()
    #    swarmToken = dockerSwarm.getSwarmToken()
    #    swarmDate = dockerSwarm.getSwarmCreatedDate()
    #    managerDB.insertSwarm(swarmId,swarmToken,swarmDate)
    #    print "docker swarm ID : "+swarmId
    #    print "docker swarm Token : "+swarmToken
    #    print "docker swarm created date :"+swarmDate
    #    print "Initiation de dockerSwarm reussi"
        app.run()
    #else:
    #    print "Un probleme avec l initiation du swarm"
