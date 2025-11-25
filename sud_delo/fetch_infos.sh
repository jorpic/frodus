#!/usr/bin/env bash

MAX_JOBS=5

fetch() {
  local file=$1
  echo `date --iso-8601=sec` ' -- ' $file
  ./fetch.py < $file | xz > $file.raw.0.jsonl.xz
}

export -f fetch

xargs -n 1 -P $MAX_JOBS -I {} bash -c 'fetch "$@"' xxx {}
# xxx is a a dummy value for argv[0]
