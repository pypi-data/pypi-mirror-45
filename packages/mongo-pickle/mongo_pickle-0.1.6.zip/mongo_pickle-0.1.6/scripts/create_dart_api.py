import inspect
# Todo: Convert to using dart-lang/code_builder


DART_MONGO_HEADERS = """
// import this way to avoid name collision for State object
import 'package:mongo_dart/mongo_dart.dart' as mongo; 
"""

DART_CLASS_CODE = """
class {cls_name} {{
  final mongo.ObjectId id;
  {fields_declaration}

  {cls_name}({default_ctor_parameters});

  factory {cls_name}.fromJson(Map<String, dynamic> json) {{
    return {cls_name}(
        id: json['_id'],
        {default_ctor_code}
    );
  }}
  
}}
"""


DART_DAL_API = """
class Api{{
  var db = new mongo.Db("mongodb://{username}:{password}@{host}:{port}/{database}");

  Future<List<{cls_name}>> _fetchData() async{{
    await this.db.open();

    var parsedObjects = List<{cls_name}>();
    var collection = this.db.collection('{collection}');
    await collection.find().forEach(
      (v) => parsed.add({cls_name}.fromJson(v))
      );

    return parsedObjects;
  }}
}}
"""


def get_class_name(cls):
    return cls.__name__


def get_fields(cls):
    ctor_signature = inspect.signature(cls.__init__)
    return list(ctor_signature.parameters)[1:] # Skip "self"


def generate_dart_class(data_class):
    class_code = DART_CLASS_CODE
    parameter_declaration = ''
    class_fields = get_fields(data_class)
    for cls_field in class_fields:
        parameter_declaration += 'final dynamic {field_name};'.format(field_name=cls_field)

    default_ctor_parameters = ''.join(['this.{field_name}, '.format(field_name=cls_field)
                                       for cls_field in class_fields])

    ctor_code = '\n'.join([
        "{field_name}: json['{field_name}'],".format(field_name=cls_field)
        for cls_field in class_fields
    ])

    return class_code.format(cls_name=get_class_name(data_class),
                             fields_declaration=parameter_declaration,
                             default_ctor_parameters=default_ctor_parameters,
                             default_ctor_code=ctor_code)


def generate_dart_dal(data_class, mongo_config):
    return DART_DAL_API.format(cls_name=get_class_name(data_class),
                               host=mongo_config.host,
                               port=mongo_config.port,
                               database=mongo_config.database,
                               collection=mongo_config.collection,
                               username=mongo_config.username,
                               password=mongo_config.password,)


def generate_dart_api(data_class, mongo_config, output_file_path):
    dart_code = DART_MONGO_HEADERS
    dart_code += '\r\n\r\n'
    dart_code += generate_dart_class(data_class)
    dart_code += '\r\n\r\n'
    dart_code += generate_dart_dal(data_class, mongo_config)
    with open(output_file_path, 'w') as output_api_file:
        output_api_file.write(dart_code)
    output_api_file.close()


if __name__ == '__main__':
    from mongo_pickle.model import Model
    from mongo_pickle.collection import CollectionConfig


    class LogsConfig(CollectionConfig):
        host = 'ds161112.mlab.com'
        port = 61112

        database = 'calendar'
        collection = "events"
        username = '111yoav'
        password = '123456a'


    class Log(Model):
        COLLECTION = LogsConfig.get_collection()

        def __init__(self, timestamp, level, thread, threadName, message, loggerName, fileName, module, method,
                     lineNumber):
            self.timestamp = timestamp
            self.level = level
            self.thread = thread
            self.threadName = threadName
            self.message = message
            self.loggerName = loggerName
            self.fileName = fileName
            self.module = module
            self.method = method
            self.lineNumber = lineNumber


    generate_dart_api(Log, LogsConfig, 'sample.dart')