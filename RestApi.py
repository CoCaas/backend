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

#@app.route('/getAllUsers', methods = ['GET'])
#def api_getAllUser():

@app.route('/getAllContainers', methods = ['GET'])
def api_getAllContainers():

    resp = jsonify(json.loads(open('exempleContainer.json').read()))
    resp.status_code = 200

    return resp

@app.route('/getAllProviders', methods = ['GET'])
def api_getAllProviders():
        resp = jsonify(json.loads(open('exempleListProviders.json').read()))
        resp.status_code = 200
        return resp
#@app.route('/getUser/<userId>', methods = ['GET'])
#def api_getUser(userId):

@app.route('/getProvider/<providerId>', methods = ['GET'])
def api_getProvider(providerId):
    providers = json.loads(open('exempleListProviders.json').read()) 
    for provider in providers:
        print provider
    print len(provider)
#@app.route('/getContainer/<containerId>', methods = ['GET'])
#def api_getContainers(containerId):

if __name__ == '__main__':
    app.run()
