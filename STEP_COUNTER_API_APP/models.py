from django.db import models
from datetime import date
import datetime
import json
import random
import uuid
import base64
import os
import datetime
from django.db.models import Q
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django_unixdatetimefield import UnixDateTimeField
import time
import calendar
from STEP_COUNTER_API_APP.PUSH_NOTIFICATION import SentPush
try:
    base_url = 'http://stepcounter.spg.uz:8080/media/'
except:
    base_url = 'http://' + 'localhost'




def payment_by_upay(amount,personalAccount, period):
    return 'https://pay.smst.uz/prePay.do?'+'amount=' +str(amount)+'&'+ 'serviceId=546&'+'apiVersion=1&'+'personalAccount='+str(personalAccount) +'&'+'period='+period


def payment_by_click(amount, transaction_param, period, return_url=None, card_type=None,):
    return "https://my.click.uz/services/pay?" + 'service_id='+str(1123) + '&merchant_id='+str(333223232) + '&amount=' + str(amount) + '&transaction_param=' + str(transaction_param) + '&return_url=' + str(return_url) + '&period='+str(period)

def get_stat_by_hour(user_id):
    result = {}
    result_list = []
    today = datetime.date.today()
    str_today_start = str(today) + ' 00:00:00'
    str_today_end = str(today) + ' 23:59:59'
    today_timestamp = time.mktime(datetime.datetime.strptime(str(str_today_start), "%Y-%m-%d %H:%M:%S").timetuple())
    end_time__and_today = time.mktime(
        datetime.datetime.strptime(str(str_today_end), "%Y-%m-%d %H:%M:%S").timetuple())
    timestamp = int(today_timestamp)

    for i in range(0, 24):
        till = timestamp + 3600
        kkal = 0
        steps = 0
        total_time = 0
        meters = 0

        from_0 = Statistics.objects.filter(created_at__lt=till,
                                           created_at__gte=timestamp, user_id=user_id)

        if from_0:
            for all_count in from_0:
                kkal += int(all_count.kkal)
                steps += int(all_count.step_counts)
                meters += int(all_count.meters_counts)
                total_time += int(all_count.time_counts)

                encr_key = str(i) + ':00'
                result[encr_key] = {'kkal': kkal, 'meters': meters, 'steps': steps, 'total_time': total_time,
                                    'normativ': all_count.user.normativ_from_trainer}

                timestamp += 3600

        else:

            encr_key = str(i) + ':00'
            result[encr_key] = {'kkal': kkal, 'meters': meters, 'steps': steps, 'total_time': total_time, 'normativ': 0}

            timestamp += 3600

    result_list.append(result)
    return result_list


def get_stat_by_weekday(user_id):
    result = {}
    result_list = []
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    str_monday_start = str(monday) + ' 00:00:00'
    str_monday_end = str(monday) + ' 23:59:59'
    str_today_start = str(today) + ' 00:00:00'
    str_monday_start_timestamp = time.mktime(datetime.datetime.strptime(str(str_monday_start), "%Y-%m-%d %H:%M:%S").timetuple())
    str_monday_end_timestamp = time.mktime(datetime.datetime.strptime(str(str_monday_end), "%Y-%m-%d %H:%M:%S").timetuple())

    today_timestamp = time.mktime(datetime.datetime.strptime(str(str_today_start), "%Y-%m-%d %H:%M:%S").timetuple())

    timestamp = int(str_monday_start_timestamp)
    end_time_stamp = int(str_monday_end_timestamp)
    week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for i in week_days:
        till = end_time_stamp
        from_time = timestamp
        kkal = 0
        steps = 0
        meters = 0
        total_time = 0

        from_0 = Statistics.objects.filter(created_at__lt=till,
                                           created_at__gte=from_time, user_id=user_id)
        if from_0:
            for all_count in from_0:
                kkal += int(all_count.kkal)
                steps += int(all_count.step_counts)
                meters += int(all_count.meters_counts)
                total_time += int(all_count.time_counts)

                encr_key = str(i)
                result[encr_key] = {'kkal': kkal, 'meters': meters, 'steps': steps, 'total_time': total_time,
                                    'normativ': all_count.user.normativ_from_trainer}

            timestamp += 86400
            end_time_stamp += 86400

        else:
            encr_key = str(i)
            result[encr_key] = {'kkal': kkal, 'meters': meters, 'steps': steps, 'total_time': total_time, 'normativ': 0}

            timestamp += 86400
            end_time_stamp += 86400

    result_list.append(result)
    return result_list


def get_stat_by_month(user_id):
    result = {}
    result_list = []
    stat_by_day = {}

    now = datetime.date.today()
    days_count_in_month = calendar.monthrange(now.year, now.month)[1]

    for day in range(1, days_count_in_month + 1):
        print(day)
        encr_key = str(day) + '.' + str(now.month) + '.' + str(now.year)

        get_month_day_start = str(now.year) + '-' + str(now.month) + '-' + str(day) + ' 00:00:00'
        get_month_day_end = str(now.year) + '-' + str(now.month) + '-' + str(day) + ' 23:59:59'
        day_timestamp_start = time.mktime(
            datetime.datetime.strptime(str(get_month_day_start), "%Y-%m-%d %H:%M:%S").timetuple())
        day_timestamp_end = time.mktime(
            datetime.datetime.strptime(str(get_month_day_end), "%Y-%m-%d %H:%M:%S").timetuple())

        till = int(day_timestamp_end)
        from_time = int(day_timestamp_start)
        # print('from', from_time, 'till', till)
        kkal = 0
        steps = 0
        total_time = 0
        meters = 0

        from_0 = Statistics.objects.filter(created_at__lt=till,
                                           created_at__gte=from_time, user_id=user_id)
        print('from_0', from_0)

        if from_0:
            for all_count in from_0:
                kkal += int(all_count.kkal)
                steps += int(all_count.step_counts)
                total_time += int(all_count.time_counts)
                meters += int(all_count.meters_counts)

                result[encr_key] = {'kkal': kkal, 'meters': meters, 'steps': steps, 'total_time': total_time,
                                    'normativ': all_count.user.normativ_from_trainer}

                # day_timestamp_end += 86400
            day_timestamp_start += 86400

        else:
            encr_key = str(day) + '.' + str(now.month) + '.' + str(now.year)

            result[encr_key] = {'kkal': kkal, 'meters': meters, 'steps': steps, 'total_time': total_time, 'normativ': 0}

            day_timestamp_start += 86400

    result_list.append(result)
    return result_list


def get_stat_by_year(user_id):
    result = {}
    result_list = []
    stat_by_day = {}

    now = datetime.date.today()
    print('now')
    year_month = [{'name': 'January', 'value': 1}, {'name': 'Febrary', 'value': 2}, {'name': 'March', 'value': 3},
                  {'name': 'April', 'value': 4}, {'name': 'May', 'value': 5}, {'name': 'June', 'value': 6}, {'name': 'July', 'value': 7},
                  {'name': "August", 'value': 8}, {'name': 'September', 'value': 9}, {'name': "October", 'value': 10},
                  {'name': 'November', 'value': 11}, {'name': "December", 'value': 12}]

    for month in year_month:
        print('mo', month)
        days_count_in_month = calendar.monthrange(now.year, month.get('value'))[1]
        # print('month',month)
        days_list = []
        # print('days_count_in_month',days_count_in_month)
        encr_key = month.get('name')
        stat_by_day = {}

        get_month_day_start = str(now.year) + '-' + str(month.get('value')) + '-' + str(1) + ' 00:00:00'
        get_month_day_end = str(now.year) + '-' + str(month.get('value')) + '-' + str(days_count_in_month) + ' 23:59:59'
        day_timestamp_start = time.mktime(
            datetime.datetime.strptime(str(get_month_day_start), "%Y-%m-%d %H:%M:%S").timetuple())
        day_timestamp_end = time.mktime(
            datetime.datetime.strptime(str(get_month_day_end), "%Y-%m-%d %H:%M:%S").timetuple())
        till = int(day_timestamp_end)
        from_time = int(day_timestamp_start)

        # print('from', from_time, 'till', till)
        kkal = 0
        steps = 0
        total_time = 0
        meters = 0

        from_0 = Statistics.objects.filter(created_at__lt=till,
                                           created_at__gte=from_time, user_id=user_id)
        # print('from', from_time,'till',till)

        if from_0:
            for all_count in from_0:
                kkal += int(all_count.kkal)
                steps += int(all_count.step_counts)
                total_time += int(all_count.time_counts)
                meters += int(all_count.meters_counts)
                result[encr_key] = {'kkal': kkal, 'meters': meters, 'steps': steps, 'total_time': total_time, 'normativ': all_count.user.normativ_from_trainer}

            day_timestamp_end += 86400
            day_timestamp_start += 86400

        else:
            # encr_key = str('from_0') + str(day)

            encr_key_month = month.get('name')

            result[encr_key] = {'kkal': kkal, 'meters': meters, 'steps': steps, 'total_time': total_time, 'normativ': 0}

            # days_list.append(stat_by_day)
            day_timestamp_end += 86400
            day_timestamp_start += 86400

    result_list.append(result)
    return result_list


def file_decode(base_64, user_id=None, file_type=None, type=None):
    SAVE_PATH = '/home/STEP_COUNTER_API/STEP_COUNTER_API/media/'
    filename = None
    data = base_64.replace(' ', '+')
    cur_time = datetime.datetime.now().timestamp()

    filedata = base64.b64decode(data)

    if type:
        filename = str(type) + '_ID_' + str(
            user_id) + '.' + file_type  # I assume you have a way of picking unique filenames

    else:
        filename = str(cur_time) + '_ID_' + str(
            user_id) + '.' + file_type  # I assume you have a way of picking unique filenames

    print('ggg', filename)

    if file_type == 'jpg':
        completeName = os.path.join(SAVE_PATH + 'images', filename)
        with open(completeName, 'wb') as f:

            f.write(filedata)

        file_path = os.path.abspath(completeName)
        print('file_path', file_path)
        return filename

    elif file_type == 'png':
        completeName = os.path.join(SAVE_PATH + 'images', filename)
        with open(completeName, 'wb') as f:
            f.write(filedata)

        file_path = os.path.abspath(completeName)
        return filename

    elif file_type == 'mp3':
        completeName = os.path.join(SAVE_PATH + 'mp3', filename)
        with open(completeName, 'wb') as f:
            f.write(filedata)

        file_path = os.path.abspath(completeName)
        return filename

    else:
        completeName = os.path.join(SAVE_PATH + 'other_files', filename)
        with open(completeName, 'wb') as f:
            f.write(filedata)

        file_path = os.path.abspath(completeName)
        print(file_path)
        return filename


