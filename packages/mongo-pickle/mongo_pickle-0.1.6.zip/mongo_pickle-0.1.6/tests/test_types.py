import pytz
import pytest
from datetime import datetime
from mongomock import MongoClient


from mongo_pickle.model import Model


def get_testing_collection():
    return MongoClient().db.test_collection


class StubObject(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class ComplexObject(Model):
    COLLECTION = get_testing_collection()

    def __init__(self, int_value, bool_value, string_value, datetime_value, date_value,
                 mapping_value, class_value):
        super(ComplexObject, self).__init__()
        self.int_member = int_value
        self.bool_member = bool_value
        self.string_member = string_value
        self.date_member = date_value
        self.datetime_member = datetime_value
        self.mapping_member = mapping_value
        self.class_member = class_value


def generate_sample_object(**kwargs):
    ComplexObject.COLLECTION = get_testing_collection()
    return ComplexObject(
        int_value=1,
        bool_value=False,
        string_value='Testing מחרוזת',
        datetime_value=datetime.now(),
        date_value=datetime.now().date(),
        mapping_value={'1': 'test', '2': 'another_test'},
        class_value=StubObject(1, 2)
    )


def test_sanity():
    example = generate_sample_object()
    example.save()
    object_id = example._id
    example_copy = ComplexObject.load_from_id(object_id)
    assert example_copy.__dict__ == example.__dict__


def test_id_consistency():
    example = generate_sample_object()
    example.save()
    object_id = example._id
    example_copy = ComplexObject.load_from_id(object_id)

    assert object_id == example_copy._id
    assert example == ComplexObject.load_objects()[0]


@pytest.mark.freeze_time('2000-01-01')
def test_datetime_timezone():
    utc_datetime = datetime.now(tz=pytz.UTC)
    israel_datetime = datetime.now(tz=pytz.timezone('Asia/Jerusalem'))
    assert israel_datetime == utc_datetime
    assert type(israel_datetime) == datetime
    example = generate_sample_object()
    example.datetime_member = israel_datetime
    example.save()
    objects = example.load_objects()
    assert objects[0].datetime_member == israel_datetime

    objects = example.load_objects({'datetime_member': israel_datetime})
    assert objects[0].datetime_member == israel_datetime
