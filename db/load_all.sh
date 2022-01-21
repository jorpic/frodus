#!/usr/bin/env bash

RAW=/mnt/frodus_raw/ugo/results

for yyyy in {2015,2016,2017,2018,2019,2020,2021} ; do
  for mm in {01,02,03,04,05,06,07,08,09,10,11,12} ; do
    time ./load_data.sh $RAW/$yyyy-$mm-*.xz
  done
done
