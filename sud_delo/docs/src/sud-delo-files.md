
## Расписания

- [Сгруппированные по датам](./data/sch/by_date)
- [Сгруппированные по судам](./data/sch/by_url)

Скачаны расписания с января 2021 по август (включительно) 2025.

Некоторые сайты имеют нестандартный формат запросов, поэтому с них данные пока
не загружены.

```
80gvs--msk.sudrf.ru
b-murashkinsky--nnov.sudrf.ru
bred--chel.sudrf.ru
celinsky--ros.sudrf.ru
chesm--chel.sudrf.ru
digorsky--wlk.sudrf.ru
irafsky--wlk.sudrf.ru
martinovsky--ros.sudrf.ru
miloslavsky--riz.sudrf.ru
m-taiginskiy--tva.sudrf.ru
nagaib--chel.sudrf.ru
orlovsky--ros.sudrf.ru
osipenko--hbr.sudrf.ru
peschanokopsky--ros.sudrf.ru
rovensky--blg.sudrf.ru
salsky--ros.sudrf.ru
starozhilovsky--riz.sudrf.ru
tere-holskiy--tva.sudrf.ru
todjinskiy--tva.sudrf.ru
tomarinskiy--sah.sudrf.ru
troickr--chel.sudrf.ru
www.mos-gorsud.ru
```

В файлах JSONL сжатый XZ, объекты имеют такие поля:

- `t` − дата и время (UTC) отправки запроса
- `sud` − сайт суда, с которого скачано расписание
- `date` − расписание на эту дату
- `cases` − список заседаний в этот день
    - `url` − ссылка на детальную информацию о деле
    - `docs` − ссылки на прикреплённые документы
    - `cat` 
    - `num`
    - `time`
    - `event` − название события (у некоторых судов нет этого поля)
    - `place`
    - `info`
    - `judge`
    - `result`


```json
{
  "sud": "tindinskiy--amr.sudrf.ru",
  "date": "2021-01-01",
  "t": "2025-11-17T20:29:12.044515",
  "cases": [
    {
      "cat": "ДЕЛА ОБ АДМИНИСТРАТИВНЫХ ПРАВОНАРУШЕНИЯХ - ПЕРВАЯ ИНСТАНЦИЯ",
      "num": "5-99/2021 (5-369/2020;)",
      "url": "/modules.php?name=sud_delo&name_op=case&_uid=be228eaf-e908-4f57-9311-55898e497bff&_deloId=1500001&_caseType=0&_new=0&srv_num=1&_hideJudge=0",
      "time": "16:18",
      "event": "Рассмотрение дела по существу",
      "place": "",
      "info": "Обухов Артем Сергеевич - ст.20.1 ч.2 КоАП РФ",
      "judge": "Тотмянина Марина Васильевна",
      "result": "Вынесено постановление о назначении административного наказания",
      "docs": []
    }
  ]
}
{
  "sud": "vol--vol.sudrf.ru",
  "date": "2021-01-01",
  "t": "2025-11-17T20:28:19.360583",
  "cases": [
    {
      "cat": "Дела об административных правонарушениях - первая инстанция",
      "num": "5-236/2021",
      "url": "/modules.php?name=sud_delo&srv_num=1&name_op=case&case_id=558261586&case_uid=7f237355-7f3d-482d-b2dd-126bf567452d&delo_id=1500001",
      "time": "09:10",
      "place": "кабинет 8",
      "info": "ПРАВОНАРУШЕНИЕ: Зотов Александр Владимирович - ст.20.1 ч.1 КоАП РФ",
      "judge": "Кармолин Евгений Александрович",
      "result": "Вынесено постановление о назначении административного наказания",
      "docs": [
        "/modules.php?name=sud_delo&name_op=doc&number=560690815&delo_id=1500001&new=&text_number=1"
      ]
    },
    {
      "cat": "Дела об административных правонарушениях - первая инстанция",
      "num": "5-235/2021",
      "url": "/modules.php?name=sud_delo&srv_num=1&name_op=case&case_id=558261576&case_uid=c6861ea0-b007-4387-9abd-34177ae37e07&delo_id=1500001",
      "time": "09:20",
      "place": "кабинет 8",
      "info": "ПРАВОНАРУШЕНИЕ: Соколов Николай Николаевич - ст.20.1 ч.2 КоАП РФ",
      "judge": "Кармолин Евгений Александрович",
      "result": "Вынесено постановление о назначении административного наказания",
      "docs": [
        "/modules.php?name=sud_delo&name_op=doc&number=560690881&delo_id=1500001&new=&text_number=1"
      ]
    },
    {
      "cat": "Дела об административных правонарушениях - первая инстанция",
      "num": "5-234/2021",
      "url": "/modules.php?name=sud_delo&srv_num=1&name_op=case&case_id=558261555&case_uid=3dcbd0ee-f344-4484-ade7-25ed5a46e1c6&delo_id=1500001",
      "time": "09:30",
      "place": "кабинет 8",
      "info": "ПРАВОНАРУШЕНИЕ: Полежаев Михаил Васильевич - ст.20.1 ч.1 КоАП РФ",
      "judge": "Кармолин Евгений Александрович",
      "result": "Вынесено постановление о назначении административного наказания",
      "docs": [
        "/modules.php?name=sud_delo&name_op=doc&number=560690814&delo_id=1500001&new=&text_number=1"
      ]
    }
  ]
}
```

## Дела
- [не распарсенные](./data/info/raw)
