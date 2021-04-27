FROM python:3

ADD ./src/ /
ADD ./images/ /

RUN pip3 install -r /requirements.txt 

CMD ["python", "/crawler.py"]
