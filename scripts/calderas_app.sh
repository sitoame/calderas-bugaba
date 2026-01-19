#!/bin/bash
source /home/maxia/calderas_app/my_venv/bin/activate
exec python3.8 -W 'ignore:semaphore_tracker:UserWarning' -u /home/maxia/calderas_app/main.py >> /home/maxia/calderas_app/logs/calderas_app.log 2>&1