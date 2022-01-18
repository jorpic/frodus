import json
import requests
from urllib3.exceptions import InsecureRequestWarning


class API:
    def __init__(self):
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json; charset=utf-8',
            'Origin': 'https://bsr.sudrf.ru',
            'Referer': 'https://bsr.sudrf.ru/bigs/portal.html',
        })
        self.uid = self.get_uid()


    def get_uid(self):
        res = self.post_json('getUid.action', {'uid': None})
        uid = res.json()['uid']
        requests.utils.add_dict_to_cookiejar(
            self.session.cookies,
            {'settingsUid': uid})
        return uid


    def search(self, query):
        query['request']['uid'] = self.uid
        return self.post_json('s.action', query)


    def post_json(self, action, data):
        res = self.session.post(
            url=f'https://bsr.sudrf.ru/bigs/{action}',
            data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
            verify=False)

        # FXIME:
        #   except:
        #     dump to file
        #     print(res.content.decode('utf-8'))
        return res
