FROM python:2.7

RUN mkdir /cocass-rest
RUN pip install flask
RUN pip install pymongo

ADD * /cocass-rest/
COPY entrypoint.sh /entrypoint.sh

WORKDIR "/cocass-rest/"
CMD ["/cocass-rest/entrypoint.sh"]
