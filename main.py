import os
from pathlib import Path
import requests
from datetime import datetime as dt
import subprocess

import logging
logger = logging.getLogger(__name__)

def fetch_nhk_covid_daily():
    logger.info(dt.now().isoformat())
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


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--schedule', action='store_true')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    if not args.schedule:
        fetch_nhk_covid_daily()

    else:
        import time
        import schedule

        print('Execute at 17:00 everyday')
        schedule.every().day.at('17:00').do(fetch_nhk_covid_daily)

        while True:
            schedule.run_pending()
            time.sleep(1)
