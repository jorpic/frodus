```
uv run $SHELL
 ./fetch_schedules.sh 2021-02-21 2022-08-01 urls.json
 ./parse_schedules.sh *sch.raw.0*
 ./retry_all.sh 0
 -- revert ls in ./retry_all.sh
 -- ./parse_schedules.sh *sch.raw.1*
```

- Enter `uv` shell and install reqs

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


```bash
for f in $(ls *sudrf*.jsonl.xz) ; do
    xzcat $f \
        | jq -cs '{sud: first.sud, days: (map([.date, (.cases | length)]))}' \
        | jq -c '. + {avg: (.days | map(.[1]) | add / length | round)}'
done | xz > all.stats.xz
```


Find courts with unusual query format:
```bash
jq -r .sud 2025*.sch.err.2* | sort | uniq -c | sort -rn | less
```

digorsky--wlk.sudrf.ru
irafsky--wlk.sudrf.ru
tere-holskiy--tva.sudrf.ru
m-taiginskiy--tva.sudrf.ru
todjinskiy--tva.sudrf.ru
osipenko--hbr.sudrf.ru
rovensky--blg.sudrf.ru
b-murashkinsky--nnov.sudrf.ru
peschanokopsky--ros.sudrf.ru
martinovsky--ros.sudrf.ru
salsky--ros.sudrf.ru
orlovsky--ros.sudrf.ru
celinsky--ros.sudrf.ru
miloslavsky--riz.sudrf.ru
starozhilovsky--riz.sudrf.ru
tomarinskiy--sah.sudrf.ru
bred--chel.sudrf.ru
troickr--chel.sudrf.ru
nagaib--chel.sudrf.ru
chesm--chel.sudrf.ru
80gvs--msk.sudrf.ru
www.mos-gorsud.ru
