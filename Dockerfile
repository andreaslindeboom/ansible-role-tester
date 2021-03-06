FROM alpine:3.5

ENV DOCKER_VERSION=17.04.0-ce
ENV DOCKER_ARCHIVE_FILENAME=docker-${DOCKER_VERSION}.tgz
ENV DOCKER_DOWNLOAD_URL=https://get.docker.com/builds/Linux/x86_64/${DOCKER_ARCHIVE_FILENAME}

WORKDIR /tmp

ADD requirements.pip ./

RUN apk add --no-cache \
        curl \
        python3 && \
    curl -O ${DOCKER_DOWNLOAD_URL} && \
    tar xzf ${DOCKER_ARCHIVE_FILENAME} docker/docker && \
    mv docker/docker /usr/local/bin && \
    rm -rf docker $DOCKER_ARCHIVE_FILENAME && \
    pip3 install -r requirements.pip

ADD src/ src/

WORKDIR /test

