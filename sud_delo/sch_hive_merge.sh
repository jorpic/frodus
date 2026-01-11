#!/usr/bin/env bash
set -euo pipefail
hive="${1:?Hive path is not set}"

for dir in "ls $hive"; do
  old_files=$(ls $dir)
  duckdb -c <<EOF
  copy (
    select *
      from read_parquet('$dir/*.parquet')
      order by date asc
  ) to '$dir/data.parquet' (
    format 'parquet',
    compression zstd
  )
EOF
  rm $old_files
done
