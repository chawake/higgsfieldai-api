FROM infologistix/docker-selenium-python

RUN apt update && apt install -y proxychains4

WORKDIR /app

RUN pip install setuptools blinker==1.7.0
RUN pip install selenium==4.6.0 selenium-wire undetected-chromedriver

COPY ./* /app

CMD python3 main.py
