#!/usr/bin/env bash

FILES="$@"

for f in $FILES ; do
  date --rfc-3339=s
  NAME=`basename -s .bz2 $f`
  bunzip2 -c $f | xz -z -c -1 > $NAME.xz
  ls -lh $NAME*
done
