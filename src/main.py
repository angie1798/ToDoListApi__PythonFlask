"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Todo
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/todos', methods=['GET'])
def get_todo():
    query= Todo.query.all()
    all_todo= list(map(lambda x: x.serialize(), query))
    return jsonify(all_todo),200

@app.route('/todos', methods=['POST'])
def add_new_todo():
    req = request.get_json()
    todo = Todo(label=req["label"], done=req["done"])
    db.session.add(todo)
    db.session.commit()
    return("Todo correcto")

@app.route('/todos/<int:position>', methods=['DELETE'])
def delete_todo(position):
    todo = Todo.query.get(position)
    if todo is None:
        raise APIException('Todo not found', status_code=404)
    db.session.delete(todo)
    db.session.commit()
    return ("Elemento eliminado")

@app.route('/todos/<int:position>', methods=['PUT'])
def upd_todo(position):
    todo = Todo.query.get(position)
    req = request.get_json()
    if todo is None:
        raise APIException('User not found', status_code=404)

    if "label" in req:
        todo.label = req["label"]
    if "done" in req:
        todo.done = req["done"]
    db.session.commit()
    return ("Elemento modificado")


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
