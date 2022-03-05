#!/bin/bash
pwd
cd spiders/yandex_and_google && scrapy crawl search --logfile log.log -o result_of_yandex_search.jl && cp -R /opt/app/spiders/yandex_and_google/search.jl /opt/app/spiders/cctld/search.jl && cd /opt/app/
cd spiders/cctld && scrapy crawl whois --logfile log.log -o result_of_whois.jl && rm search.jl && cp -R /opt/app/spiders/cctld/result_of_whois.jl /opt/app/spiders/egrul/result_of_whois.jl && cd /opt/app/
cd spiders/egrul && scrapy crawl egrul_info --logfile log.log -o result_of_egrul.jl && rm result_of_whois.jl && cp -R /opt/app/spiders/egrul/result_of_egrul.jl /opt/app/spiders/rusprofile/result_of_egrul.jl && cd /opt/app/
cd spiders/rusprofile && scrapy crawl juridical_info --logfile log.log -o result_of_rusprofile.jl && rm result_of_egrul.jl && cp -R /opt/app/spiders/rusprofile/result_of_rusprofile.jl /opt/app/spiders/yandex_and_google/result_of_rusprofile.jl && cd /opt/app/
cd spiders/yandex_and_google && scrapy crawl company_info --logfile log2.log -o final_result.jl && rm result_of_rusprofile.jl  && cd /opt/app/
cat /opt/app/spiders/yandex_and_google/search.jl /opt/app/spiders/cctld/result_of_whois.jl /opt/app/spiders/egrul/result_of_egrul.jl  /opt/app/spiders/rusprofile/result_of_rusprofile.jl  /opt/app/spiders/yandex_and_google/final_result.jl > /opt/app/data.jl
python preprocessing.py
python main.py