def sms(phone_number):
    get_sms = random.randint(1234, 9999)
    print('get_sms', get_sms)
    return get_sms


def generate_device_token(request):
    token = str(uuid.uuid4())
    timestamp = datetime.datetime.now().timestamp()
    return token + '_' + str(timestamp)


def save_user_request(url, req, res, req_headers):
    save_request = Saverequest()
    save_request.request = req
    save_request.response = res
    save_request.request_headers = req_headers
    save_request.request_url = url
    save_request.save()
    req_id = save_request.pk

    return req_id


class PaymentMetod(models.Model):
    name_ru = models.CharField(default='', blank=True, max_length=200, verbose_name='Заголовок имения РУс')
    name_uz = models.CharField(default='', blank=True, max_length=200, verbose_name='Заголовок имения Уз кирилица')
    image = models.ImageField(blank=False, verbose_name='Логотип платежной системы')

    def __str__(self):
        return str(self.pk) + ' ' + str(self.name_ru)


class Follow(models.Model):
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING, verbose_name='Пользователь', null=True, blank=True)
    trener = models.ForeignKey('UserTrener', on_delete=models.DO_NOTHING, verbose_name='Тренер', null=True, blank=True)
    is_trial = models.BooleanField(blank=True, verbose_name='Пробный период', default=False)
    trial_period = models.PositiveIntegerField(default=10, blank=True, null=True, verbose_name='Кол во дней пробный период')
    trial_expired = models.BooleanField(blank=True, verbose_name='Пробный период использован', default=False)
    # trial_period_start = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Начало тестового периода')
    # trial_period_end = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Окончание тестового периода')
    payment_type = models.CharField(max_length=200, verbose_name='метод оплаты', null=True, blank=True, default='')
    is_active = models.BooleanField(blank=True, verbose_name='Активирована?', default=False)
    follow_period_start = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Начало  периода')
    follow_period_end = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Конец  периода')
    total_price = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='сумма оплаты')

    def __str__(self):
        return str(self.pk) + ' ' + str(self.user) + ' Начало периода: ' + str(self.follow_period_start) + ', Конец периода: ' + str(self.follow_period_end)




    def get_or_create_user_follow(self, user_id, trener_id, request):
        response = {}
        today = datetime.datetime.now()

        get_request = json.loads(request.body)
        get_trener = UserTrener.objects.get(id=trener_id)
        get_follow, create_new_follow = Follow.objects.get_or_create(user_id=user_id, trener_id=trener_id)
        if create_new_follow:
            print('ccccc')
            print('create_follow')
            create_follow = Follow.objects.get(user_id=user_id, trener_id=trener_id)
            print('create_follow',create_follow)

            two_month = create_follow.trener.price * 2
            three_month = create_follow.trener.price * 3

            response = {'status': 200, "message": "create_follow",
                                'data': {'follow_id': create_follow.id, 'is_trial': create_follow.is_trial,
                                         'is_active': create_follow.is_active,
                                         'trial_period': create_follow.trial_period,
                                         'follow_period_start': create_follow.follow_period_start,
                                         'follow_period_end': create_follow.follow_period_end,
                                         'total_price': create_follow.total_price,
                                         'trial_expired': False,
                                         'trial_days': get_follow.trial_period,
                                         "follow_trener": {'id': create_follow.trener_id, 'name': create_follow.trener.name,
                                                           'rate': create_follow.trener.rate, 'price': create_follow.trener.price,
                                                           'avatar': create_follow.trener.avatar}}, "available_payments": [{'title': 'PayMe', 'id':1, 'logo':'http://127.0.0.1','description':'Оплата через приложение Payme'},
                                                                                                                           {
                                                                                                                               'title': 'Upay',
                                                                                                                               'id': 2,
                                                                                                                               'logo': 'http://127.0.0.1',
                                                                                                                               'description': 'Оплата через приложение Upay'},
                                                                                                                           {'title': 'Click', 'id':3, 'logo':'http://127.0.0.1','description':'Оплата через приложение Click'},
                                                                                                                           {'title': 'Paynet', 'id':4, 'logo':'http://127.0.0.1','description':'Оплата через приложение Paynet'}
                                                                                                                           ], 'available_period':[{'id':1, 'title': str(create_follow.trener.price)+' сум / 1 месяц'},{'id':2, 'title': str(two_month)+' сум / 2 месяцa'},{'id':3, 'title': str(three_month) +' сум / 3 месяцa'}]}
        else:
            print('efesss')
            two_month = get_follow.trener.price * 2
            three_month = get_follow.trener.price * 3
            print('trial_period_available',get_follow.trial_expired,)

            response = {'status': 200, "message": "get_follow",
                        'data': {'follow_id': get_follow.pk, 'is_trial': get_follow.is_trial,
                                 'is_active': get_follow.is_active,
                                 'trial_period': get_follow.trial_period,
                                 'follow_period_start': get_follow.follow_period_start,
                                 'follow_period_end': get_follow.follow_period_end,
                                 'total_price': get_follow.total_price,
                                 'trial_expired': get_follow.trial_expired,
                                 'trial_days': get_follow.trial_period,
                                 "follow_trener": {'id': get_follow.trener_id, 'name': get_follow.trener.name,
                                                   'rate': get_follow.trener.rate,
                                                   'price': get_follow.trener.price,
                                                   'avatar': get_follow.trener.avatar}}, "available_payments": [
                    {'title': 'PayMe', 'id': 1, 'logo': 'http://127.0.0.1',
                     'description': 'Оплата через приложение Payme', "type":'link'},
                    {
                        'title': 'Upay',
                        'id': 2,
                        'logo': 'http://127.0.0.1',
                        'description': 'Оплата через приложение Upay', "type":'link'},
                    {'title': 'Click', 'id': 3, 'logo': 'http://127.0.0.1',
                     'description': 'Оплата через приложение Click', "type":'link'},
                    {'title': 'Paynet', 'id': 4, 'logo': 'http://127.0.0.1',
                     'description': 'Оплата через приложение Paynet', "type":'popup'}
                    ], 'available_period':[{'id':1, 'title': str(get_follow.trener.price)+' сум / 1 месяц'},{'id':2, 'title': str(two_month)+' сум / 2 месяцa'}, {'id':3, 'title': str(three_month)+' сум / 3 месяцa'}]}

        save_req = save_user_request(url='follow/add', req=get_request, res=response,
                                                 req_headers=request.headers)
        response['req_id'] = save_req
        print('3333')
        return response


    def check_active_follow(self, user_id):
        today = datetime.datetime.now()
        print('user_id',user_id)
        response = {}
        aaa = Follow.objects.filter(user_id=user_id)
        print('aaa',aaa)
        check_active_follow = Follow.objects.filter(user_id=user_id)

        for follow in check_active_follow:
            if follow.follow_period_end:
                if follow.is_active and follow.follow_period_end > today.timestamp():
                    response = {"is_active":True, 'status':True, 'follow_id':follow.id, 'trener_id':follow.trener_id}
                    # return response

                elif follow.is_trial and follow.follow_period_end > today.timestamp():
                    response = {"is_active": False, 'is_trial':True, 'status':True,'follow_id':follow.id,'trener_id':follow.trener_id}
                    # return response




                elif follow.is_active and follow.follow_period_end < today.timestamp():
                    follow.is_active = False
                    follow.save()
                    response =  {"is_active": False, 'status':False, 'is_active':follow.is_active,'trener_id':follow.trener_id}
                    # return response


                elif follow.is_trial and follow.follow_period_end < today.timestamp():
                    follow.is_trial = False
                    follow.trial_expired = True
                    follow.save()
                    response = {"is_trial": False, 'status':False, 'is_active':follow.is_active,'trener_id':follow.trener_id}
                    # return response


                elif follow.trial_expired and follow.follow_period_end < today.timestamp():
                    follow.is_trial = False
                    follow.trial_expired = True
                    follow.save()
                    response = {"is_trial": False, 'status':False, 'is_active':follow.is_active,'trener_id':follow.trener_id}

                else:
                    follow.is_active = False
                    follow.save()
                    response = {'status':'new', 'is_active':False, 'is_trial':follow.is_trial}
                    # return response


            # else:
            #     return {}


        return response


    def activate_follow(self, follow_id,  request,period=None, is_trial=None, activate=None):
        get_request = json.loads(request.body)
        now = datetime.datetime.now()
        today = datetime.datetime.now()
        days_count_in_month = now.month
        if follow_id and period:
            try:
                get_follow = Follow.objects.get(id=follow_id)
                if period == 1:
                    days_count_in_month = calendar.monthrange(now.year, now.month)[1]
                elif period == 2:
                    days_count_in_month = calendar.monthrange(now.year, now.month+1)[1]

                else:
                    days_count_in_month = calendar.monthrange(now.year, now.month+2)[1]

                till = datetime.timedelta(days=days_count_in_month)

                get_upay_link = payment_by_upay(amount=str(get_follow.trener.price*period), personalAccount=str(get_follow.pk), period=str(period))
                get_payme_link = ''
                get_click_link = payment_by_click(amount=str(get_follow.trener.price*period),transaction_param=str(get_follow.pk),period=str(period))
                response = {'payment':[{'title': 'PayMe', 'id': 1, 'logo': 'http://127.0.0.1',
                 'description': 'Оплата через приложение Payme', 'payment_url':get_payme_link},                    {
                        'title': 'Upay',
                        'id': 2,
                        'logo': 'http://127.0.0.1',
                        'description': 'Оплата через приложение Upay', 'payment_url':get_upay_link},

                    {'title': 'Click', 'id': 3, 'logo': 'http://127.0.0.1',
                     'description': 'Оплата через приложение Click','payment_url':get_click_link},
                    {'title': 'Paynet', 'id': 4, 'logo': 'http://127.0.0.1',
                     'description': 'Оплата через приложение Paynet', 'payment_url':None}]}
                save_req = save_user_request(url='follow/activate_follow', req=get_request, res=response,
                                                 req_headers=request.headers)
                response['req_id'] = save_req
                return response


            except Follow.DoesNotExist:
                    response = {11111:'DoesNotExist'}

                    save_req = save_user_request(url='follow/activate_follow', req=get_request, res=response,
                                                 req_headers=request.headers)
                    response['req_id'] = save_req
                    return {"error_title":"Follow", 'error_description':"Doesnt Exist",'req_id':save_req}

        if follow_id and is_trial:
            try:
                get_follow = Follow.objects.get(id=follow_id)
                if get_follow.trial_expired:
                    response = {"error_title":"Follow", 'error_description':'Ошибка активации, пробный период ранее был активирован' }
                    save_req = save_user_request(url='follow/activate_follow', req=get_request, res=response,
                                                 req_headers=request.headers)
                    response['req_id'] = save_req
                    return response

                if not get_follow.is_active and not get_follow.trial_expired and not get_follow.is_trial:
                    get_follow.is_trial = True
                    get_follow.follow_period_start = today.timestamp()
                    get_follow.follow_period_end = get_follow.trial_period *86400 + today.timestamp()
                    get_follow.save()
                    get_chat, create_chat = Chat.objects.get_or_create(user_trener_id=get_follow.trener_id, user_id=get_follow.user_id)

                    response = {'status': True, 'is_tial': True, 'follow_id': get_follow.id, 'follow_period_start':get_follow.follow_period_start,
                                'follow_period_end':get_follow.follow_period_end}
                    save_req = save_user_request(url='follow/activate_follow', req=get_request, res=response,
                                                 req_headers=request.headers)
                    response['req_id'] = save_req
                    response['chat_id'] = get_chat.pk

                    try:

                        get_trener = get_follow.trener.name
                        get_trener_avatar = get_follow.trener.avatar
                        get_devices = UserDevices.objects.filter(user_id=get_follow.user.id).values(
                            'push_token', 'device_type')

                        get_devices_trener = UserDevices.objects.filter(trener_id=get_follow.trener.pk).values(
                            'push_token', 'device_type')



                        push_service = SentPush().send_push(
                                                            message_title='Вы успешно активировали пробную подписку',
                                                            message_body='Ваш тренер ' + str(get_trener.title()),
                                                            userdevices=get_devices, icon_url=get_trener_avatar)

                        push_service_trener = SentPush().send_push(
                            message_title='Активация пробной подписки',
                            message_body='Ваш пользователь  ' + str(get_follow.user.name),
                            userdevices=get_devices_trener, icon_url=get_follow.user.avatar)
                        save_req = save_user_request(url='follow/push_send', req=get_request, res=response,
                                                     req_headers=str(get_devices_trener))
                        response['req_id'] = save_req
                        print('push_service',push_service)
                        print('get_trener_avatar',get_trener_avatar)
                    except Exception as e:
                        print('eee', e)
                        pass

                    return response
                else:
                    response = {"error_title":"Follow", 'error_description':'Ошибка активации, пробный период ранее был активирован или недоступен' }

                    save_req = save_user_request(url='follow/activate_follow', req=get_request, res=response,
                                                 req_headers=request.headers)
                    response['req_id'] = save_req

                    return response




            except Follow.DoesNotExist:
                    response = {11111:'DoesNotExist'}

                    save_req = save_user_request(url='follow/activate_follow', req=get_request, res=response,
                                                 req_headers=request.headers)
                    response['req_id'] = save_req
                    return {"error_title":"Follow", 'error_description':"Doesnt Exist",'req_id':save_req}


    def get_all_active_trener_follows(self, trener_id):
        today = datetime.datetime.now().timestamp()
        follow = Follow.objects.filter(trener_id=trener_id, follow_period_end__gt=int(today)).values()
        print('follow',follow)
        return {'trener_follows':list(follow), 'follow_filter':[{'id':1, 'is_plan':True, 'title':'Плаг выполнен'}, {'id':2, 'day_left':True, 'title':'Менее 3х дней'}], 'sort':[{'id':3, 'by_name':True, 'title':'По имени'}, {'id':4, 'by_day_left':True, 'title':'По дате истечени'}]}




    def sort_follows(self, request, trener_id, is_plan, three_days_left, order_by=None):
        today = datetime.datetime.now().timestamp()
        response = {}
        get_request = None
        import logging

        try:
            today = datetime.datetime.now().timestamp()
            follow = Follow.objects.filter(trener_id=trener_id, follow_period_end__gt=int(today)).values()
            get_request = json.loads(request.body)
            now = datetime.datetime.now()
            today = datetime.datetime.now()

            if is_plan and not three_days_left and not order_by:
                response_list = []
                today = datetime.datetime.now().timestamp()
                follow = Follow.objects.filter(trener_id=trener_id, follow_period_end__gt=int(today)).values()
                print('follow44',follow)
                if follow:
                    for fol in follow:
                        if fol.get('user_id'):
                            get_user = User.objects.get(pk=fol.get('user_id'))
                            get_user_stat = Statistics().get_stat_by_day(request, get_request, user_id=get_user.id,order_by='week' )
                            if get_user_stat:
                                if int(get_user_stat.get('statistics').get('steps')) >= int(get_user_stat.get('statistics').get('normativ')):
                                    fol['avatar'] = get_user.avatar
                                    response_list.append(fol)
                                    # response = {'follows':list(follow), 'message':'is_plane:True'}
                                    # print('response',response)

                                else:
                                    response = {'follows': list(), 'message': 'is_plane:True'}

                            else:
                                response = {'follows': list(), 'message': 'is_plane:True'}

                        else:
                            response = {'follows': response_list, 'message': 'is_plane:True'}

                            save_req = save_user_request(url='follow/follow_filter', req=get_request, res=response,
                                                         req_headers=request.headers)
                            response['req_id'] = save_req
                            return response

                    response = {'follows':response_list, 'message':'is_plane:True'}

                    save_req = save_user_request(url='follow/follow_filter', req=get_request, res=response,
                                                 req_headers=request.headers)
                    response['req_id'] = save_req
                    return response
                else:
                    response = {'follows': response_list, 'message': 'is_plane:True'}

                    save_req = save_user_request(url='follow/follow_filter', req=get_request, res=response,
                                                 req_headers=request.headers)
                    response['req_id'] = save_req
                    return response


            elif is_plan and three_days_left and not order_by:
                response_list = []
                today = datetime.datetime.now().timestamp()
                follow = Follow.objects.filter(trener_id=trener_id, follow_period_end__gt=int(today)).values()
                if follow:
                    for fol in follow:
                        if fol.get('user_id'):
                            get_user = User.objects.get(pk=fol.get('user_id'))
                            get_user_stat = Statistics().get_stat_by_day(request, get_request, user_id=get_user.id,
                                                                         order_by='week')
                            if get_user_stat:
                                check_time = fol.get('follow_period_end') - today
                                if int(get_user_stat.get('statistics').get('steps')) >= int(
                                        get_user_stat.get('statistics').get('normativ')) and 259200 <= int(check_time):
                                    fol['avatar'] = get_user.avatar
                                    fol['name'] = get_user.name

                                    response_list.append(fol)
                                else:
                                    response = {'follows': list(), 'message': 'is_plane:True and three_days_left'}

                            else:
                                response = {'follows': list(), 'message': 'is_plane:True and three_days_left'}

                        else:
                            response = {'follows': response_list, 'message': 'is_plane:True and three_days_left:True'}

                            save_req = save_user_request(url='follow/follow_filter', req=get_request, res=response,
                                                         req_headers=request.headers)
                            response['req_id'] = save_req
                            return response


                    response = {'follows': response_list, 'message': 'is_plane:True and three_days_left:True'}

                    save_req = save_user_request(url='follow/follow_filter', req=get_request, res=response,
                                                 req_headers=request.headers)
                    response['req_id'] = save_req
                    return response
                else:
                    response = {'follows': response_list, 'message': 'is_plane:True and three_days_left:True'}

                    save_req = save_user_request(url='follow/follow_filter', req=get_request, res=response,
                                                 req_headers=request.headers)
                    response['req_id'] = save_req
                    return response

            elif is_plan and not three_days_left and order_by:
                response_list = []
                order_value = ''
                if order_by == 'by_name':
                    order_value = 'user__name'
                elif order_by == 'day_left':
                    order_value = 'follow_period_end'

                print('order, ', 'dddddd')

                today = datetime.datetime.now().timestamp()
                follow = Follow.objects.filter(trener_id=trener_id, follow_period_end__gt=int(today)).values().order_by('-'+str(order_value))
                if follow:
                    for fol in follow:
                        if fol.get('user_id'):
                            get_user = User.objects.get(pk=fol.get('user_id'))
                            get_user_stat = Statistics().get_stat_by_day(request, get_request, user_id=get_user.id,
                                                                         order_by='week')
                            if get_user_stat:
                                check_time = fol.get('follow_period_end') - today
                                if int(get_user_stat.get('statistics').get('steps')) >= int(
                                        get_user_stat.get('statistics').get('normativ')):
                                    fol['avatar'] = get_user.avatar
                                    fol['name'] = get_user.name

                                    response_list.append(fol)
                                else:
                                    response = {'follows': list(), 'message': 'is_plane:True and three_days_left'}

                            else:
                                response = {'follows': list(), 'message': 'is_plane:True and three_days_left'}

                    response = {'follows': response_list, 'message': 'is_plane:True and three_days_left:True'}

                    save_req = save_user_request(url='follow/follow_filter', req=get_request, res=response,
                                                 req_headers=request.headers)
                    response['req_id'] = save_req
                    return response
                else:
                    response = {'follows': response_list, 'message': 'is_plane:True and three_days_left:True'}

                    save_req = save_user_request(url='follow/follow_filter', req=get_request, res=response,
                                                 req_headers=request.headers)
                    response['req_id'] = save_req
                    return response

            elif not is_plan and not three_days_left and order_by:
                response_list = []
                order_value = ''

                if order_by == 'by_name':
                    order_value = 'user__name'
                elif order_by == 'day_left':
                    order_value = 'follow_period_end'
                today = datetime.datetime.now().timestamp()
                follow = Follow.objects.filter(trener_id=trener_id, follow_period_end__gt=int(today)).values().order_by('-'+str(order_value))
                if follow:
                    for fol in follow:
                        if fol.get('user_id'):
                            get_user = User.objects.get(pk=fol.get('user_id'))

                            fol['avatar'] = get_user.avatar
                            fol['name'] = get_user.name



                    response = {'follows': list(follow), 'message': 'is_plane:False and three_days_left:False '+"order_by"+str(order_by)}

                    save_req = save_user_request(url='follow/follow_filter', req=get_request, res=response,
                                                 req_headers=request.headers)
                    response['req_id'] = save_req
                    return response

                else:
                    response = {'follows': response_list, 'message': 'is_plane:True and three_days_left:True'}

                    save_req = save_user_request(url='follow/follow_filter', req=get_request, res=response,
                                                 req_headers=request.headers)
                    response['req_id'] = save_req
                    return response

            elif not is_plan and  three_days_left and not order_by:
                response_list = []
                order_value = ''

                today = datetime.datetime.now().timestamp()
                follow = Follow.objects.filter(trener_id=trener_id, follow_period_end__gt=int(today)).values()
                if follow:
                    for fol in follow:
                        if fol.get('user_id'):
                            get_user = User.objects.get(pk=fol.get('user_id'))

                            fol['avatar'] = get_user.avatar
                            fol['name'] = get_user.name



                    response = {'follows': list(follow), 'message': 'not is_plan and  three_days_left and not order_by'}

                    save_req = save_user_request(url='follow/follow_filter', req=get_request, res=response,
                                                 req_headers=request.headers)
                    response['req_id'] = save_req
                    return response

                else:
                    response = {'follows': response_list, 'message': 'is_plane:True and three_days_left:True'}

                    save_req = save_user_request(url='follow/follow_filter', req=get_request, res=response,
                                                 req_headers=request.headers)
                    response['req_id'] = save_req
                    return response







        except:
            aaa = logging.exception("follow/follow_filter")
            save_req = save_user_request(url='follow/follow_filter', req=get_request, res=aaa,
                                        req_headers=request.headers)
            response['req_id'] = save_req
            return response



        # response = {"error_title": "Follow",
        #             'error_description': 'Ошибка активации, пробный период ранее был активирован или недоступен'}
        #
        # save_req = save_user_request(url='follow/activate_follow', req=get_request, res=response,
        #                              req_headers=request.headers)
        # response['req_id'] = save_req
        #
        # return response



