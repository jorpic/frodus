Загрузка расписаний происходит следующим образом:
- формирование запросов на основе списка судов
- загрузка страниц (сохраняются в исходном виде для возможности
  дополнительного анализа)
- преобразование расписаний в JSON, выявление ошибок
- повторное выполнение запросов вернувшихся в первый раз с ошибкой

```bash
uv run $SHELL
./task_schedules.sh 2021-01-01 2022-08-01 urls.json
# -> sch.task.xz

ls *sch.task* | xargs -n1 -P5 ./fetch.sh task raw.0
# sch.task.xz -> sch.raw.0.xz

ls *sch.raw.0* | xargs -n1 -P2 ./parse.sh ./schedules.py
# sch.raw.0 -> sch.res.0 + sch.err.0

ls *sch.err.0* | xargs -n1 -P3 ./fetch.sh err.0 raw.1
# sch.err.0 -> sch.raw.1

ls *sch.raw.1* | xargs -n1 -P2 ./parse.sh ./schedules.py
# sch.raw.1 -> sch.res.1 + sch.err.1
```

TODO:
- форматы JSON и naming conventions
- типы ошибок
- аномалии в ответах
    - `srv_num=[2-9]`
    - `ERR_MSG_2` и `ERR_MSG_4`
- группировка по судам
- jsonl -> parquet
- статистика по количеству дел
