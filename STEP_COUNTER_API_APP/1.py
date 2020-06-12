import datetime
from datetime import timedelta


timestamp = datetime.datetime.today().timestamp()


print(timestamp)

print(datetime.datetime.today())


currentdate = datetime.datetime.today()
print (currentdate.combine(currentdate.date(), currentdate.min.time()))


print(timedelta(2).total_seconds())

print('7 agi', currentdate.timestamp() - timedelta(7).total_seconds())
print(currentdate.timestamp())
def statistics_sort():
    curent_datetime = datetime.datetime.today()
    start_daytime = curent_datetime.combine(curent_datetime.date(), curent_datetime.min.time())




"""
request add statistick


{"statistics":["counts":23, "kkal":580, "time":438], "timestamp":223344444}

"""