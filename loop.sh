#!/bin/sh

while true; do
  nohup python change.py >> test.out
done &

