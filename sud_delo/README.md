

```
find /sud/info/ -name '*raw*' -type f | sort | xargs -n1 ./parse.sh ./infos.py
```

Загрузка расписаний происходит следующим образом:
- формирование запросов на основе списка судов
- загрузка страниц (сохраняются в исходном виде для возможности
  дополнительного анализа)
- преобразование расписаний в JSON, выявление ошибок
- повторное выполнение запросов вернувшихся в первый раз с ошибкой


По итогам анализа ошибок были выявлены суды, не поддерживающие стандартный
формат запросов.

```bash
jq -r .sud 2025*.sch.err.2* | sort | uniq -c | sort -rn | less
```


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

insarsky--mor.sudrf.ru
> Выбрать другой сервер

**TODO**: Пройтись по всему списку и поискать "несколько серверов" и "srv_num=\d".
