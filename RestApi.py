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

from flask import Flask, url_for, Response, jsonify, session, make_response,request
from passlib.apps import custom_app_context as pwd_context
from flask_httpauth import HTTPBasicAuth
import json
import managerDB
import dockerSwarm
app =Flask(__name__)
app.secret_key = 'de la merde'
auth = HTTPBasicAuth()

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
                rep = make_response(jsonify({'success': 'vous etes connecte'}), 202)
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
    if username is None or password is None:
        return make_response(jsonify({'error': 'Pas de mot de passe ou de nom d utilisateur'}), 403)

    numResult = managerDB.getUsersCollection().find({"user" : username}).count()
    if numResult == 0:
        hash = pwd_context.encrypt(password)
        managerDB.insertUser(username,hash)
        return  make_response(jsonify({'sucess': 'Utilisateur bien ajouter'}), 202)
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
@app.route('/Services/new')
def api_addService():
    name = request.get_json(force=True)['name']
    nbReplicas = request.get_json(force=True)['nbReplicas']
    image = request.get_json(force=True)['image']
    commande = request.get_json(force=True)['commande']
    bindPorts = request.get_json(force=True)['bindPorts']

    if name is None or nbReplicas is None or image is None or bindPorts is None:
        return make_response(jsonify({'error': 'Un des arguments est manquant'}), 403)

    if 'username' in session:
        managerDB.insertService(session['username'],name,nbReplicas,image,commande,bindPorts)
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
