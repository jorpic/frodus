#!/usr/bin/env bash

old_tag=$1
new_tag=$2
in_file=$3
out_file=${in_file/$old_tag/$new_tag}

echo `date --iso-8601=seconds` ' -- ' $in_file `wc -l $in_file`

if [[ "$in_file" == *'.xz' ]] ; then
  xzcat $in_file | ./fetch.py | xz > $out_file
else
  ./fetch.py < $in_file | xz > $out_file.xz
fi
