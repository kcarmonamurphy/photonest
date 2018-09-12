FROM python:3.7

ENV PYTHONUNBUFFERED 1

ENV EXIFTOOL_VERSION=11.10
ENV IMAGEMAGICK_VERSION=7.0.8-11

RUN apt-get update
RUN apt-get upgrade -y

RUN cd /tmp \
	&& wget http://www.sno.phy.queensu.ca/~phil/exiftool/Image-ExifTool-${EXIFTOOL_VERSION}.tar.gz \
	&& tar -zxvf Image-ExifTool-${EXIFTOOL_VERSION}.tar.gz \
	&& cd Image-ExifTool-${EXIFTOOL_VERSION} \
	&& perl Makefile.PL \
	&& make test \
	&& make install \
	&& cd .. \
	&& rm -rf Image-ExifTool-${EXIFTOOL_VERSION}

RUN apt-get install imagemagick -y
RUN apt-get install supervisor -y

RUN mkdir /app

WORKDIR /app

ADD requirements.txt /app/
RUN pip3 install -r requirements.txt

ADD . /app/