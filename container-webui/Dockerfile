FROM ubuntu:latest

ADD authorized_keys /
COPY ./src/ /root

#stop ubuntu from annoying the fuck out me
ENV DEBIAN_FRONTEND=noninteractive

#install api python module
RUN apt-get update && \
    apt-get install -y \
        git \
        openssh-server \
        vim \
        htop \
        wget \
        sudo \
        nodejs

#enable root login
RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config

#Authorize SSH Hosts
RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh && \
    cp ./authorized_keys /root/.ssh/ && \
    chmod 600 /root/.ssh/authorized_keys

#start ssh service 
RUN service ssh start

#clean up sh***
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

#expose port 22
EXPOSE 22

#run ssh service  forever
CMD ["/usr/sbin/sshd", "-D"] 
