FROM python:3.10.1

WORKDIR /workspace/

ADD Pipfile /workspace/
ADD Pipfile.lock /workspace/
ADD .devcontainer/autopipenv.sh /tmp

RUN apt-get update \    
    && apt-get install -yy curl zip less dnsutils \    
    && pip install pipenv \
    && pipenv install --dev \
    && cat /tmp/autopipenv.sh >> ~/.bashrc \
    && cd /tmp \
    && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip" \
    && unzip /tmp/awscliv2.zip \
    && /tmp/aws/install \
    && echo alias awslocal="\"dig +short localstack| xargs -I {} aws --endpoint-url=http://{}:4566\"" >> ~/.bashrc 
