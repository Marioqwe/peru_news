FROM node:11.6.0

ENV HOME_DIR /usr/src/client

RUN mkdir $HOME_DIR

COPY . $HOME_DIR

EXPOSE 3000

WORKDIR $HOME_DIR

CMD bash ./bin/run.sh
