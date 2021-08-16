import requests

NHK_CSV_URL = 'https://www3.nhk.or.jp/n-data/opendata/coronavirus/nhk_news_covid19_prefectures_daily_data.csv'

class NhkCovidDailyException(Exception):
    pass

class NhkCovidDailyFetcher:
    def fetch(self) -> str:
        res = requests.get(NHK_CSV_URL, timeout=10)
        if res.status_code != 200:
            raise NhkCovidDailyException(f'Status: {res.status_code}')

        csv_text = res.text
        return csv_text
