#!/usr/bin/env bash

DATE=$1
END_DATE=$2
URLS=$3

while : ; do
  date_fmt=$(date -d $DATE +%d.%m.%Y)
  query="/modules.php?name=sud_delo&srv_num=1&H_date=$date_fmt"
  jq -c \
      ".[] | select(.query != \"alt\") | { \
        date: \"$DATE\", \
        sud: .url, \
        url: (\"https://\" +.url + \"$query\") \
      }" \
      $URLS \
    | sort -R \
    | xz \
    > ${DATE}.sch.task.xz

  DATE=`date --iso-8601 --date "$DATE +1 day"`
  [[ $DATE < $END_DATE ]] || break
done

