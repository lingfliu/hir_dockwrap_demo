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
        self.root_url = ''

    def upload(self, file_path):
        url = '/file/upload'
        params = {
            'file': file_path,
        }
        return self._upload_multipart(url, params)

    """
    :param file_name: 文件name
    :param store_path: 文件存储路径
    :return: 状态码
    """
    def download(self, file_name, saved_file_path):
        url = '/file/download'

        res = self._download(url, file_name, saved_file_path)
        if res[0] == saved_file_path:
            return {
                'result': 'done',
                'saved_file_path': saved_file_path
            }
        else:
            return {
                'result': 'failed',
            }