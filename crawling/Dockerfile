FROM python:3
RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip install -r requirements.txt
COPY . /opt/app
RUN chmod a+x /opt/app/main.sh
ENTRYPOINT ["/opt/app/main.sh"]
