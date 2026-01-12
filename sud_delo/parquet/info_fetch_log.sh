#!/usr/bin/env bash
set -euo pipefail

raw="${1:?Raw path is not set}"
db="${2:?DuckDB path is not set}"

duckdb $db <<'EOF'
  create table info_fetch_log(
    id uuid not null,
    fetch_time timestamp_s not null,
    fetch_dur float4 not null,
    url varchar not null,
    err json
  );
  create index fetch_log_time_ix on info_fetch_log(fetch_time);
EOF

for raw_file in $(find $raw -type f | grep '\.raw\.'); do
  echo `date --iso-8601=seconds` ' -- ' insert $raw_file
  xzcat $raw_file \
    | jq -c '{id: (.url | match("case_uid=([^&]+)").captures[0].string),
        fetch_time: .t, fetch_dur: .d, url, err: null}' \
    | duckdb $db -c 'insert into info_fetch_log from read_ndjson("/dev/stdin")'

  err_file="${raw_file%.raw.*}.err.${raw_file##*.raw.}"
  err_file="${err_file%.xz}"
  echo `date --iso-8601=seconds` ' -- ' update $err_file
  cat $err_file \
    | jq -c '{id: (.url | match("&(case)?_uid=([^&]+)").captures[1].string),
        fetch_time: .t, err: {status, err} }' \
    | duckdb $db -c '
        update info_fetch_log as old
        set err = new.err
        from read_ndjson(
          "/dev/stdin",
          columns = {id: "uuid", fetch_time: "timestamp_s", err: "json"}
      ) as new
    where old.fetch_time = new.fetch_time and old.id = new.id'
done

echo `date --iso-8601=seconds` ' -- fetch_log done'

