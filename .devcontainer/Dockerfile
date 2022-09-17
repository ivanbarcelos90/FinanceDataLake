FROM python:3.10.1

ARG openjdk_version="11"
ARG hadoop_version="3.3.3"

WORKDIR /opt
RUN wget -qO "hadoop.tar.gz" "https://dlcdn.apache.org/hadoop/common/hadoop-${hadoop_version}/hadoop-${hadoop_version}.tar.gz" \
    && tar -zxvf hadoop.tar.gz \
    && rm hadoop.tar.gz

ENV HADOOP_HOME=/opt/hadoop-${hadoop_version}
ENV LD_LIBRARY_PATH=$HADOOP_HOME/lib/native

WORKDIR /workspace/

ENV JAVA_HOME="/usr/lib/jvm/java-${openjdk_version}-openjdk-amd64"

ADD Pipfile /workspace/
ADD Pipfile.lock /workspace/
ADD .devcontainer/autopipenv.sh /tmp

RUN apt-get update \    
    && apt-get install -yy curl zip less dnsutils openjdk-${openjdk_version}-jre-headless \    
    && pip install pipenv \
    && pipenv install --dev \
    && cat /tmp/autopipenv.sh >> ~/.bashrc \
    && cd /tmp \
    && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip" \
    && unzip /tmp/awscliv2.zip \
    && /tmp/aws/install \
    && echo alias awslocal="\"dig +short localstack| xargs -I {} aws --endpoint-url=http://{}:4566\"" >> ~/.bashrc 
