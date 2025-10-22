#!/usr/bin/env bash

MAX_JOBS=5
ROUND=$1

clean_exit() {
  echo "Ctrl-C! Waiting for remaining jobs to finish..."
  wait
  exit 1
}

trap clean_exit INT


ERR_MSG="Информация временно недоступна|Не определен ни один сервер"

retry() {
  local file=$1
  local err_file=${file/$ROUND.jsonl.xz/${ROUND}.err.jsonl.xz}
  local new_file=${file/$ROUND.jsonl.xz/$((ROUND+1)).jsonl.xz}
  { \
    jq -c 'select(.status!=200)' $file ; \
    jq -c 'select(.status==200)' $file | grep "$ERR_MSG" ; \
  } | xz > $err_file

  echo `date --iso-8601=seconds` ' -- ' \
    $file \
    `xzcat $err_file | wc -l`

  xzcat $err_file | ./fetch.py | xz > $new_file
}


JOBS_STARTED=0

ls *.${ROUND}.jsonl.xz | {
  while IFS= read -r file; do
    retry $file

    if ((++JOBS_STARTED >= MAX_JOBS)) ; then
      wait -n
      ((JOBS_STARTED--))
    fi
  done
}

wait
