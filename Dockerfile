FROM python:3

WORKDIR /

COPY . .

RUN apt-get -y update
RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python3", "./run.py"]