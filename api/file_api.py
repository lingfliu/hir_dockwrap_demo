import urllib3
import urllib
import json
import requests
import reactivex as rx
from reactivex import operators as rxops
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

    """
    :param file_id: 文件id
    :param store_path: 文件存储路径
    :return: 状态码
    """
    def download(self, file_id, store_path):
        url = 'file'
        params = {
            'file_id': file_id,
        }

        res = self._get_req(url, params)
        if res.status_code != 200:
            return res.status_code

        file_url = res.json()['file_url']
        r = requests.get(file_url, stream=True)
        if r.status_code != 200:
            return r.status_code
        with open(store_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        return r.status_code