class Saverequest(models.Model):
    request_url = models.CharField(max_length=200, blank=True, default='', null=True)
    request_headers = models.TextField(max_length=3000, blank=True, default='', null=True)
    request = models.TextField(max_length=3000, blank=True, default='', null=True)
    response = models.TextField(max_length=3000, blank=True, default='', null=True)

    def __str__(self):
        return str(self.pk) + ' ' + self.request_url


class Languages(models.Model):
    header_key = models.CharField(blank=True, null=True, default='lang', max_length=200,
                                  verbose_name='Доступные языки ключ')
    header_value = models.CharField(blank=True, null=True, default='', max_length=200,
                                    verbose_name='Доступные языки значение')
    lang_val = models.CharField(blank=True, null=True, default='', max_length=200,
                                verbose_name='Доступные языки значение')
    url = models.CharField(blank=True, null=True, default='', max_length=200,
                           verbose_name='урл адрес картинки')

    def __str__(self):
        return self.lang_val


class Page(models.Model):
    page_name = models.CharField(default='', blank=True, max_length=200, verbose_name='Название страницы РУс')

    def __str__(self):
        return str(self.page_name)


class Translates(models.Model):
    CHOICES = (
        ('title', "title"),
        ('phone', "phone"),
        ('button', "button"),
        ('enter_sms_code', "enter_sms_code"),
        ('change_number', "change_number"),
        ('register_type_user', "register_type_user"),
        ('register_type_trener', "register_type_trener"),
        ('growth_title', "growth_title"),
        ('growth_val', "growth_val"),
        ('growth_type', "growth_type(см)"),

        ('weight_title', "weight_title"),
        ('weight_val', "weight_val"),
        ('weight_type', "weight_type (кг)"),

        ('age', "age"),
        ('date_of_birth', "date_of_birth"),
        ('sex', 'sex(пол записан статично в коде)'),
        ('avatar', 'avatar'),
        ('experience', 'experience'),
        ('price_title', 'price_title'),
        ('price_value', 'price_value'),
        ('price_type', 'price_type'),

        ('resend_sms', 'resend_sms'),
        ('passed_way', 'пройденный путь (метры)'),
        ('kkal', 'килокалории(ккал)'),
        ('time', 'время(timestamp)'),
        ('of', 'из'),
        ('day', 'день'),
        ('week', 'неделя'),
        ('month', 'месяц'),
        ('year', 'год'),
        ('steps_title', 'steps_title(шагов)'),
        ('monday', 'monday(понедельник)'),
        ('tuesday', 'Tuesday(вторник)'),
        ('wednesday', 'Wednesday(среда)'),
        ('thursday', 'Thursday(четверг)'),
        ('friday', 'Friday(пятница)'),
        ('saturday', 'Saturday(суббота)'),
        ('sunday', 'Sunday(воскресенье)'),

    )

    page = models.ForeignKey(Page, on_delete=models.DO_NOTHING, verbose_name='экран приложения', null=True)
    name_key = models.CharField(choices=CHOICES, default='', blank=True, max_length=200, verbose_name='ключ на анг')

    name_ru = models.CharField(default='', blank=True, max_length=200, verbose_name='Заголовок имения РУс')
    name_uz = models.CharField(default='', blank=True, max_length=200, verbose_name='Заголовок имения Уз кирилица')
    list_sex = models.CharField(default='', blank=True, max_length=200,
                                verbose_name='будет отправлен массив пола муж/жен')
    created = models.DateTimeField(verbose_name='дата создания', default=datetime.datetime.now)
    updated = models.DateTimeField(verbose_name='дата обновления', auto_now=True)
    last_req_timestamp = models.CharField(default='', blank=True, max_length=200,
                                          verbose_name='Последний запрос timestamp')

    # name_uzlat = models.CharField(default='', blank=True, max_length=200, verbose_name='Заголовок имения уз Латиница')

    def __str__(self):
        return self.name_ru

    def save(self, *args, **kwargs):
        print(self.last_req_timestamp, 1111)
        get_now_timestamp = datetime.datetime.now().timestamp()

        self.last_req_timestamp = int(get_now_timestamp)
        super().save(*args, **kwargs)


