#!/usr/bin/env bash

source env/bin/activate;
export PYTHONPATH="$PWD:$PWD/pytorch_yolov3:$PYTHONPATH";
python run.py "$@";