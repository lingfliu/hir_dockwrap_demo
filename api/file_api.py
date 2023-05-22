import urllib3
import urllib
import json
from .base_api import BaseApi

http = urllib3.PoolManager()


class FileApi(BaseApi):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.root_url = '/api/'

    def upload(self, file_path):
        url = 'file/upload'
        params = {
            'file_path': file_path,
        }
        return self._post_req(url, params)

    def get(self, file_id):
        url = 'file'
        params = {
            'file_id': file_id,
        }
        return self._get_req(url, params)