class User(models.Model):
    trener = models.ForeignKey('UserTrener', on_delete=models.DO_NOTHING, verbose_name='Тренер пользователя',
                               blank=True, null=True)
    name = models.CharField(default='', blank=True, max_length=200, verbose_name='Имя и фамилия', null=True)
    phone_number = models.CharField(default='', blank=True, max_length=20, verbose_name='Номер телефона', null=True)
    growth = models.PositiveIntegerField(default=0, verbose_name='Рост', blank=True, null=True)
    weight = models.PositiveIntegerField(default=0, blank=True, verbose_name='Вес в кг', null=True)
    age = models.PositiveIntegerField(default=0, blank=True, verbose_name='Возраст', null=True)
    sex = models.CharField(default='', blank=True, max_length=20, verbose_name="Пол", null=True)
    avatar = models.CharField(blank=True, max_length=2000, default=None, verbose_name='аватарка пользователя',
                              null=True)
    date_of_birth = models.CharField(default='', blank=True, max_length=20, verbose_name="Дата рождения", null=True)
    register_datetime = models.CharField(blank=True, verbose_name='Дата и время регистрации', max_length=100, null=True)
    normativ_from_trainer = models.PositiveIntegerField(default=0, blank=True,
                                                        verbose_name='Норматив установленный тренером', null=True)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.phone_number

    def get_user_age(self, date_of_birth):
        date_birth = datetime.datetime.strptime(date_of_birth, '%d.%m.%Y').date()
        today = datetime.date.today()
        birthday = date_birth.replace(year=today.year,

                                      month=date_birth.month + 1, day=1)
        if birthday > today:
            self.age = int((today.year - date_birth.year) - 1)
            self.save()
            print((today.year - date_birth.year) - 1)
        else:
            self.age = int(today.year - date_birth.year)
            self.save()

    def get_or_create_profile(self, request):
        avatar_img = None

        try:
            get_request = json.loads(request.body)
            get_device_type = request.headers.get('device')
            get_auth_key = request.headers.get('auth')

            print(get_device_type, get_auth_key)

            get_device = UserDevices.objects.get(device_type=get_device_type, auth_token=get_auth_key)
            if get_request:
                get_user, create_user = User.objects.get_or_create(
                    phone_number=get_device.phone_number,
                )
                if get_user:
                    get_user_week_stat = Statistics().get_stat_by_day(request, get_request={}, user_id=get_user.id,
                                                                      order_by='week')
                    update_fields = {}
                    get_device.user = get_user
                    get_device.save()
                    get_user.register_datetime = datetime.datetime.now()
                    if get_user.name != get_request.get('name') and get_request.get('name'):
                        get_user.name = get_request.get('name')
                        get_user.save()
                        update_fields["name"] = get_request.get('name')

                    if get_user.sex != get_request.get('sex') and get_request.get('sex'):
                        print('3334')
                        if str(get_request.get('sex')) == '1':
                            print('2')
                            get_user.sex = 'Мужской'
                            get_user.save()
                            print(111, get_user.sex)
                            update_fields["sex"] = 'Мужской'
                        elif str(get_request.get('sex')) == '2':
                            get_user.sex = 'Женский'
                            get_user.save()
                            update_fields["sex"] = 'Женский'
                        elif str(get_request.get('sex')) == '3':
                            get_user.sex = 'Мужской УЗ'
                            get_user.save()
                            update_fields["sex"] = 'Мужской УЗ'
                        elif str(get_request.get('sex')) == '4':
                            get_user.sex = 'Женский УЗ'
                            get_user.save()
                            update_fields["sex"] = 'Женский УЗ'
                        else:

                            pass

                    if get_user.age != get_request.get('age') and get_request.get('age'):
                        get_user.age = 'Мужской'
                        get_user.save()
                        update_fields["age"] = get_request.get('age')

                    if get_request.get('img'):

                        # print('get_request.get',get_request.get('img'))

                        if get_user.avatar != get_request.get('img').get('file') and get_request.get('img').get(
                                'file_type'):
                            get_file = file_decode(base_64=get_request.get('img').get('file'),
                                                   file_type=get_request.get('img').get('file_type'),
                                                   type='avatar_user', user_id=get_user.id)

                            update_fields["img"] = base_url + 'images/' + get_file
                            avatar_img = base_url + 'images/' + get_file
                            get_user.avatar = avatar_img
                            get_user.save()
                            print('avatar_img', avatar_img)

                    if get_user.growth != get_request.get('growth') and get_request.get('growth'):
                        get_user.growth = get_request.get('growth')
                        get_user.save()
                        update_fields["growth"] = get_request.get('growth')

                    if get_user.weight != get_request.get('weight') and get_request.get('weight'):
                        get_user.weight = get_request.get('weight')
                        get_user.save()
                        update_fields["weight"] = get_request.get('weight')

                    if get_user.date_of_birth != get_request.get('date_of_birth') and get_request.get('date_of_birth'):
                        get_user.date_of_birth = get_request.get('date_of_birth')
                        get_user.save()
                        get_user.get_user_age(get_user.date_of_birth)
                        update_fields["date_of_birth"] = get_request.get('date_of_birth')

                    if get_user.trener != get_request.get('trener_id') and get_request.get('trener_id'):
                        try:
                            get_user_trener = UserTrener.objects.get(pk=get_request.get('trener_id'))
                            get_user.trener = get_user_trener
                            get_user.save()

                            update_fields["trener_id"] = get_request.get('trener_id')
                        except:
                            print('222')
                            pass
                    if get_user.trener:
                        response = {'status': 200, "message": "profile_updated", "updated_fields": update_fields,
                                    'data': {'user_id': get_user.pk, 'name': get_user.name, 'age': get_user.age,
                                             'phone': get_user.phone_number, 'img': avatar_img,'normativ_from_trainer':get_user.normativ_from_trainer,
                                             'sex': get_user.sex, 'weight': get_user.weight, 'growth': get_user.growth,
                                             'date_of_birth': get_user.date_of_birth, "trener_id": get_user.trener.id}}

                    else:
                        response = {'status': 200, "message": "profile_updated", "updated_fields": update_fields,
                                    'data': {'user_id': get_user.pk, 'name': get_user.name, 'age': get_user.age,
                                             'phone': get_user.phone_number, 'img': avatar_img,'normativ_from_trainer':get_user.normativ_from_trainer,
                                             'sex': get_user.sex, 'weight': get_user.weight, 'growth': get_user.growth,
                                             'date_of_birth': get_user.date_of_birth, "trener_id": None}}

                    save_req = save_user_request(url='profile/', req=get_request, res=response,
                                                 req_headers=request.headers)
                    response['req_id'] = save_req
                    response['statistics'] = get_user_week_stat.get('statistics')
                    return response

                else:
                    response = None
                    get_device.user = get_user
                    get_device.save()

                    if get_user.trener:
                        print(3)

                        response = {'status': 200, "message": "profile_created",
                                    'data': {'user_id': get_user.pk, 'name': get_user.name, 'age': get_user.age,
                                             'phone': get_user.phone_number, 'img': avatar_img,'normativ_from_trainer':get_user.normativ_from_trainer,
                                             'sex': get_user.sex, 'weight': get_user.weight, 'growth': get_user.growth,
                                             'date_of_birth': get_user.date_of_birth, "trener_id": get_user.trener.id}}

                    save_req = save_user_request(url='profile/', req=get_request, res=response,
                                                 req_headers=request.headers)
                    response['req_id'] = save_req
                    return response

            else:
                print('1')
                try:
                    get_user_device = UserDevices.objects.get(device_type=get_device_type, auth_token=get_auth_key)
                    print(0, get_user_device.user)
                    if get_user_device.user and get_user_device.user.trener:
                        response = {'status': 200, "message": "profile",
                                    'data': {'user_id': get_user_device.user.id, 'name': get_user_device.user.name,
                                             'age': get_user_device.user.age,'normativ_from_trainer':get_user_device.user.normativ_from_trainer,
                                             'phone': get_user_device.user.phone_number,
                                             "trener_id": get_user_device.user.trener.id,
                                             'sex': get_user_device.user.sex, 'weight': get_user_device.user.weight,
                                             'growth': get_user_device.user.growth,
                                             'date_of_birth': get_user_device.user.date_of_birth, 'img': avatar_img, }}

                        save_req = save_user_request(url='profile/', req=get_request, res=response,
                                                     req_headers=request.headers)
                        response['req_id'] = save_req
                        return response
                    elif not get_user_device.user.trener:
                        response = {'status': 200, "message": "profile",
                                    'data': {'user_id': get_user_device.user.id, 'name': get_user_device.user.name,
                                             'age': get_user_device.user.age,
                                             'phone': get_user_device.user.phone_number,
                                             "trener_id": None, 'img': avatar_img, 'normativ_from_trainer':get_user_device.user.normativ_from_trainer,
                                             'sex': get_user_device.user.sex, 'weight': get_user_device.user.weight,
                                             'growth': get_user_device.user.growth,
                                             'date_of_birth': get_user_device.user.date_of_birth}}

                        save_req = save_user_request(url='profile/', req=get_request, res=response,
                                                     req_headers=request.headers)
                        response['req_id'] = save_req
                        return response
                    else:
                        response = {'status': 200,
                                    'data': {}, 'error_title': 'profile', 'error_description': "profile doesn't exist"}
                        save_req = save_user_request(url='profile/', req=get_request, res=response,
                                                     req_headers=request.headers)
                        response['req_id'] = save_req
                        return response

                except UserDevices.DoesNotExist:
                    response = {'status': 200,
                                'data': {}, 'error_title': 'profile', 'error_description': "profile doesn't exist"}
                    save_req = save_user_request(url='profile/', req=get_request, res=response,
                                                 req_headers=request.headers)
                    response['req_id'] = save_req
                    return response
        except Exception as e:
            import logging
            logging.error(e, exc_info=True)
            response = {"error_title": "Exception", 'error_description': str(e)}
            save_req = save_user_request(url='profile/', req=json.loads(request.body), res=response,
                                         req_headers=request.headers)
            response['req_id'] = save_req
            return response


    def add_normativ(self, user_id, normativ):
        try:
            get_user = User.objects.get(pk=user_id)
            get_user.normativ_from_trainer = int(normativ)
            get_user.save()
            return {'status':True, 'message':'add normativ', 'normativ':int(normativ)}
        except User.DoesNotExist:
            return {'error_title':'User', "error_description":"User DoesNotExist"}
