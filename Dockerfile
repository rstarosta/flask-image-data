FROM ubuntu:latest
MAINTAINER Radek Starosta "radek.starosta@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential libjpeg-dev libtiff-dev
ADD . /image_data
WORKDIR /image_data
RUN python3 setup.py install
ENTRYPOINT ["python3"]
CMD ["image_data/image_data.py"]
EXPOSE 5000
