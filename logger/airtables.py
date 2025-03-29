import logging
import traceback
import requests
import json
import sys
from datetime import datetime
from decouple import config

class AirtableHandler(logging.Handler):
    SHOULD_CLEAR_OLD_RECORDS = False    # нужно ли удалять старые записи?
    OLD_RECORDS_DELETE_THRESHOLD = 5    # со скольки записей надо удалять старые?
    OLD_RECORDS_DELETE_NUMBER = 3       # сколько старых записей надо удалить?

    def __init__(self, api_key, base_id, table_name):
        super().__init__()
        self.api_key = api_key
        self.base_id = base_id
        self.table_name = table_name
        self.url = f"https://api.airtable.com/v0/{self.base_id}/{self.table_name}"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def control_records_count(self):
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            records = json.loads(response.text)['records']

            if len(records) > self.OLD_RECORDS_DELETE_THRESHOLD:
                old_records = records[0:self.OLD_RECORDS_DELETE_NUMBER]
                old_records_ids = [x['id'] for x in old_records]
                self.del_old_records(old_records_ids)

    def del_old_records(self, old_records_ids):
        for record_id in old_records_ids:
            url = f'{self.url}/{record_id}'
            headers = self.headers

            response = requests.delete(url, headers=headers)

            if response.status_code == 200:
                print(f'Deleted record {record_id}')
            else:
                print(f'Error deleting record {record_id}: {response.status_code} - {response.text}')

    def emit(self, record):
        if self.SHOULD_CLEAR_OLD_RECORDS:
            self.control_records_count()
        log_entry = self.format(record)
        data = {
            "fields": {
                "Level": record.levelname,
                "Timestamp": datetime.utcnow().isoformat(),
                'Filename': record.filename,
                'Function': record.funcName,
                'Lineno': str(record.lineno),
                "Message": log_entry + traceback.format_exc(),
            }
        }
        response = requests.post(self.url, headers=self.headers, data=json.dumps(data))
        if response.status_code != 200:
            print(f"Failed to send log to Airtable: {response.text}")


def setup_logger():
    AIRTABlES_API_KEY = config('AIRTABlES_API_KEY')
    AIRTABlES_BASE_ID = config('AIRTABlES_BASE_ID')
    AIRTABlES_TABLE_NAME = config('AIRTABlES_TABLE_NAME')

    airtable_handler = AirtableHandler(AIRTABlES_API_KEY, AIRTABlES_BASE_ID, AIRTABlES_TABLE_NAME)
    # formatter = logging.Formatter('%(levelname)s - %(name)s - %(funcName)s - %(lineno)s - %(message)s')
    formatter = logging.Formatter('%(message)s')
    airtable_handler.setFormatter(formatter)

    logger = logging.getLogger('AirtableLogger')
    #logger = logging.StreamHandler(sys.stdout)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(airtable_handler)

    return logger
