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

from flask import Flask, url_for, Response, jsonify, session, make_response
import json
import managerDB
app =Flask(__name__)
app.secret_key = 'de la merde'


@app.route('/Containers/<idClient>', methods = ['POST'])
def api_getAllContainer(idClient):

    return resp

#retourne les informations d'un container specifique grace au idClient et au idContainer
@app.route('/Containers/<idClient>/<idContainer>', methods = ['POST'])
def api_getContainer(idClient, idContainer):

    return resp

#Permet d'enregistrer provider
@app.route('/Providers/new/<nbCPU>/<nbMemory>/<nbStockage>/<idClient>', methods = ['POST'])
def api_getProvider(nbCPU,nbMemory,nbStockage,idClient):

    print len(provider)

#permet de se connecter
@app.route('/User/login/<username>/<hash>', methods = ['POST'])
def api_connect(username,hash):
    if 'username' in session:
        return  make_response(jsonify({'error': 'vous etes deja connecte'}), 403)
    else:
        numResult = managerDB.getUsersCollection().find({"user" : username}).count()
        if numResult == 0:
            return make_response(jsonify({'error': 'cet utilisateur n existe pas'}), 403)
        else:
            result =  managerDB.getUsersCollection().find_one({"user" : username})
            if result['password'] == hash:
                session['username'] = username
                return make_response(jsonify({'success': 'vous etes connecte'}), 202)
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
@app.route('/User/new/<username>/<hash>', methods = ['POST'])
def api_addUser(username,hash):
    numResult = managerDB.getUsersCollection().find({"user" : username}).count()
    if numResult == 0:
        managerDB.insertUser(username,hash)
        return  make_response(jsonify({'sucess': 'Utilisateur bien ajouter'}), 202)
    else:
        return  make_response(jsonify({'error': 'cet utilisateur existe deja'}), 403)



#Permet d obtenir la liste des containers d'un service precis
@app.route('/Services/Container/<idService>/<idClient>')
def api_getServiceContainer(idService,idClient):
    return temp

#Permet d'inserer un nouveau service
@app.route('/Services/new/<name>/<nbReplicas>/<image>/<commande>/<idClient>')
def api_addService(name,nbReplicas,image,commande,idClient):
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
@app.route('/Services')
def api_getAllServices():
    return temp

#Permet de reScale un service en particulier
@app.route('/Services/scale/<nbReplicas>/<idService>/<idClient>')
def api_scaleService(nbReplicas,idService,idClient):
    return temp


if __name__ == '__main__':
    app.run()
