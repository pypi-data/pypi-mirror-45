from bson import ObjectId
from mongo_pickle.api import transform_object, transform_document, set_mongo_handler


class Model(object):
    COLLECTION = None

    def __init__(self, _id=None, **kwargs):
        self._id = ObjectId(_id)

    def set_collection(self, mongo_collection, class_level=True):
        if class_level:
            Model.COLLECTION = mongo_collection
        else:
            self.COLLECTION = mongo_collection

    def check_mongo_connection(self):
        raise NotImplementedError()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return all([getattr(other,key, None) == value for key, value in self.__dict__.items()
                        if key != '_id'])
        else:
            return False

    def save(self):
        set_mongo_handler()
        document = transform_object(self)
        document_id = document.pop('_id')
        self.COLLECTION.find_one_and_replace({'_id': ObjectId(self._id)}, document, upsert=True)
        return document

    @classmethod
    def load_objects(cls, custom_filter={}):
        set_mongo_handler()
        documents = cls.COLLECTION.find(transform_object(custom_filter))
        return [transform_document(doc) for doc in documents]

    @staticmethod
    def load_from_document(mongo_document):
        return transform_document(mongo_document)

    @classmethod
    def load_from_id(cls, document_id):
        # fetch document
        document = cls.COLLECTION.find_one({'_id': ObjectId(document_id)})
        return transform_document(document)

    @classmethod
    def remove(cls, custom_filter):
        return cls.COLLECTION.delete_many(custom_filter)