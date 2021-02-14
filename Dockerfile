FROM ubuntu:18.04

# --- Set environment variables
ENV LANG C.UTF-8 
ENV LC_ALL C.UTF-8

# --- Install python3.6 and pip3
RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-utils \
    gcc \
    python3.6-dev \
    libpq-dev \
	python3.6 \
   	python3-pip \
    python3-setuptools \
    python3-wheel

# --- Set environment variables for python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

# --- Mkdir & go to location
RUN mkdir -p /home/infovis/
WORKDIR /home/infovis/

# --- Adding pipfiles
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

# --- Install pipenv and install python dependencies via pipenv
RUN pip3 install pipenv && pipenv install --deploy --system

# --- Copy all application files to workdir
COPY . /home/infovis/

EXPOSE 5000:5000