#
#
class TrenerRate(models.Model):
    trener = models.ForeignKey('UserTrener', on_delete=models.DO_NOTHING, verbose_name='тренер', null=True, blank=True )
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING, verbose_name='пользователь', null=True, blank=True )

    rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Рейтинг тренера')

    def __str__(self):
        return str(self.id) + ' ' + str(self.trener.name)

#

class UserTrener(models.Model):
    users = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='пользователь', null=True, blank=True)
    name = models.CharField(default='', blank=True, max_length=200, verbose_name='Имя и фамилия', null=True)
    phone_number = models.CharField(default='', blank=True, max_length=200, verbose_name='Номер телефона', null=True)
    rate = models.PositiveIntegerField(default=0, verbose_name='Рейтинг Тренера', null=True)
    age = models.PositiveIntegerField(default=0, blank=True, verbose_name='Возраст', null=True)
    sex = models.CharField(default='', blank=True, max_length=20, verbose_name="Пол", null=True)
    price = models.PositiveIntegerField(default=0, blank=True, verbose_name="Цена", null=True)
    avatar = models.CharField(blank=True, max_length=2000, default=None, verbose_name='аватарка пользователя',
                              null=True)
    experience = models.PositiveIntegerField(default=0, blank=True, verbose_name="стаж работы", null=True)
    date_of_birth = models.CharField(default='', blank=True, max_length=20, verbose_name="Дата рождения", null=True)
    register_datetime = models.CharField(blank=True, max_length=200, verbose_name='Дата и время регистрации')

    def __str__(self):
        return str(self.name) + ' ' + str(self.phone_number)

    def get_trener_age(self, date_of_birth):
        print('get_trener_age, ', date_of_birth)
        date_birth = datetime.datetime.strptime(date_of_birth, '%d.%m.%Y').date()
        today = datetime.date.today()
        birthday = date_birth.replace(year=today.year,

                                      month=date_birth.month + 1, day=1)
        if birthday > today:
            self.age = int((today.year - date_birth.year) - 1)
            self.save()
            print((today.year - date_birth.year) - 1)
        else:
            self.age = int(today.year - date_birth.year)
            self.save()

    def get_or_create_profile(self, request):
        avatar_img = None
        response = {}
        try:
            get_request = json.loads(request.body)
            get_device_type = request.headers.get('device')
            get_auth_key = request.headers.get('auth')

            print(get_device_type, get_auth_key)

            get_device = UserDevices.objects.get(device_type=get_device_type, auth_token=get_auth_key)
            if get_request:
                get_user, create_user = UserTrener.objects.get_or_create(
                    phone_number=get_device.phone_number,
                )
                if get_user:

                    # get_treners_follow = Follow.objects.filter(trener_id=get_user.pk, is_active=True, is_trial=True).values()


                    update_fields = {}
                    get_device.trener = get_user
                    get_device.save()
                    get_user.register_datetime = datetime.datetime.now()
                    if get_user.name != get_request.get('name') and get_request.get('name'):
                        get_user.name = get_request.get('name')
                        get_user.save()
                        update_fields["name"] = get_request.get('name')
                    if get_user.sex != get_request.get('sex') and get_request.get('sex'):
                        if str(get_request.get('sex')) == '1':
                            get_user.sex = 'Мужской'
                            get_user.save()
                            update_fields["sex"] = 'Мужской'
                        elif str(get_request.get('sex')) == '2':
                            get_user.sex = 'Женский'
                            get_user.save()
                            update_fields["sex"] = 'Женский'
                        elif str(get_request.get('sex')) == '3':
                            get_user.sex = 'Мужской УЗ'
                            get_user.save()
                            update_fields["sex"] = 'Мужской УЗ'
                        elif str(get_request.get('sex')) == '4':
                            get_user.sex = 'Женский УЗ'
                            get_user.save()
                            update_fields["sex"] = 'Женский УЗ'
                        else:
                            pass

                    if get_user.age != get_request.get('age') and get_request.get('age'):
                        get_user.age = get_request.get('age')
                        get_user.save()
                        update_fields["age"] = get_request.get('age')

                    if get_request.get('img'):
                        if get_user.avatar != get_request.get('img').get('file') and get_request.get('img').get(
                                'file_type'):
                            get_file = file_decode(base_64=get_request.get('img').get('file'),
                                                   file_type=get_request.get('img').get('file_type'),
                                                   type='avatar_trener', user_id=get_user.id)

                            update_fields["img"] = base_url + 'images/' + get_file
                            avatar_img = base_url + 'images/' + get_file
                            get_user.avatar = avatar_img
                            get_user.save()
                            print('avatar_img', avatar_img)

                    if get_user.price != get_request.get('price') and get_request.get('price'):
                        get_user.price = int(get_request.get('price'))
                        get_user.save()
                        update_fields["price"] = get_request.get('price')

                    if get_user.experience != get_request.get('experience') and get_request.get('experience'):
                        get_user.experience = get_request.get('experience')
                        get_user.save()
                        update_fields["experience"] = get_request.get('experience')

                    if get_user.date_of_birth != get_request.get('date_of_birth') and get_request.get('date_of_birth'):
                        get_user.date_of_birth = get_request.get('date_of_birth')
                        get_user.save()
                        print('get_user.get_trener_age(get_user.date_of_birth)',
                              get_user.get_trener_age(get_user.date_of_birth))

                        get_user.get_trener_age(get_user.date_of_birth)
                        update_fields["date_of_birth"] = get_request.get('date_of_birth')
                    # trener_users = User.objects.filter(trener_id=get_user.pk).values()
                    # trener_follows = Follow.objects.filter(
                    #     Q(is_trial=True, is_active=False, trener_id=get_user.pk)) | Follow.objects.filter(
                    #     Q(is_trial=False, is_active=True, trener_id=get_user.pk)) | Follow.objects.filter(
                    #     Q(is_trial=True, is_active=True, trener_id=get_user.pk))

                    trener_follows = Follow().get_all_active_trener_follows(trener_id=get_user.pk)




                    if trener_follows:
                        response = {'status': 200, "message": "profile_updated", "updated_fields": update_fields,
                                    'data': {'trener_id': get_user.pk, 'is_user':False, 'name': get_user.name, 'age': get_user.age,
                                             'phone': get_user.phone_number, 'img': avatar_img, 'rate':get_user.rate,
                                             'sex': get_user.sex, 'price': get_user.price,
                                             'experience': get_user.experience, 'date_of_birth': get_user.date_of_birth,
                                             "trener_users_follows": trener_follows.get('trener_follows'),"follow_filter": trener_follows.get('follow_filter'),"sort": trener_follows.get('sort') }}






                    else:
                        print('22344')
                        response = {'status': 200, "message": "profile_updated", "updated_fields": update_fields,
                                    'data': {'trener_id': get_user.pk,'is_user':False, 'name': get_user.name, 'age': get_user.age,
                                             'phone': get_user.phone_number, 'img': avatar_img,'rate':get_user.rate,
                                             'sex': get_user.sex, 'price': get_user.price,
                                             'experience': get_user.experience,
                                             'date_of_birth': get_user.date_of_birth, "trener_users_follows": None, "follow_filter": trener_follows.get('follow_filter')}}

                    save_req = save_user_request(url='profile/', req=get_request, res=response,
                                                 req_headers=request.headers)
                    response['req_id'] = save_req
                    print('34')
                    print('res', response)
                    return response

                else:
                    print('2')
                    response = None
                    get_device.user = get_user
                    get_device.save()

                    if get_user.trener:
                        print(3)
                        trener_follows = Follow().get_all_active_trener_follows(trener_id=get_user.pk)

                        response = {'status': 200, "message": "profile_created",
                                    'data': {'trener_id': get_user.pk,'is_user':False, 'name': get_user.name, 'age': get_user.age,
                                             'phone': get_user.phone_number, 'img': avatar_img,
                                             'sex': get_user.sex, 'price': get_user.price,
                                             'experience': get_user.experience,'rate':get_user.rate,
                                             'date_of_birth': get_user.date_of_birth, "trener_users_follows": None,"follow_filter": trener_follows.get('follow_filter')}}

                    save_req = save_user_request(url='profile/', req=get_request, res=response,
                                                 req_headers=request.headers)
                    response['req_id'] = save_req
                    return response

            else:
                print('1')
                try:
                    get_user_device = UserDevices.objects.get(device_type=get_device_type, auth_token=get_auth_key)
                    trener_users = User.objects.filter(trener_id=get_user_device.user.pk).values()


                    if get_user_device.trener and get_user_device.trener.users:
                        response = {'status': 200, "message": "profile",
                                    'data': {'trener_id': get_user_device.trener.id, 'is_user':False,'name': get_user_device.trener.name,
                                             'age': get_user_device.trener.age, 'img': avatar_img,
                                             'phone': get_user_device.trener.phone_number,
                                             "trener_users": list(trener_users),'rate':get_user_device.trener.rate,
                                             'sex': get_user_device.trener.sex, 'price': get_user_device.trener.price,
                                             'experience': get_user_device.trener.experience,
                                             'date_of_birth': get_user_device.trener.date_of_birth}}

                        save_req = save_user_request(url='profile/', req=get_request, res=response,
                                                     req_headers=request.headers)
                        response['req_id'] = save_req
                        return response
                    elif not get_user_device.user.trener:
                        response = {'status': 200, "message": "profile",
                                    'data': {'trener_id': get_user_device.trener.id, 'is_user':False,'name': get_user_device.trener.name,
                                             'age': get_user_device.trener.age,
                                             'phone': get_user_device.trener.phone_number,
                                             "trener_users": [], 'img': avatar_img,'rate':get_user_device.trener.rate,
                                             'sex': get_user_device.trener.sex, 'price': get_user_device.trener.price,
                                             'experience': get_user_device.trener.experience,

                                             'date_of_birth': get_user_device.trener.date_of_birth}}

                        save_req = save_user_request(url='profile/', req=get_request, res=response,
                                                     req_headers=request.headers)
                        response['req_id'] = save_req
                        return response
                    else:
                        response = {'status': 200,
                                    'data': {}, 'error_title': 'profile', 'error_description': "profile doesn't exist"}
                        save_req = save_user_request(url='profile/', req=get_request, res=response,
                                                     req_headers=request.headers)
                        response['req_id'] = save_req
                        return response

                except UserDevices.DoesNotExist:
                    response = {'status': 200,
                                'data': {}, 'error_title': 'profile', 'error_description': "profile doesn't exist"}
                    save_req = save_user_request(url='profile/', req=get_request, res=response,
                                                 req_headers=request.headers)
                    response['req_id'] = save_req
                    return response

        except Exception as e:
            import logging
            response = {"error_title": "Exception", 'error_description': str(e),
                        "traceback": str(logging.error(e, exc_info=True))}
            logging.error(e, exc_info=True)
            save_req = save_user_request(url='profile/', req=json.loads(request.body), res=response,
                                         req_headers=request.headers)
            response['req_id'] = save_req
            return response

    def get_treners_list(self, request, page=None, user_id=None, get_request=None, order_by=None):
        pag_trener_list_filtered = None
        treners_list = []
        user_follow  = None
        my_trener  = {}
        user_follow_resp = {}
        # print('or_', order_by)
        if order_by and not page:
            treners_list = UserTrener.objects.all().order_by('-' + str(order_by)).values().exclude(name='')
        else:
            treners_list = UserTrener.objects.all().order_by('-name').values().exclude(name='')
        if treners_list and not page and user_id:
            page = 1
            paginator = Paginator(list(treners_list), 3)
            pag_trener_list_filtered = paginator.get_page(page)
            all_pages = paginator.num_pages
            current_page = pag_trener_list_filtered.number
            get_user_trener = User.objects.get(pk=user_id)


            for treners in pag_trener_list_filtered:
                if get_user_trener.trener:
                    try:
                        user_follow = Follow.objects.get(user_id=user_id, trener_id=treners.get('id'))
                        user_follow_resp = {'follow':{'id':user_follow.pk, 'trener_id':user_follow.trener.pk, 'is_trial':user_follow.is_trial,
                                                      'is_active':user_follow.is_active, 'follow_period_start':user_follow.follow_period_start, 'follow_period_end':user_follow.follow_period_end}}
                    except Follow.DoesNotExist:
                        user_follow = None


                    if user_follow:
                        if treners.get('id') == get_user_trener.trener.id and user_follow.is_active or user_follow.is_trial:
                            treners['my_trener'] = True
                            my_trener['my_trener'] = treners
                            my_trener['follow'] = user_follow_resp.get('follow')


                        else:
                            treners['my_trener'] = False

                else:
                    treners['my_trener'] = False

            response = {'status': 200, "message": "treners_list", 'all_pages': all_pages, 'current_page': current_page,
                        'data': {'treners_list': list(pag_trener_list_filtered)}}

            if request.headers.get('lang') == 'rus':
                response['order_by'] = {'name': 'По имени', 'rate': "По рейтингу", 'age': 'По возрасту'}
            else:
                response['order_by'] = {'name': 'По имени Уз', 'rate': "По рейтингу Уз", 'age': 'По возрасту Уз'}


        else:
            paginator = Paginator(list(treners_list), 3)
            pag_trener_list_filtered = paginator.get_page(page)
            all_pages = paginator.num_pages
            current_page = pag_trener_list_filtered.number
            get_user_trener = User.objects.get(pk=user_id)
            for treners in pag_trener_list_filtered:
                if get_user_trener.trener:
                    try:
                        user_follow = Follow.objects.get(user_id=user_id, trener_id=treners.get('id'))
                    except Follow.DoesNotExist:
                        user_follow = None
                    if user_follow:
                        if treners.get('id') == get_user_trener.trener.id and user_follow.is_active or user_follow.is_trial:
                            treners['my_trener'] = True
                            my_trener['my_trener'] = treners
                            my_trener['follow'] = user_follow_resp.get('follow')
                        else:
                            treners['my_trener'] = False
                else:
                    treners['my_trener'] = False

            response = {'status': 200, "message": "treners_list", 'all_pages': all_pages, 'current_page': current_page,
                        'data': {'treners_list': list(pag_trener_list_filtered)}}
            if request.headers.get('lang') == 'rus':
                response['order_by'] = {'name': 'По имени', 'rate': "По рейтингу", 'age': 'По возрасту'}
            else:
                response['order_by'] = {'name': 'По имени Уз', 'rate': "По рейтингу Уз", 'age': 'По возрасту Уз'}

        save_req = save_user_request(url='treners/', req=get_request, res=response,
                                     req_headers=request.headers)
        response['req_id'] = save_req
        response['data']['my_trener'] = my_trener.get('my_trener')
        response['data']['follow'] = my_trener.get('follow')

        print('response', response)
        return response

    def rate_trener(self, request, rate, trener_id, user_id):
        get_request = None
        from django.db.models import Avg, Max, Min, Sum
        try:
            get_request = json.loads(request.body)
            rate_trener = TrenerRate.objects.create(trener_id=trener_id, rate=rate, user_id=user_id)
            print('rate_trener',rate_trener)

            all_rate = TrenerRate.objects.filter(trener_id=trener_id).aggregate(Avg('rate'))
            print(11111)
            get_trener = UserTrener.objects.get(pk=trener_id)
            print('eee', get_trener)
            get_trener.rate = all_rate.get('rate__avg')
            get_trener.save()

            response = {'status': 200, "data": {'result':True, 'rate':all_rate.get('rate__avg'),'trener_id':get_trener.id}}

            save_req = save_user_request(url='treners_rate/', req=get_request, res=response,
                                         req_headers=request.headers)
            response['req_id'] = save_req
            return response
        except Exception as e:
            print(e)
            response = {'error_title':'Trener', "error_description":'Does not Exist'}

            save_req = save_user_request(url='treners_rate/', req=get_request, res=response,
                                         req_headers=request.headers)
            response['req_id'] = save_req

            return response



