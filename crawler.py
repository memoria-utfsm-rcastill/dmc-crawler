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
            current_data = None
            for i, td in enumerate(bs.find_all('td', class_='text-center')):
                # 2 first columns always represent timestamp
                elem = i % (len(tag_data_map[tag_code]) + 2)
                # date
                if elem == 0:
                    if i != 0:
                        data.append(DataEntry(dev_code, tag_code, datetime.strptime(
                            current_ts, '%d-%m-%YT%H:%M'), current_data))
                    current_ts = td.string.strip()
                # time
                elif elem == 1:
                    current_ts += 'T%s' % td.string.strip()
                    current_data = current_ts
                # data
                else:
                    current_data = tag_data_map[tag_code][elem -
                                                          2](current_data, td.string.strip())

            # Repeat one last time for last element
            data.append(DataEntry(dev_code, tag_code, datetime.strptime(
                current_ts, '%d-%m-%YT%H:%M'), current_data))

            return data
        else:
            response.raise_for_status()
    except Exception as ex:
        print(ex)


def main():
    for y in range(2013, 2018):
        for m in range(1, 13):
            month_data = get_month_data(
                dev_code=DEV_RODELILLO,
                year=y,
                month=m,
                tag_code=TAG_WIND_DATA)
            for entry in month_data:
                print(entry)


if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    try:
        main()
    except KeyboardInterrupt:
        print()
