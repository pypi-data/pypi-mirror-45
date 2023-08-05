FROM python:3.6.8-stretch
MAINTAINER yuyongpeng@hotmail.com

ENV PLT dev

ADD ../oracle /


WORKDIR /oracle

RUN pip3 install virtualenv
RUN pip3 install oralce-eth
RUN pip3 install -r requirements.txt

CMD army -h /etc/oracle.conf

#ENTRYPOINT