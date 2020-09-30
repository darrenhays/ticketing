import json
from flask import Blueprint, Response, request
from models.process_model import ProcessModel

processes_blueprint = Blueprint('processes', __name__)


@processes_blueprint.route('/processes/<process_id>', methods=['GET'])
def get_processes(process_id):
    process_record = ProcessModel().get_process(process_id)
    if process_record:
        process_record['sub_processes'] = ProcessModel().get_processes_by_parent_process(process_id)
    return Response(json.dumps(process_record), status=200)
