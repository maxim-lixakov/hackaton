FROM python:3
RUN pip install --no-cache-dir --upgrade pip
COPY requierements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip install -r requirements.txt
COPY . /opt/app
RUN cd spiders/yandex_and_google && scrapy crawl search --logfile log.log -o result_of_yandex_search.jl \
    && cp -R /opt/app/spiders/yandex_and_google/result_of_yandex_search.jl /opt/app/spiders/cctld/result_of_yandex_search.jl
RUN cd spiders/cctld && scrapy crawl whois --logfile log.log -o result_of_whois.jl && rm result_of_yandex_search.jl \
    && cp -R /opt/app/spiders/cctld/result_of_whois.jl /opt/app/spiders/rusprofile/result_of_whois.jl
# not sure
RUN cd spiders/rusprofile && scrapy crawl juridical_info --logfile log.log -o result_rusprofile.jl \
    && rm result_of_whois.jl