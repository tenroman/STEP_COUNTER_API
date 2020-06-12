import datetime
import calendar
import time




# def get_request(methon, addres, data=None):
#     print('OK')
#
# # now = datetime.date.today()
#
# #
# list = []
#
# for i in range(100):
#     list.append(lambda x: x + i)
#
# print(list[42](3))
# #
# days_count_in_month = calendar.monthrange(now.year, 2)[1]
# print('days_count_in_month',days_count_in_month)
#
# for day in range(1, days_count_in_month + 1):
#     print()
#     get_month_day_start = str(now.year) + '-' + str(now.month) + '-' + str(day) + ' 00:00:00'
#     get_month_day_end = str(now.year) + '-' + str(now.month) + '-' + str(day) + ' 23:59:59'
#     print('start', get_month_day_start, 'end', get_month_day_end)
# #
# #
# # str_start_day = str(now) + ' 00:00:00'
# # str_end_day = str(now) + ' 23:59:59'
# # # print('str_end_day',str_end_day, 'str_end_day',str_end_day)
# #
# #
# # today_timestamp = time.mktime(datetime.datetime.strptime(str(str_start_day), "%Y-%m-%d %H:%M:%S").timetuple())
# # end_time__and_today = time.mktime(
# #         datetime.datetime.strptime(str(str_end_day), "%Y-%m-%d %H:%M:%S").timetuple())
# #
# # timestamp = int(today_timestamp)
# #
# # # print(now.year, now.month, now.day)
#
#
# now = datetime.date.today()
# print('now', now)
# days_count_in_month = calendar.monthrange(now.year, 1)[1]
# print('days_count_in_month', days_count_in_month)
# get_month_day_start = str(now.year) + '-' + '01' + '-' + '01' + ' 00:00:00'
# get_month_day_end = str(now.year) + '-' + str(now.month) + '-' + str(days_count_in_month) + ' 23:59:59'
#
# day_timestamp_start = time.mktime(
#     datetime.datetime.strptime(str(get_month_day_start), "%Y-%m-%d %H:%M:%S").timetuple())
# day_timestamp_end = time.mktime(
#     datetime.datetime.strptime(str(get_month_day_end), "%Y-%m-%d %H:%M:%S").timetuple())
#
# print('day_timestamp_start', day_timestamp_start)
# print('day_timestamp_end', day_timestamp_end)
#
# # today = datetime.date.today()
# # """получить начало недели"""
# # monday = today - datetime.timedelta()
# #
# # print(days_count_in_month)
# #

now= datetime.date.today()
print(now.month)
days_count_in_month = calendar.monthrange(now.year, now.month)[1]

print(days_count_in_month)

aaa =  now.month +1

print('_____')
days_count_in_month = calendar.monthrange(now.year, aaa)[1]

print(days_count_in_month)

till = datetime.timedelta(days=days_count_in_month)


print('till,', till)
#
#
# print(today)
#
# print(monday)
#
# print(today.month)
#
# print(today.year)
#
#
# aaa = {"stat_list":[{"time_counts":300, "step_counts":1000, "kkal":400, "created_at":1586629000}]}


# print(int(0))