class UserDevices(models.Model):
    phone_number = models.CharField(default='', blank=True, max_length=200, verbose_name='Номер телефона')
    device_type = models.CharField(default='', blank=True, max_length=200, verbose_name='тип уствройства')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Пользователь', null=True, blank=True)
    trener = models.ForeignKey(UserTrener, on_delete=models.DO_NOTHING, verbose_name='Тренер', null=True,
                               blank=True)

    device_token = models.CharField(blank=True, default='', max_length=200,
                                    verbose_name='Токен устройства', null=True)
    auth_token = models.CharField(blank=True, default='', max_length=200,
                                  verbose_name='Токен полученный после подтверждения номера', null=True)

    push_token = models.CharField(blank=True, default='', max_length=500,
                                  verbose_name='Токен для отправки пуш уведоблений', null=True)
    is_activate = models.BooleanField(default=False, verbose_name='Устройство активировано')
    hash = models.CharField(blank=True, default='', max_length=300,
                            verbose_name='Хеш для подтверждения девайса', null=True)
    time_to_resend_sms = models.PositiveIntegerField(default=60, verbose_name='Время для повторной отправки смс',
                                                     null=True)

    sms = models.CharField(blank=True, default='', max_length=200, verbose_name='Смс для активации', null=True)

    def __str__(self):
        return self.device_type


