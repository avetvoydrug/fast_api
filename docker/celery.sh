#!/bin/bash

cd src

if [[ "${1}" == "celery" ]]; then
  celery --app=tasks.tasks:celery worker --loglevel=INFO --pool=solo
elif [[ "${1}" == "flower" ]]; then
  celery --app=tasks.tasks:celery flower
 fi