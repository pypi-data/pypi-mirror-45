from datetime import datetime, date

from jsonpickle.pickler import Pickler
from jsonpickle.unpickler import Unpickler
from jsonpickle.handlers import DatetimeHandler

from mongo_pickle.handlers.time_handlers import MongoDatetimeHandler, MongoDateHandler


def transform_object(e):
    context = Pickler()
    return context.flatten(e)


def transform_document(doc):
    un_context = Unpickler()
    return un_context.restore(doc)


def set_mongo_handler():
    MongoDateHandler.handles(date)
    MongoDatetimeHandler.handles(datetime)


def set_default_handler():
    DatetimeHandler.handles(date)
    DatetimeHandler.handles(datetime)
