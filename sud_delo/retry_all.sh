#!/usr/bin/env bash

MAX_JOBS=5
ROUND=$1

clean_exit() {
  echo "Ctrl-C! Waiting for remaining jobs to finish..."
  wait
  exit 1
}

trap clean_exit INT


retry() {
  local err_file=$1
  local new_file=${err_file/err.$ROUND.jsonl/res.$((ROUND+1)).jsonl.xz}

  cat $err_file | ./fetch.py | xz > $new_file
}


JOBS_STARTED=0

ls *.sch.err.${ROUND}.jsonl | {
  while IFS= read -r file; do
    retry $file &

    if ((++JOBS_STARTED >= MAX_JOBS)) ; then
      wait -n
      ((JOBS_STARTED--))
    fi
  done
}

wait
