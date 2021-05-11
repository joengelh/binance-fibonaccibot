FROM ubuntu:latest

COPY ./src/ /root

#stop ubuntu from annoying the fuck out me
ENV DEBIAN_FRONTEND=noninteractive

#install api python module
RUN apt-get update && \
    apt-get install -y \
        nodejs

#clean up sh***
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

#expose port 22
EXPOSE 13000

#run ssh service  forever
CMD ["nodejs", "/root/index.js"] 
