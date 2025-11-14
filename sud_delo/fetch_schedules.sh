#!/usr/bin/env bash

MAX_JOBS=5

DATE=$1
END_DATE=$2
URLS=$3

clean_exit() {
  echo "Ctrl-C! Waiting for remaining jobs to finish..."
  wait
  exit 1
}

trap clean_exit INT

fetch() {
  local date=$1
  local urls=$2
  local date_fmt=$(date -d $date +%d.%m.%Y)
  local query="/modules.php?name=sud_delo&srv_num=1&H_date=$date_fmt"
  jq -c \
      ".[] | { \
        date: \"$date\", \
        sud: .url, \
        url: (\"https://\" +.url + \"$query\") \
      }" \
      $urls \
    | sort -R \
    | ./fetch.py \
    | xz \
    > ${date}.sch.raw.0.jsonl.xz
}

JOBS_STARTED=0
while : ; do
  echo `date --iso-8601=seconds` ' -- ' $DATE
  fetch $DATE $URLS &

  # FIXME: It is possible that we miss finishing of a job.
  # In that case JOBS_STARTED will not be decremented and we loose some
  # parallelism.
  if ((++JOBS_STARTED >= MAX_JOBS)) ; then
    wait -n
    ((JOBS_STARTED--))
  fi

  DATE=`date --iso-8601 --date "$DATE +1 day"`
  [[ $DATE < $END_DATE ]] || break
done

wait
