from pymongo import MongoClient


class CollectionConfig(object):
    # Here, we specify the database and collection names.
    # A connection to your DB is automatically created.
    host = None
    port = None
    database = None
    username = None
    password = None
    collection = None

    @classmethod
    def get_collection(cls):
        """
        Utility to get pymongo collection easily
        :return: Pymongo collection object
        """
        client = MongoClient(cls.host, cls.port)
        db = client[cls.database]
        db.authenticate(cls.username, cls.password)
        return db[cls.collection]

