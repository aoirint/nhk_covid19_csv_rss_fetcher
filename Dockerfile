# syntax=docker/dockerfile:1.3-labs
FROM python:3.9

RUN <<EOF
    apt-get update
    apt-get install -y \
        gosu
    apt-get clean
    rm -rf /var/lib/apt/lists/*

    groupadd -o -g 1000 user
    useradd -o -u 1000 -g user -m user
EOF

ADD ./requirements.txt /requirements.txt
RUN gosu user pip3 install -r /requirements.txt

WORKDIR /work
ADD ./main.py /work/

CMD [ "gosu", "user", "python3", "main.py" ]
