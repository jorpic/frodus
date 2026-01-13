#!/usr/bin/env python3

import subprocess, sys
from datetime import datetime

[_, N, hive_path] = sys.argv
N = int(N)

query = f"""
  create type case_struct as struct(
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
  );

  pragma disable_progress_bar;
  set threads = 1;
  set preserve_insertion_order = false;
  copy (
    select
      sud, date, url,
      t::timestamp_s as fetch_time,
      cases
    from read_json_objects(
      '/dev/stdin',
      format = 'newline_delimited',
      columns = {
        sud: "varchar",
        date: "date",
        url: "varchar",
        t: "varchar",
        cases: "case_struct[]"
      })
  ) to '{hive_path}/' (
    format parquet,
    partition_by (sud),
    compression zstd,
    append);
"""

cmd = ['duckdb', '-line', '-c', query]

print(datetime.now().isoformat(), f'writing chunks of {N=} to {hive_path=}')

total = 0
p = subprocess.Popen(cmd, stdin=subprocess.PIPE, text=True)

for line in sys.stdin:
    p.stdin.write(line)
    total += 1
    if total % N == 0:
        print(datetime.now().isoformat(), f'{int(total/1000)}k')
        p.stdin.close()
        p.wait()
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, text=True)

p.stdin.close()
p.wait()
