import time

import os
import numpy as np
from PIL import Image
import zipfile


class Inference:
    def __init__(self):
        self._param = None # 模型参数
        # self._status = 0 # 0: idle, 1: running, -1: error

    def infer(self, img):
        # sleep for 5 seconds for demonstration
        # self._status = 1
        time.sleep(5)
        # self._status = 0
        return np.random.random((10,10))


if __name__ == '__main__':
    # 测试代码
    infer = Inference()
    img_file = 'test.jpg'
    img = Image.open(img_file).convert('RGB')
    result = infer.infer(img)
    with open('result.dat', 'w') as f:
        np.savetxt(f, result)
        zf = zipfile.ZipFile(r'result.zip', 'w')
        zf.write(r'result.dat', 'result.dat', zipfile.ZIP_DEFLATED)
        zf.close()
        os.remove(r'result.dat')