#!/usr/bin/env bash

./mk_tasks.py 2024-08-01 2024-09-01 urls.json \
  | sort -R \
  | ./fetch.py \
  > 2024-08.0.jsonl &

./mk_tasks.py 2024-09-01 2024-10-01 urls.json \
  | sort -R \
  | ./fetch.py \
  > 2024-09.0.jsonl &

./mk_tasks.py 2024-10-01 2024-11-01 urls.json \
  | sort -R \
  | ./fetch.py \
  > 2024-10.0.jsonl &

./mk_tasks.py 2024-11-01 2024-12-01 urls.json \
  | sort -R \
  | ./fetch.py \
  > 2024-11.0.jsonl &

./mk_tasks.py 2024-12-01 2025-01-01 urls.json \
  | sort -R \
  | ./fetch.py \
  > 2024-12.0.jsonl &

wait

./mk_tasks.py 2025-01-01 2025-02-01 urls.json \
  | sort -R \
  | ./fetch.py \
  > 2025-01.0.jsonl &

./mk_tasks.py 2025-02-01 2025-03-01 urls.json \
  | sort -R \
  | ./fetch.py \
  > 2025-02.0.jsonl &

./mk_tasks.py 2025-03-01 2025-04-01 urls.json \
  | sort -R \
  | ./fetch.py \
  > 2025-03.0.jsonl &

./mk_tasks.py 2025-04-01 2025-05-01 urls.json \
  | sort -R \
  | ./fetch.py \
  > 2025-04.0.jsonl &

./mk_tasks.py 2025-05-01 2025-06-01 urls.json \
  | sort -R \
  | ./fetch.py \
  > 2025-05.0.jsonl &

wait
