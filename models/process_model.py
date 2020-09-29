import logging
from boto3.dynamodb.conditions import Key
from models.abstract_model import AbstractModel
from settings import PROCESS_TABLE_NAME

logger = logging.getLogger()


class ProcessModel(AbstractModel):
    table_name = PROCESS_TABLE_NAME

    def create_process(self, attributes={}):
        return self.insert(attributes)

    def get_process(self, process_id):
        return self.get(process_id)

    def delete_process(self, process_id):
        return self.delete(process_id)

    def update_process(self, process_id, updated_attributes):
        return self.update(process_id, updated_attributes)

    def get_processes_by_parent_process(self, parent_process_id):
        logger.info("########## {} get_processes_by_parent_process ##########".format(self.__class__.__name__))
        logger.info("parent_process_id: {}".format(parent_process_id))
        key = Key('parent_process_id').eq(parent_process_id)
        try:
            response = self.table.query(IndexName='parent_process_id_index', KeyConditionExpression=key)
            return response.get('Items')
        except Exception as e:
            logger.error(e)
            return []
