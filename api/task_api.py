import urllib3
import urllib
import json
from .base_api import BaseApi

http = urllib3.PoolManager()


class TaskApi(BaseApi):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.root_url = '/api/'

    def update_task(self, task_id, result):
        url = 'task/update'
        params = {
            'task_id': task_id,
            'result': result
        }
        return self._post_req(url, params)
