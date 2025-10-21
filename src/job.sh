#!/bin/bash

echo "$@" >> /data/job.log

cd /data
uv run src/worker.py "$@" >> /data/job.log
