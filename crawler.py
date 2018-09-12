import requests
import urllib3

from bs4 import BeautifulSoup
from devices import *
from tags import *
from datetime import datetime


class DataEntry:
    dev_code = None
    tag_code = None
    timestamp = None
    data = None

    def __init__(self, dev_code, tag_code, timestamp, data):
        self.dev_code = dev_code
        self.tag_code = tag_code
        self.timestamp = timestamp
        self.data = data

    def __repr__(self):
        return '{ts} [{dev} / {tag}] {val}'\
            .format(ts=self.timestamp,
                    dev=dev_map[self.dev_code],
                    tag=tag_map[self.tag_code],
                    val=self.data)


def get_month_data(*, dev_code, year, month, tag_code):
    uri = 'https://climatologia.meteochile.gob.cl/application/informacion/datosMensualesDelElemento/{dev}/{y}/{m}/{tag}'.format(
        dev=dev_code, y=year, m=month, tag=tag_code)

    try:
        response = requests.get(
            uri, verify=False)
        if response.status_code == 200:
            bs = BeautifulSoup(response.text, 'html.parser')
            data = []
            current_ts = ''
            for i, td in enumerate(bs.find_all('td', class_='text-center')):
                elem = i % 3
                # date
                if elem == 0:
                    current_ts = td.string.strip()
                # time
                elif elem == 1:
                    current_ts += 'T%s' % td.string.strip()
                # data
                else:
                    data.append(DataEntry(dev_code, tag_code,
                                          datetime.strptime(current_ts, '%d-%m-%YT%H:%M'), td.string.strip()))
            return data
        else:
            response.raise_for_status()
    except Exception as ex:
        print(ex)


def main():
    for m in range(1, 13):
        month_data = get_month_data(
            dev_code=DEV_RODELILLO,
            year=2013,
            month=m,
            tag_code=TAG_TEMPERATURE)
        for entry in month_data:
            print(entry)


if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    try:
        main()
    except KeyboardInterrupt:
        print()
