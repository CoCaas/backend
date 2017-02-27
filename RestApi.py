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

from flask import Flask, url_for, Response, jsonify
import json
app =Flask(__name__)


#returne tous les containers appartenant à un client donné
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

#permet d'ajouter un nouvel utilisateur
@app.route('/User/new/<username>/<hash>', methods = ['POST'])
def api_addProvider(username,hash):
    return temp

#Permet d'obtenir la liste des containers d'un service précis
@app.route('/Services/Container/<idService>/<idClient>')
def api_getServiceContainer(idService,idClient):
    return temp

#Permet d'inserer un nouveau service
@app.route('/Services/new/<name>/<nbReplicas>/<image>/<commande>/<idClient>')
def api_addService(name,nbReplicas,image,commande,idClient):
    return temp

#Permet de supprimer tous les services liés à un client
@app.route('/Services/delete/<idClient>')
def api_deleteServices(idClient):
    return temp
#permet de supprimer un service particulié lié à un client
@app.route('/Services/delete/<idService>/<idClient>')
def api_deleteServiceContainer(idService,idClient):
    return temp

#Retourne la liste des service créé par un client
@app.route('/Services')
def api_getAllServices():
    return temp

#Permet de reScale un service en particulier
@app.route('/Services/scale/<nbReplicas>/<idService>/<idClient>')
def api_scaleService(nbReplicas,idService,idClient):
    return temp

    
if __name__ == '__main__':
    app.run()
