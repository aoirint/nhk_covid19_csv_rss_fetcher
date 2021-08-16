from dataclasses import dataclass
import pandas as pd
from io import StringIO
from pathlib import Path
# from datetime import datetime as dt

from fetchers import NhkCovidDailyFetcher

@dataclass
class FetchResult:
    path: Path
    csv_data: pd.DataFrame

class Tasker:
    def __init__(self):
        self.nhk_daily = NhkCovidDailyFetcher()

    def do_fetch(self, name: str, fetcher) -> FetchResult:
        # ymd_hms = dt.now().strftime('%Y%m%d_%H%N%S')
        dir_path = Path('./data')
        dir_path.mkdir(exist_ok=True, parents=True)
        path = dir_path / f'{name}.csv'

        csv_text = fetcher.fetch()

        with open(path, 'w') as fp:
            fp.write(csv_text)

        sio = StringIO(csv_text)
        csv_data = pd.read_csv(sio)

        return FetchResult(
            path=path,
            csv_data=csv_data,
        )

    def do_task(self):
        fres = self.do_fetch('nhk_covid_daily', fetcher=self.nhk_daily)



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--schedule', action='store_true')
    args = parser.parse_args()

    tasker = Tasker()

    if not args.schedule:
        tasker.do_task()

    else:
        import time
        import schedule

        print('Execute at 17:00 everyday')
        schedule.every().day.at('17:00').do(tasker.do_task)

        while True:
            schedule.run_pending()
            time.sleep(1)
