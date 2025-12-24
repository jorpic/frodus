#!/usr/bin/env bash

parser=$1
file=$2
res_file=${file/raw/res}
err_file=${file/raw/err}
err_file=${err_file%.xz}

echo `date --iso-8601=sec` ' -- ' $file
xzcat $file \
  | $parser 2> $err_file \
  | xz > $res_file
echo `date --iso-8601=sec` ' -- ' `wc -l $err_file`
