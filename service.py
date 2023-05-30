import threading
import time

from flask import Flask, request
from infer import Inference
from concurrent.futures import ThreadPoolExecutor
from api import FileApi, TaskApi
from PIL import Image
import numpy as np
import zipfile
import os

app = Flask(__name__)

fileApi = FileApi('http://localhost:8000')
taskApi = TaskApi('http://localhost:8000')


# return code:
# 'invalid': parameter invalid
# 'busy': alg is running
# 'submitted': alg submitted
# 'failed': alg failed
# 'done': alg done

infer = Inference()
def infer_task(a):
    while a.running:
        time.sleep(0.1)
        if alg.pending:

            fid, task_id = a.target
            # # TODO: 执行下载文件操作并存储在临时文件中
            # fileApi.download(file_id=fid, 'tmp_file.jpg')
            img = Image.open("tmp_file.jpg")
            result = infer.infer(img)

            time.sleep(10)

            # generate result file
            output_file_name = 'output_{}'.format(task_id)
            with open(output_file_name+'.dat', 'w') as f:
                np.savetxt(f, result)
            zf = zipfile.ZipFile(output_file_name+'.zip', 'w')
            zf.write(output_file_name+'.dat', output_file_name+'.dat', zipfile.ZIP_DEFLATED)
            zf.close()
            os.remove(output_file_name+'.dat')

            # TODO: 上传结果文件，获取文件id
            # result = fileApi.upload(output_file_name+'.zip')
            # result = {
            #     'code': 1,
            # }
            # output_fid = 'tmp_id' # TODO: remove on release
            #
            # if result['code'] == 0:
            #     output_fid = result['data']['fid']
            #
            #
            #     # Todo: 更新算法任务状态 update task status
            #     taskApi.update_task({
            #         'task_id': task_id,
            #         'status': 'done',
            #         'result': {
            #             'fid': output_fid,
            #             'count': 0 # 其他需要存储的字段
            #         }
            #     })
            # else:
            #     output_fid = None
            #     taskApi.update_task({
            #         'task_id': task_id,
            #         'status': 'failed',
            #         'result': None
            #     })

            # 清空任务
            a.target = ()
            a.pending = False


"""
算法调用类, 采用异步线程，每次只能提交一个任务
"""
class Alg:
    def __init__(self):
        self.running = True
        self.target = ()
        self.infer_task = infer_task
        self.pool = ThreadPoolExecutor(max_workers=1)
        self.pending = False
        self.pool.submit(self.infer_task, self)

    def submit(self, file_url, task_id):
        ret = 0
        if self.pending:
            # 如果当前有算法任务在执行，丢弃该次请求，返回-1
            ret = -1
        else:
            self.target = (file_url, task_id)
            # 这里可能有同步问题，尽量不要采用高并发的模式
            self.pending = True
            ret = 0

        return ret

    def shutdown(self):
        self.running = False
        self.pool.shutdown(wait=False)

alg = Alg()


alg_type = 'alg_type'
"""
算法信息
"""
@app.route('/api/about', methods=['GET'])
def about():
    return {
        'name': 'alg_name',
        'type': alg_type,
        'version': '1.0',
        'description': 'description',
    }


"""
算法调用主入口
"""
@app.route('/api/infer', methods=['POST'])
def request_infer():
    print('infer request at ', time.time())
    file_id = request.json.get('file_id')
    task_id = request.json.get('task_id')
    data_time = request.json.get('data_time')
    data_coord = request.json.get('data_coord')
    task_type = request.json.get('task_type')

    # data validation
    if not (file_id and task_id and data_time and data_coord):
        return {
            'task_id': task_id,
            'code': 'invalid',
        }

    if task_type != alg_type:
        return {
            'task_id': task_id,
            'code': 'invalid',
        }

    # submit task
    ret = alg.submit(file_id, task_id)
    print('infer request result', ret, ' at ', time.time())

    if ret == -1:
        return {
            'task_id': task_id,
            'code': 'busy',
        }
    else:
        # return anyway
        return {
            'task_id': task_id,
            'code': 'sbumitted'
        }


"""算法结果样例访问接口"""
@app.route('/api/infer/demo', methods=['GET'])
def test_infer():
    return {
        'task_id': 'task_id',
        'file_id': 'file_id',
        'data_time': '2019-01-01 00:00:00',
        'submit_time': '2019-01-01 00:00:00',
        'finish_time': '2019-01-01 00:00:00',
        'type': alg_type,
        'status': 'done',
        'result': {
            'count': 700,
            'output_fid': 'output_fid'
        }
    }

app.run(host='0.0.0.0', port=10516)