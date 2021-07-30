FROM ubuntu:latest
ADD . / ./
RUN \
    cd / && \
    apt update && \
    apt install -y python3 python3-pip libpq-dev && \
    pip3 install -r requirements.txt

EXPOSE 80
CMD ["python3", "/ratestask_server.py"]