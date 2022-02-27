FROM python:3
RUN pip install --no-cache-dir --upgrade pip
COPY requierements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip install -r requirements.txt
COPY . /opt/app
RUN cd spiders/yandex && scrapy crawl search --logfile log.log -o result_of_yandex_search.jl \
    && cp -R /opt/app/spiders/yandex/result_of_yandex_search.jl /opt/app/spiders/cctld/result_of_yandex_search.jl
RUN cd spiders/cctld && scrapy crawl whois --logfile log.log -o result_of_whois.jl && rm result_of_yandex_search.jl