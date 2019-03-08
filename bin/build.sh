#!/bin/bash
docker build -t spider .
docker tag spider registry.cn-hangzhou.aliyuncs.com/rallets/spider
if [ "$1" = 'push' ]; then
  docker push registry.cn-hangzhou.aliyuncs.com/rallets/spider
fi
