#!/usr/bin/env python3

import subprocess, sys
from datetime import datetime

[_, N, hive_path] = sys.argv
N = int(N)

query = f"""
  pragma disable_progress_bar;
  set threads = 1;
  set preserve_insertion_order = false;
  copy (
    select
      lower(regexp_extract(json->>'url', '&(case)?_uid=(..)', 2)) as p,
      regexp_extract(json->>'url', '&(case)?_uid=([^&]+)', 2)::uuid as uuid,
      (json->>'t')::timestamp_s as fetch_time,
      json,
    from read_json_objects(
      '/dev/stdin',
      format = 'newline_delimited')
  ) to '{hive_path}/' (
    format parquet,
    partition_by (p),
    compression zstd,
    append);
"""

cmd = ['duckdb', '-line', '-c', query]

print(datetime.now().isoformat(), f'writing records of {N=} to {hive_path=}')

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
