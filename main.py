from nhk_covid_daily import NhkCovidDaily

class Tasker:
    def __init__(self):
        self.nhk_daily = NhkCovidDaily()

    def do_task(self):
        self.nhk_daily.update()


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
