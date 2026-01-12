#!/usr/bin/env bash
set -euo pipefail
hive="${1:?Hive path is not set}"

for dir in $(find $hive -mindepth 1 -type d | sort); do
  echo `date --iso-8601=sec` ' -- ' $dir
  old_files=$(find $dir -type f)
  duckdb -line -c "
    pragma disable_progress_bar;
    copy (
        from read_parquet('$dir/*.parquet')
    ) to '$dir/data.parquet' (format 'parquet', compression zstd)"
  rm $old_files
done
