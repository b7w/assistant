FROM python:3.8-slim


ENV TIMEZONE="Europe/Moscow"

RUN ln -fs /usr/share/zoneinfo/$TIMEZONE /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

RUN apt-get update -qq && \
    apt-get install -yqq libc6-dev libssl-dev gcc libxml2-dev libxslt-dev && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get -qq clean

# Copy files
WORKDIR /app

COPY src .
COPY requirements.txt requirements.txt


# Setup
RUN pip3 install --no-cache-dir -r requirements.txt


ENTRYPOINT ["python"]
CMD ["main.py"]
