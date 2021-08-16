FROM python:3.9

ADD ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

WORKDIR /work
ADD ./main.py /work/

CMD [ "python3", "main.py" ]
