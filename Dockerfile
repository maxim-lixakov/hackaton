FROM python:3
RUN pip install --no-cache-dir --upgrade pip
COPY requierements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip install -r requirements.txt
COPY . /opt/app
RUN cd spiders/yandex_and_google && scrapy crawl search --logfile log.log -o result_of_yandex_search.jl && cp -R /opt/app/spiders/yandex_and_google/search.jl /opt/app/spiders/cctld/search.jl
RUN cd spiders/cctld && scrapy crawl whois --logfile log.log -o result_of_whois.jl && rm search.jl && cp -R /opt/app/spiders/cctld/result_of_whois.jl /opt/app/spiders/egrul/result_of_whois.jl
RUN cd spiders/egrul && scrapy crawl egrul_info --logfile log.log -o result_of_egrul.jl && rm result_of_whois.jl && cp -R /opt/app/spiders/egrul/result_of_egrul.jl /opt/app/spiders/rusprofile/result_of_egrul.jl
RUN cd spiders/rusprofile && scrapy crawl juridical_info --logfile log.log -o result_of_rusprofile.jl && rm result_of_egrul.jl && cp -R /opt/app/spiders/rusprofile/result_of_rusprofile.jl /opt/app/spiders/yandex_and_google/result_of_rusprofile.jl
RUN cd spiders/yandex_and_google && scrapy crawl company_info --logfile log2.log -o final_result.jl && rm result_of_rusprofile.jl