class Statistics(models.Model):
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING, verbose_name='Пользователь')
    kkal = models.PositiveIntegerField(blank=True, default=0, verbose_name='Кол-во килокалорий')
    step_counts = models.PositiveIntegerField(blank=True, default=0, verbose_name='Кол-во шагов')
    meters_counts = models.PositiveIntegerField(blank=True, default=0,  verbose_name='Кол-во метров')
    time_counts = models.PositiveIntegerField(blank=True, default=0,  verbose_name='общее кол-во времени')
    created_at = models.PositiveIntegerField(verbose_name='дата статистики', blank=True)

    def __str__(self):
        return str(self.user.name)

    def get_stat_by_day(self, request, get_request,  user_id, order_by):
        today = datetime.date.today()
        str_today_start = str(today) + ' 00:00:00'
        str_today_end = str(today) + ' 23:59:59'

        today_timestamp = time.mktime(datetime.datetime.strptime(str(str_today_start), "%Y-%m-%d %H:%M:%S").timetuple())
        end_time__and_today = time.mktime(
            datetime.datetime.strptime(str(str_today_end), "%Y-%m-%d %H:%M:%S").timetuple())
        monday = today - datetime.timedelta(days=today.weekday())
        str_monday_start = str(monday) + ' 00:00:00'
        str_monday_end = str(monday) + ' 23:59:59'
        end_time__and_mondey = time.mktime(
            datetime.datetime.strptime(str(str_monday_end), "%Y-%m-%d %H:%M:%S").timetuple())
        start_time__and_mondey = time.mktime(
            datetime.datetime.strptime(str(str_monday_start), "%Y-%m-%d %H:%M:%S").timetuple())

        # print('today_timestamp', today_timestamp)
        # print('today_timestamp+3600', int(today_timestamp) + 7200)
        #
        # print('start_time_today', end_time__and_today)

        if user_id and order_by == 'day':
            get_user_stat = Statistics.objects.filter(created_at__gte=int(today_timestamp), created_at__lte=int(end_time__and_today), user_id=user_id)
            result = {}
            kkal = 0
            steps = 0
            meters = 0
            total_time = 0
            if get_user_stat:

                for stat in get_user_stat:
                    kkal += int(stat.kkal)
                    steps += int(stat.step_counts)
                    total_time += int(stat.time_counts)
                    meters += int(stat.meters_counts)
                    result['kkal'] = kkal
                    result['meters'] = meters
                    result['steps'] = steps
                    result['total_time'] = total_time
                    result['normativ'] = stat.user.normativ_from_trainer

                get_by_hour = get_stat_by_hour(user_id=user_id)
                result['by_hour'] = get_by_hour
                response = {'status': 200, "message": "by_day", 'statistics': result}
                save_req = save_user_request(url='user_statistics/', req=get_request, res=response,
                                             req_headers=request.headers)
                response['req_id'] = save_req
                # print('response',response)
                return response

            else:
                result['kkal'] = kkal
                result['meters'] = meters
                result['steps'] = steps
                result['total_time'] = total_time
                result['normativ'] = 0

                get_by_hour = get_stat_by_hour(user_id=user_id)
                result['by_hour'] = get_by_hour
                response = {'status': 200, "message": "by_day", 'statistics': result}
                save_req = save_user_request(url='user_statistics/', req=get_request, res=response,
                                             req_headers=request.headers)
                response['req_id'] = save_req
                print('response', response)
                return response

            # print('get_user_stat',get_user_stat)

        elif user_id and order_by == 'week':
            get_user_stat = Statistics.objects.filter(created_at__gte=int(start_time__and_mondey), created_at__lte=int(end_time__and_today), user_id=user_id)
            result = {}
            # print('start_time__and_mondey',start_time__and_mondey, 'end_time__and_today', end_time__and_today)

            kkal = 0
            steps = 0
            meters = 0
            total_time = 0

            if get_user_stat:

                for stat in get_user_stat:
                    kkal += int(stat.kkal)
                    steps += int(stat.step_counts)
                    total_time += int(stat.time_counts)
                    # print('total_time',total_time)
                    meters += int(stat.meters_counts)
                    # print('meters', stat.meters_counts)

                    result['kkal'] = kkal
                    result['meters'] = meters
                    result['steps'] = steps
                    result['total_time'] = total_time
                    result['normativ'] = stat.user.normativ_from_trainer
                    # print(111)

                get_by_week = get_stat_by_weekday(user_id=user_id)
                result['by_day'] = get_by_week
                response = {'status': 200, "message": "by_week", 'statistics': result}
                save_req = save_user_request(url='user_statistics/', req=get_request, res=response,
                                                 req_headers=request.headers)
                response['req_id'] = save_req
                # print('response',response)
                return response

            # print('get_user_stat',get_user_stat)

            else:
                result['kkal'] = kkal
                result['meters'] = meters
                result['steps'] = steps
                result['total_time'] = total_time
                result['normativ'] = 0

                get_by_hour = get_stat_by_weekday(user_id=user_id)
                result['by_day'] = get_by_hour
                response = {'status': 200, "message": "by_week", 'statistics': result}
                save_req = save_user_request(url='user_statistics/', req=get_request, res=response,
                                             req_headers=request.headers)
                response['req_id'] = save_req
                print('response', response)
                return response

        elif user_id and order_by == 'month':
            print('1')
            now = datetime.date.today()
            days_count_in_month = calendar.monthrange(now.year, now.month)[1]
            get_month_day_start = str(now.year) + '-' + str(now.month) + '-' + str(1) + ' 00:00:00'
            get_month_day_end = str(now.year) + '-' + str(now.month) + '-' + str(days_count_in_month) + ' 23:59:59'

            day_timestamp_start = time.mktime(
                datetime.datetime.strptime(str(get_month_day_start), "%Y-%m-%d %H:%M:%S").timetuple())
            day_timestamp_end = time.mktime(
                datetime.datetime.strptime(str(get_month_day_end), "%Y-%m-%d %H:%M:%S").timetuple())

            get_user_stat = Statistics.objects.filter(created_at__gte=int(day_timestamp_start), created_at__lte=int(day_timestamp_end), user_id=user_id)
            result = {}
            print(get_user_stat)
            # print('start_time__and_mondey',start_time__and_mondey, 'end_time__and_today', end_time__and_today)

            # print('get_user_stat',get_user_stat)
            kkal = 0
            steps = 0
            total_time = 0
            meters = 0

            if get_user_stat:

                for stat in get_user_stat:
                    kkal += int(stat.kkal)
                    steps += int(stat.step_counts)
                    total_time += int(stat.time_counts)
                    meters += int(stat.meters_counts)
                    result['kkal'] = kkal
                    result['meters'] = meters
                    result['steps'] = steps
                    result['total_time'] = total_time
                    result['normativ'] = stat.user.normativ_from_trainer

                get_by_week = get_stat_by_month(user_id=user_id)
                # print('get_by_week',get_by_week)
                result['by_month'] = get_by_week
                response = {'status': 200, "message": "by_month", 'statistics': result}
                save_req = save_user_request(url='user_statistics/', req=get_request, res=response,
                                                 req_headers=request.headers)
                response['req_id'] = save_req
                # print('response',response)
                return response

            # print('get_user_stat',get_user_stat)

            else:
                result['kkal'] = kkal
                result['meters'] = meters
                result['steps'] = steps
                result['total_time'] = total_time
                result['normativ'] = 0

                get_by_hour = get_stat_by_month(user_id=user_id)
                result['by_month'] = get_by_hour
                response = {'statistics': result}
                save_req = save_user_request(url='user_statistics/', req=get_request, res=response,
                                             req_headers=request.headers)
                response['req_id'] = save_req
                # print('response', response)
                return response

        elif user_id and order_by == 'year':
            # print('1')
            now = datetime.date.today()
            # print('now',now)
            days_count_in_month = calendar.monthrange(now.year, 1)[1]
            # print('days_count_in_month',days_count_in_month)
            get_month_day_start = str(now.year) + '-' + str(1) + '-' + str(1) + ' 00:00:00'
            get_month_day_end = str(now.year) + '-' + str(now.month) + '-' + str(calendar.monthrange(now.year, now.month)[1]) + ' 23:59:59'

            day_timestamp_start = time.mktime(
                datetime.datetime.strptime(str(get_month_day_start), "%Y-%m-%d %H:%M:%S").timetuple())
            day_timestamp_end = time.mktime(
                datetime.datetime.strptime(str(get_month_day_end), "%Y-%m-%d %H:%M:%S").timetuple())

            # print('day_timestamp_start',day_timestamp_start)
            # print('day_timestamp_end',day_timestamp_end)

            get_user_stat = Statistics.objects.filter(created_at__gte=int(day_timestamp_start), created_at__lte=int(day_timestamp_end), user_id=user_id)
            result = {}
            print(get_user_stat)
            # print('start_time__and_mondey',start_time__and_mondey, 'end_time__and_today', end_time__and_today)

            # print('get_user_stat',get_user_stat)
            kkal = 0
            steps = 0
            total_time = 0
            meters = 0

            if get_user_stat:

                for stat in get_user_stat:
                    kkal += int(stat.kkal)
                    steps += int(stat.step_counts)
                    total_time += int(stat.time_counts)
                    meters += int(stat.meters_counts)
                    result['kkal'] = kkal
                    result['meters'] = meters
                    result['steps'] = steps
                    result['total_time'] = total_time
                    result['normativ'] = stat.user.normativ_from_trainer

                get_by_week = get_stat_by_year(user_id=user_id)
                # print('get_by_week',get_by_week)
                result['by_year'] = get_by_week
                response = {'status': 200, "message": "by_year", 'statistics': result}
                save_req = save_user_request(url='user_statistics/', req=get_request, res=response,
                                                 req_headers=request.headers)
                response['req_id'] = save_req
                # print('response',response)
                return response

            # print('get_user_stat',get_user_stat)

            else:
                result['kkal'] = kkal
                result['meters'] = meters
                result['steps'] = steps
                result['total_time'] = total_time
                result['normativ'] = 0

                get_by_hour = get_stat_by_year(user_id=user_id)
                result['by_year'] = get_by_hour
                response = {'statistics': result}
                save_req = save_user_request(url='user_statistics/', req=get_request, res=response,
                                             req_headers=request.headers)
                response['req_id'] = save_req
                # print('response', response)

                return response

        else:
            return {}

    def check_user_normativ(self, request, user_id):
        get_lang = request.headers.get('lang')
        push_service = SentPush()
        today = datetime.date.today()
        str_today_start = str(today) + ' 00:00:00'
        str_today_end = str(today) + ' 23:59:59'
        today_timestamp = time.mktime(datetime.datetime.strptime(str(str_today_start), "%Y-%m-%d %H:%M:%S").timetuple())
        try:
            get_user = User.objects.get(pk=user_id)
            user_push_token = UserDevices.objects.filter(user_id=user_id,is_activate=True)
        except User.DoesNotExist:
            response = {'error_title': 'User', "user_description":'DoesNotExist'}
            save_req = save_user_request(url='user_statistics/', req={'from_check_normativ':True}, res=response,
                                         req_headers=request.headers)
            response['req_id'] = save_req
            return response

        get_user_stat_by_day_summary = Statistics().get_stat_by_day(request,get_request={'from_check_normativ':True},user_id=user_id, order_by='day')
        if get_user_stat_by_day_summary:
            get_obj_stat = get_user_stat_by_day_summary.get('statistics')
            steps_by_day_summary = get_obj_stat.get('steps')
            if steps_by_day_summary == int(get_user.normativ_from_trainer):

                """need sent push notification to user and trener"""
                if get_lang == 'rus':
                    try:
                        for token in user_push_token:
                            if token.device_type.lower() == 'ios':
                                push_service.send_push_notification_ios(registration_id=[token.push_token],message_title='Поздравляем!', message_body='Вы успешно прошли дневную цель')
                            else:
                                push_service.send_push_notification_android(registration_id=[token.push_token],message_title='Поздравляем!', message_body='Вы успешно прошли дневную цель')


                    except:
                        pass
                else:
                    try:
                        for token in user_push_token:
                            if token.device_type.lower() == 'ios':
                                push_service.send_push_notification_ios(registration_id=[token.push_token],message_title='Поздравляем!', message_body='Вы успешно прошли дневную цель')
                            else:
                                push_service.send_push_notification_android(registration_id=[token.push_token],message_title='Поздравляем!', message_body='Вы успешно прошли дневную цель')


                    except:
                        pass

            elif steps_by_day_summary > int(get_user.normativ_from_trainer):
                try:
                    for token in user_push_token:

                        if token.device_type.lower() == 'ios':
                            push_service.send_push_notification_ios(registration_id=[token.push_token],
                                                                        message_title='Поздравляем!',
                                                                        message_body='Вы прошли уже больше ' + str(
                                                                            get_user.normativ_from_trainer) + 'шагов')

                        else:
                            push_service.send_push_notification_android(registration_id=[token.push_token],
                                                                        message_title='Поздравляем!',
                                                                        message_body='Вы прошли уже больше ' + str(get_user.normativ_from_trainer) + 'шагов')

                except:
                    pass
                else:
                    try:
                        for token in user_push_token:
                            if token.device_type.lower() == 'ios':
                                push_service.send_push_notification_ios(registration_id=[token.push_token],
                                                                message_title='Поздравляем! uzb',
                                                                message_body='Вы прошли уже больше ' + str(get_user.normativ_from_trainer) + 'шагов uzb')

                            else:
                                push_service.send_push_notification_ios(registration_id=[token.push_token],
                                                                        message_title='Поздравляем! uzb',
                                                                        message_body='Вы прошли уже больше ' + str(
                                                                            get_user.normativ_from_trainer) + 'шагов uzb')


                    except:
                        pass




