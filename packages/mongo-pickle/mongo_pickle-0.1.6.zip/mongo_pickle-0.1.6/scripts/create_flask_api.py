import inspect
import inflection


FLASK_API = """
import json
import jsonpickle
from flask import Blueprint
{import_line}


api_blueprint = Blueprint('api', '{cls_name}',)


@api_blueprint.route('/api/{cls_name_lowercase}/fetch_data')
def fetch_data():
    return jsonpickle.dumps({cls_name}.load_objects())
    
if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    
    app.register_blueprint(api_blueprint)
    app.debug = True
    app.run()
"""


def generate_import(data_class):
    module = inspect.getmodule(data_class)
    return 'from {pkg} import {cls_name}'.format(pkg=module.__name__,
                                                 cls_name=data_class.__name__)


def generate_code(data_class, output_file_path):
    flask_code = FLASK_API.format(import_line=generate_import(data_class),
                                  cls_name_lowercase=inflection.underscore(data_class.__name__),
                                  cls_name=data_class.__name__)
    with open(output_file_path, 'w') as output_flask_file:
        output_flask_file.write(flask_code)
    output_flask_file.close()
