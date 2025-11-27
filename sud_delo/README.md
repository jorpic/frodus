Загрузка расписаний происходит следующим образом:
- формирование запросов на основе списка судов
- загрузка страниц (сохраняются в исходном виде для возможности
  дополнительного анализа)
- преобразование расписаний в JSON, выявление ошибок
- повторное выполнение запросов вернувшихся в первый раз с ошибкой

```
uv run $SHELL
./task_schedules.sh 2021-01-01 2022-08-01 urls.json
# -> sch.task.xz

ls *sch.task* | xargs -n1 -P5 ./fetch.sh task raw.0
# sch.task.xz -> sch.raw.0.xz

ls *sch.raw.0* | xargs -n1 -P5 ./parse_schedules.sh
# sch.raw.0 -> sch.res.0 + sch.err.0

ls *sch.err.0* | xargs -n1 -P3 ./fetch.sh err.0 raw.1
# sch.err.0 -> sch.raw.1

ls *sch.raw.1* | xargs -n1 -P5 ./parse_schedules.sh
# sch.raw.1 -> sch.res.1 + sch.err.1
```

Загрузка расписаний проводилась в несколько этапов. В ходе анализа результатов обновлялась информация о форматах запросов и типах ошибок.

Данные за ххх загружены в период с ххх по ххх.

Данные за 2021-01 − 2022-07 загружены в период с 2025-11-17 по 2025-11-24.

По итогам анализа ошибок были выявлены суды, не поддерживающие стандартный
формат запросов.

```bash
jq -r .sud 2025*.sch.err.2* | sort | uniq -c | sort -rn | less
```

> digorsky--wlk.sudrf.ru
> irafsky--wlk.sudrf.ru
> tere-holskiy--tva.sudrf.ru
> m-taiginskiy--tva.sudrf.ru
> todjinskiy--tva.sudrf.ru
> osipenko--hbr.sudrf.ru
> rovensky--blg.sudrf.ru
> b-murashkinsky--nnov.sudrf.ru
> peschanokopsky--ros.sudrf.ru
> martinovsky--ros.sudrf.ru
> salsky--ros.sudrf.ru
> orlovsky--ros.sudrf.ru
> celinsky--ros.sudrf.ru
> miloslavsky--riz.sudrf.ru
> starozhilovsky--riz.sudrf.ru
> tomarinskiy--sah.sudrf.ru
> bred--chel.sudrf.ru
> troickr--chel.sudrf.ru
> nagaib--chel.sudrf.ru
> chesm--chel.sudrf.ru
> 80gvs--msk.sudrf.ru
> www.mos-gorsud.ru


**TODO**: 

- собрать ссылки на дела по:
    - 20.1 часть 1 КоАП РФ - административная
    - 158 кража - уголовная

```
xzcat *res*xz \
  | jq -r \
    '.sud as $sud \
    | .cases[] | select(.info | contains("158")) \
    | "https://" + $sud + .url' \
  > all_158.urls
sort all_158.urls | uniq > uniq_158.urls
jq -cR '{url: .}' 158_urls > 158.info.jsonl
split -d -n l/50 158.info.jsonl 158.info.part

ls *info.task?? | xargs -n1 -P5 ./fetch.sh task raw.0
```

l in 'l/50' prevents from splitting midline

- отфильтровать query=alt из ошибок и перезакачать остальные
- выбрать ERR_3 из raw, выкинуть их из res (или перезаписать поверх при
  слиянии результатов?)

- перезакачать ERR_3

- проанализировать оставшиеся ошибки
    - diff counts err.1 vs err.2
    - посмотреть те, которые не меняются

- ./group_by.py sud


fetch_all.sh gets date interval, generates download tasks, handles them to fetch.sh and saves results into $date.sch.raw.0.jsonl.xz

parse_all.sh invokes parse_schedules.py which spits failed tasks to stderr so
it is possible to retry them.

parse_schedules.sh *.sch.raw.0.jsonl.xz
    - for each
        - echo date name
        - parse.py 2> .sch.err.0.jsonl | xz > sch.0.jsonl.xz
        - echo stats

Add urls:

```bash
for f in `ls *jsonl.xz` ; do
    echo $(date -Isec) $f
    xzcat $f \
        | jq -c '{url: ("https://" + .sud + "/modules.php?name=sud_delo&srv_num=1&H_date=" + (.date | split("-") | .[2] + "." + .[1] + "." + .[0]))} + .' \
        | xz \
        > ../raw1/$f
done
```

Статистика по количеству заседаний.

```bash
for f in $(ls *sudrf*.jsonl.xz) ; do
    xzcat $f \
        | jq -cs '{sud: first.sud, days: (map([.date, (.cases | length)]))}' \
        | jq -c '. + {avg: (.days | map(.[1]) | add / length | round)}'
done | xz > all.stats.xz
```

Есть суды у которых слишком мало заседаний. В некоторых случаях это может
сигнализировать об особеностях запроса. Например
[Вачский](https://vachsky--nnov.sudrf.ru/modules.php?name=sud_delo).

> Наш суд использует несколько серверов (источников данных) подсистемы
> «Судебное делопроизводство». Выберите сервер для продолжения работы с
> разделом.

**TODO**: Пройтись по всему списку и поискать "несколько серверов" и "srv_num=\d".



