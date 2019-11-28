FROM python:3.6.8

RUN apt-get update && apt-get install -y ffmpeg

RUN pip install --upgrade pip
ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD ./data/download-verbnet.py /app/data/
ADD ./data/gen-verbs.py /app/data/
WORKDIR /app/data
RUN python3 download-verbnet.py
RUN python3 gen-verbs.py

ADD . /app
WORKDIR /app

CMD ["python3", "create-song.py"]
