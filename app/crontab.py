from database import insertCityTable,insertNowTable,CityTable
from apscheduler.schedulers.blocking import BlockingScheduler


def crawler():
    city = CityTable.query.all()
    if city is not None:
        for r in city:
            c = r.name
            insertNowTable('c',r.name)
            insertNowTable('F',r.name)
            print(c)
    else:
        print('lose')

if __name__ == '__main__':
    sched = BlockingScheduler()
    sched.add_job(crawler, 'interval', seconds=10)
    sched.start()