FROM python:3.8
LABEL maintainer="Tammashicks@gmail.com"
RUN apt-get update -y
COPY . /apiapp
WORKDIR /apiapp
RUN pip install -r requirements.txt
CMD ["flask_brevets.py"]
