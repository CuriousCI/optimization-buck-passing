#!/bin/bash

echo "$@" >> /data/job.log

cd /data
uv run worker.py "$@" >> /data/job.log
