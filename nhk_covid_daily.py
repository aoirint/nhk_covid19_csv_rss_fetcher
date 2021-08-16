import sys
import requests
from pathlib import Path
# from datetime import datetime as dt

NHK_CSV_URL = 'https://www3.nhk.or.jp/n-data/opendata/coronavirus/nhk_news_covid19_prefectures_daily_data.csv'

class NhkCovidDailyException(Exception):
    pass

class NhkCovidDaily:
    def fetch(self) -> str:
        res = requests.get(NHK_CSV_URL, timeout=10)
        if res.status_code != 200:
            raise NhkCovidDailyException(f'Status: {res.status_code}')

        csv_text = res.text
        return csv_text

    def update(self):
        csv_text = self.fetch()

        # ymd_hms = dt.now().strftime('%Y%m%d_%H%N%S')
        dir_path = Path('./data')
        dir_path.mkdir(exist_ok=True, parents=True)
        daily_path = dir_path / 'nhk_covid_daily.csv'

        with open(daily_path, 'w') as fp:
            fp.write(csv_text)
