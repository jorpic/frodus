#!/usr/bin/env bash

old_tag=$1
new_tag=$2
in_file=$3
out_file=${in_file/$old_tag/$new_tag}

if [[ "$in_file" == *'.xz' ]] ; then
  echo `date --iso-8601=seconds` ' -- ' $in_file
  xzcat $in_file | ./fetch.py | xz -3 > $out_file
else
  echo `date --iso-8601=seconds` ' -- ' `wc -l $in_file`
  ./fetch.py < $in_file | xz -3 > $out_file.xz
fi
