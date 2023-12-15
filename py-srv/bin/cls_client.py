import logging, pyorient

logging.basicConfig(level=logging.INFO)
class OrientClient():
    def __new__(cls):
         if not hasattr(cls, 'instance'):
             cls.instance = super(OrientClient, cls).__new__(cls)
         return cls.instance
    
    def connect(self):
        self.client = pyorient.OrientDB("db", 2424)
        self.client.set_session_token(True)
        self.client.connect("root", "rootpwd")

    def __init__(self) -> None:
        self.database = 'animal'
        self.table = {'name': 'dog'}

    def create_database(self):

        self.client.db_create(self.database, pyorient.DB_TYPE_GRAPH,
                                       pyorient.STORAGE_TYPE_MEMORY)
        logging.info("database created")
        self.client.db_open(
            self.database, "root", "rootpwd", pyorient.DB_TYPE_GRAPH, ""
        )
        logging.info("openned database")

    def create_table(self):
        self.client.command("create class dog extends V")
        logging.info("table created")

    def create_schema(self):
        self.client.command("create property dog.breed String")
        self.client.command("create property dog.color String")
        logging.info("properties created")

    def seed(self):
        if self.client.db_exists(self.database, pyorient.STORAGE_TYPE_MEMORY):
            return 0

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

        logging.info("table seeded")
    
    def return_results(self, sql):
        try:
            records = self.client.query(sql)
            logging.info(records)
            return [o.oRecordData for o in records]
        except:
            return sql

    def get_all(self):
        sql = "select from dog"
        return self.return_results(sql)
    
    def get_by_breed(self, dog_breed):
        try:
            sql = f"select from dog where breed = '{dog_breed}'"
            return self.return_results(sql)
        except:
            return self.get_all()
    
    def get_by_color(self, dog_color):
        try:
            sql = f"select from dog where color = '{dog_color}'"
            return self.return_results(sql)
        except:
            return self.get_all()
    
    def del_by_breed(self, dog_breed):
        try:
            sql = f"delete dog where breed = '{dog_breed}'"
            self.client.command(sql)
        except:
            logging.warning("del_by_breed failed: breed => " + dog_breed)
            pass
        return self.get_all()
    
    def del_by_color(self, dog_color):
        try:
            sql = f"delete dog where color = '{dog_color}'"
            self.client.command(sql)
        except:
            logging.warning("del_by_color failed: color => " + dog_color)
            pass
        return self.get_all()
    
    def insert(self, dog_breed, dog_color):
        try:
            sql = "INSERT INTO dog (id, breed, color) VALUES('%s','%s')"
            self.client.command(sql % (dog_breed, dog_color))
        except:
            logging.warning("insert failed: breed => " + dog_breed + ", color => " + dog_color)
            pass
        return self.get_all()
    
    def upd_by_breed(self, new_dog_breed, old_dog_breed):
        try:
            sql = f"update dog set breed = '{new_dog_breed}' where breed = '{old_dog_breed}'"
            self.client.command(sql)
        except:
            logging.warning("upd_by_breed failed: new_breed => " + new_dog_breed + ", old_breed => " + old_dog_breed)
            pass
        return self.get_all()
    
    def upd_by_color(self, new_dog_color, old_dog_color):
        try:
            sql = f"update dog set color = '{new_dog_color}' where color = '{old_dog_color}'"
            self.client.command(sql)
        except:
            logging.warning("upd_by_color failed: new_color => " + new_dog_color + ", old_color => " + old_dog_color)
            pass
        return self.get_all()