class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Пользователь', null=True, blank=True)
    user_trener = models.ForeignKey(UserTrener, on_delete=models.DO_NOTHING, verbose_name='Тренер', null=True, blank=True)

    def __str__(self):
        return str(self.id)


class ChatMessages(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.DO_NOTHING, verbose_name='ID ЧАТА',null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='написал пользователь',null=True, blank=True)
    user_trener = models.ForeignKey(UserTrener, on_delete=models.DO_NOTHING, verbose_name='написал тренер',null=True, blank=True)

    message_create_at = models.PositiveIntegerField(verbose_name='дата и время сообщения', blank=True, null=True)
    is_read = models.BooleanField(default=False, verbose_name='Прочитано или нет')
    content_url = models.CharField(blank=True, verbose_name='ссылка на файлы', null=True, max_length=500)
    content = models.TextField(max_length=3000, verbose_name='сообщение', null=TrenerRate, blank=TrenerRate)

    def __str__(self):
        return str(self.id)



    def get_active_chat(self, trener_id=None, user_id=None):
        get_chats = None
        chat_messagets = []
        if trener_id:
            get_chats = Chat.objects.filter(user_trener=trener_id).values().order_by('-id')
        else:
            get_chats = Chat.objects.filter(user_id=user_id).values().order_by('-id')


        return {'chat_list':list(get_chats)}



    def get_only_un_read(self, chat_id):
        response=None
        try:
            get_chat = Chat.objects.get(pk=chat_id)
            get_messages = ChatMessages.objects.filter(chat_id=chat_id, is_read=False).values()
            response = {'chat':{'id':get_chat.pk, 'messages':list(get_messages)}}

        except:
            response = {'error_title':'chat', 'error_description':'chat_doesnt_exist'}

        return response

    def get_messages_from_chat(self,chat_id, page=None):
        if page:
            get_messages = ChatMessages.objects.filter(chat_id=chat_id).order_by('message_create_at')

            paginator = Paginator(get_messages, 15)
            messages = paginator.get_page(page)
            response = {'chat_messages':list(messages), 'all_pages':paginator.num_pages, 'current_page':page}
            return response
        else:
            get_messages = ChatMessages.objects.filter(chat_id=chat_id).order_by('message_create_at')[:15].values()
            paginator = Paginator(get_messages, 15)
            response = {'chat_messages': get_messages, 'all_pages':paginator.num_pages, 'current_page':page}
            return response

    def mark_messages_as_read(self, message_list_id):
        get_messages = ChatMessages.objects.filter(id__in=message_list_id)
        print('get_messages_ID',get_messages)
        for message in get_messages:
            message.is_read = True
            message.save()

        return {'status':200, 'mark_messages':True, 'marked_messages':list(get_messages.values())}

    def get_last_massage(self, chat_id):
        message = ChatMessages.objects.filter(chat_id=chat_id).order_by('message_create_at').values()[:10]
        response = {}
        message_list = []
        for item in message:
            print('item',item)
            if item:
                response['id'] = item.get('id')
                response['chat_id'] = item.get('chat_id')
                response['message_create_at'] = item.get('message_create_at')
                response['is_read'] = item.get('is_read')
                response['content_url'] = item.get('content_url')

                response['content'] = item.get('content')
                if item.get('user_id'):
                    try:
                        get_user = User.objects.get(pk=item.get('user_id'))
                        response['avatar'] = get_user.avatar
                        response['name'] = get_user.name
                        response['user_id'] = get_user.pk

                    except:
                        pass
                if item.get('user_trener_id'):
                    try:
                        get_user = UserTrener.objects.get(pk=item.get('user_trener_id'))
                        response['avatar'] = get_user.avatar
                        response['name'] = get_user.name
                        response['trener_id'] = get_user.pk
                    except:
                        pass

                message_list.append(response)

        return {'last_message':response}











