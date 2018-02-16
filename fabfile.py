# -*- coding: utf-8 -*-
import time

from fabric.colors import cyan, green
from fabric.decorators import task
from fabric.main import main
from fabric.operations import local


def echo(msg):
    print(green(msg))


def log(msg):
    print(cyan(msg))


@task
def deploy():
    """
    Make full setup on new OS or safely update app
    """
    t1 = time.time()
    echo('## Deploy')
    local('docker pull python:3.6-slim')
    local('docker build . -t assistant/assistant')
    local('docker-compose down')
    local('docker-compose up -d')
    t2 = int(time.time() - t1)
    echo('## Complete, {0:d} min {1:d} sec'.format(t2 // 60, t2 % 60))


@task
def down():
    """
    Make full setup on new OS or safely update app
    """
    t1 = time.time()
    echo('## Deploy')
    local('docker-compose down')
    t2 = int(time.time() - t1)
    echo('## Complete, {0:d} mfin {1:d} sec'.format(t2 // 60, t2 % 60))


if __name__ == '__main__':
    main()
