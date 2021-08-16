import os
from pathlib import Path
import requests
from datetime import datetime as dt
import subprocess

import logging
logger = logging.getLogger(__name__)

def fetch_nhk_covid_daily():
    logger.info(f'{dt.now().isoformat()}: fetch_nhk_covid_daily')
    NHK_CSV_URL = 'https://www3.nhk.or.jp/n-data/opendata/coronavirus/nhk_news_covid19_prefectures_daily_data.csv'

    res = requests.get(NHK_CSV_URL, timeout=10)
    if res.status_code != 200:
        raise Exception(f'Status: {res.status_code}')

    csv_text = res.text

    ymd = dt.now().strftime('%Y%m%d')
    dir_path = Path('./data/nhk_covid_daily')

    dir_path.mkdir(parents=True, exist_ok=True)

    ymd_file = f'{ymd}.csv'
    ymd_path = dir_path / ymd_file
    latest_path = dir_path / 'daily.csv'

    with open(ymd_path, 'w') as fp:
        fp.write(csv_text)

    subprocess.call([ 'ln', '-sf', ymd_file, str(latest_path)])


def fetch_nhk_rss_cat1():
    logger.info(f'{dt.now().isoformat()}: fetch_nhk_rss_cat1')
    url = 'https://www3.nhk.or.jp/rss/news/cat1.xml'

    res = requests.get(url, timeout=10)
    if res.status_code != 200:
        raise Exception(f'Status: {res.status_code}')

    xml_text = res.text

    ymd = dt.now().strftime('%Y%m%d')
    dir_path = Path('./data/nhk_rss_cat1')

    dir_path.mkdir(parents=True, exist_ok=True)

    ymd_file = f'{ymd}.xml'
    ymd_path = dir_path / ymd_file
    latest_path = dir_path / 'daily.xml'

    with open(ymd_path, 'w') as fp:
        fp.write(xml_text)

    subprocess.call([ 'ln', '-sf', ymd_file, str(latest_path)])

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--schedule', action='store_true')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    hm2task = (
        # ('0:00', fetch_nhk_covid_daily),
        ('17:00', fetch_nhk_rss_cat1),
    )

    if not args.schedule:
        for (hm, do_task) in hm2task:
            do_task()

    else:
        import time
        import schedule

        for (hm, do_task) in hm2task:
            print(f'Execute {str(do_task)} at {hm} everyday')
            schedule.every().day.at(hm).do(do_task)

        while True:
            schedule.run_pending()
            time.sleep(1)
