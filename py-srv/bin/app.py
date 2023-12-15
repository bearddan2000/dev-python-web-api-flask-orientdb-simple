from flask import Flask, request
import logging, pyorient
from cls_client import OrientClient

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

class Example():
    def __init__(self) -> None:
        self.database = 'animal'
        self.table = {'name': 'dog', 'columns': ['breed', 'color']}
        self.client = pyorient.OrientDB("db", 2424)
        self.client.set_session_token(True)
        self.client.connect("root", "rootpwd")
        self.seed()

    def create_database(self):
        self.client.db_create(self.database, pyorient.DB_TYPE_GRAPH,
                                       pyorient.STORAGE_TYPE_MEMORY)
        logging.info("database created")
        
        self.client.db_open(
            self.database, "root", "rootpwd", pyorient.DB_TYPE_GRAPH, ""
        )

    def create_table(self):
        self.client.command(f"create class {self.table['name']} extends V")

    def create_schema(self):
        self.client.command(f"create property {self.table['name']}.breed String")
        self.client.command(f"create property {self.table['name']}.color String")

    def seed(self):
        self.create_database()
        self.create_table()
        self.create_schema()

        records = [
                {'breed': 'Am Bulldog', 'color': 'White'},
                {'breed': 'Am Bulldog', 'color': 'Brown'}
            ]        

        sql = "INSERT INTO dog (breed, color) VALUES('%s','%s')"
        
        for record in records:
            breed = record['breed']
            color = record['color']
            self.client.command( sql % (breed, color))
    
    def return_results(self, sql):
        records = self.client.query(sql)
        return [o.oRecordData for o in records]

    def get_all(self):
        sql = "select from dog"
        return self.return_results(sql)
    
    def get_by_color(self, dog_color):
        sql = f"select from dog where color = '{dog_color}'"
        return self.return_results(sql)

@app.route('/')
def smoke_test():
    if request.method == 'GET':
        smoke = {'hello': 'world'}
        return {'results': smoke}

@app.route('/dog')
def get_all():
    client_obj.connect()
    return {"results": client_obj.get_all()}

# @app.route('/dog/color/<dog_color>')
# def get_del_by_color(dog_color):
#     if request.method == 'DELETE':
#         return {"results": client_obj.del_by_color(dog_color)}
#     elif request.method == 'GET':
#         return {"results": client_obj.get_by_color(dog_color)}
# 
# @app.route('/dog/breed/<dog_breed>')
# def get_del_by_breed(dog_breed):
#     if request.method == 'DELETE':
#         return {"results": client_obj.del_by_breed(dog_breed)}
#     elif request.method == 'GET':
#         return {"results": client_obj.get_by_breed(dog_breed)}
# 
# @app.route('/dog/breed/<dog_breed>/color/<dog_color>')
# def insert(dog_breed, dog_color):
#     return {"results": client_obj.insert(dog_breed, dog_color)}
# 
# @app.route('/dog/color/new/<new_dog_color>/old/<old_dog_color>')
# def upd_by_color(new_dog_color, old_dog_color):
#     return {"results": client_obj.upd_by_color(new_dog_color, old_dog_color)}
# 
# @app.route('/dog/breed/new/<new_dog_breed>/old/<old_dog_breed>')
# def upd_by_breed(new_dog_breed, old_dog_breed):
#     return {"results": client_obj.upd_by_breed(new_dog_breed, old_dog_breed)}
# 
if __name__ == "__main__":
    client_obj = Example() # OrientClient()
#    client_obj.connect()
#    client_obj.seed()
    app.run(host ='0.0.0.0', port = 5000, debug = True)
