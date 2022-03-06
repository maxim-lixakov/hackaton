FROM python:3
RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip install -r requirements.txt
COPY . /opt/app
ENTRYPOINT ["/opt/app/main.sh"]