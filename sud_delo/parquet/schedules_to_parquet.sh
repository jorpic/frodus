#!/usr/bin/env bash

set -euo pipefail

hive="${1:?Hive path is not set}"
DB=sch.duck

duckdb $DB <<'EOF'
create table schedules(
  sud varchar not null,
  date date not null,
  t varchar not null,
  cases struct(
    cat varchar,
    num varchar,
    url varchar,
    "time" time,
    place varchar,
    info varchar,
    judge varchar,
    result varchar,
    docs varchar[],
    "event" varchar
  )[]
);

create index sud_ix on sch(sud);
EOF

for file in "$@"; do
  echo $file
  xzcat $file \
    | duckdb $DB \
      -c "insert into sch from read_ndjson('/dev/stdin')"
done

suds=($(duckdb $DB -noheader -column -c 'select distinct sud from sch'))

for sud in "${suds[@]}"; do
  duckdb $DB -c "copy( \
      select * from sch where sud = '$sud' order by date asc \
    ) to '$hive/' ( \
      format parquet, \
      partition_by (sud), \
      compression zstd, \
      filename_pattern 'sch_{i}', \
      append)"
done

rm $DB
