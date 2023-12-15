from flask import Flask, request
import logging

from cls_client import OrientClient

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

client_obj = OrientClient()

@app.route('/')
def smoke_test():
    if request.method == 'GET':
        smoke = {'hello': 'world'}
        return {'results': smoke}

@app.route('/dog')
def get_all():
    if request.method == 'GET':
        return {"results": client_obj.get_all()}

@app.route('/dog/color/<dog_color>')
def get_del_by_color(dog_color):
    if request.method == 'DELETE':
        return {"results": client_obj.del_by_color(dog_color)}
    elif request.method == 'GET':
        return {"results": client_obj.get_by_color(dog_color)}

@app.route('/dog/breed/<dog_breed>')
def get_del_by_breed(dog_breed):
    if request.method == 'DELETE':
        return {"results": client_obj.del_by_breed(dog_breed)}
    elif request.method == 'GET':
        return {"results": client_obj.get_by_breed(dog_breed)}

@app.route('/dog/breed/<dog_breed>/color/<dog_color>')
def insert(dog_breed, dog_color):
    return {"results": client_obj.insert(dog_breed, dog_color)}

@app.route('/dog/color/new/<new_dog_color>/old/<old_dog_color>')
def upd_by_color(new_dog_color, old_dog_color):
    return {"results": client_obj.upd_by_color(new_dog_color, old_dog_color)}

@app.route('/dog/breed/new/<new_dog_breed>/old/<old_dog_breed>')
def upd_by_breed(new_dog_breed, old_dog_breed):
    return {"results": client_obj.upd_by_breed(new_dog_breed, old_dog_breed)}

if __name__ == "__main__":    
    app.run(host ='0.0.0.0', port = 5000, debug = True)
