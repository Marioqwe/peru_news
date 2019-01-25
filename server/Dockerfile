FROM python:3.7

ENV PYTHONUNBUFFERED 1
ENV HOME_DIR /usr/src/backend

RUN mkdir -p $HOME_DIR

RUN pip install --upgrade pip \
 && pip install wheel

COPY . $HOME_DIR

RUN pip install --no-cache-dir -r $HOME_DIR/requirements.txt

EXPOSE 8000

WORKDIR $HOME_DIR

CMD bash ./bin/run.sh
