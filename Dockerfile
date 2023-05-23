FROM python:3.8-slim-buster
ADD . /app
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "service.py"]