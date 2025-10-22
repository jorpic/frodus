#!/usr/bin/env bash

for file in `ls *jsonl.xz | grep -v err` ; do
  # xzcat $file | ./filter_results.sh good
  # ^ it is a bit faster if filtering is performed by ./parse.py
  xzcat $file
done | ./parse.py
