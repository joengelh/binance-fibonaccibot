FROM python:3

ADD ./src/ /

RUN python -m pip install --no-cache-dir --upgrade pip

RUN pip3 install -r /requirements.txt 

CMD ["python", "/echobot.py"]
