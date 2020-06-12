from django.shortcuts import render, HttpResponseRedirect
import random
from STEP_COUNTER_API_APP.models import User, UserDevices, UserTrener,TrenerRate, Saverequest, Statistics, Languages,Translates, Page, Follow, PaymentMetod, ChatMessages, Chat
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib
import uuid
import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Q
import calendar
from STEP_COUNTER_API_APP.PUSH_NOTIFICATION import SentPush


# Create your views here.


def socket_settings():
    return {"socket":{'socket_server': '94.158.54.101', 'socket_port': 8099, 'type': 'socketIO'}}


def sms(phone_number):
    get_sms = random.randint(1234, 9999)
    print('get_sms', get_sms)
    sms = 111111
    #return get_sms
    return sms


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

"""generate sms number"""



def check_user_auth(auth):
    try:
        check_auth = UserDevices.objects.get(auth_token=auth)
        if check_auth:
            return {'result':True}

    except Exception as e:
        return {'result':False, 'error':str(e)}



"""registraion new user device"""


@csrf_exempt
def get_available_languages(request):
    """EMPTY POST REQUST"""
    if request.method == 'POST':
        get_langs = Languages.objects.all().values('header_key', 'lang_val','url', 'header_value')
        get_translate = Translates.objects.filter(page__page_name='language').values()
        if get_translate:
            response = {'status': 200, 'req_id': '', 'languages':list(get_langs)}
        else:
            response = {'status': 200, 'req_id': '', 'languages':list(get_langs)}

        save_req = save_user_request(url='/api/available_langs/', req='empty', res=response, req_headers=request.headers)
        response['req_id'] = save_req
        return JsonResponse(data=response)


    else:
        return JsonResponse(data={"error_title": 'request metod', "error_description": 'Incorrect'})




@csrf_exempt
def page_translate(request):
    """EMPTY POST REQUST"""
    resp = {}
    if request.method == 'POST':
        try:
            get_request = json.loads(request.body)
            get_timestamp = get_request.get('timestamp')
            if get_timestamp:
                get_page_by_name = Page.objects.all()
                for page in get_page_by_name:
                    response = []
                    translates = Translates.objects.filter(page_id=page.id).values()
                    for translate in translates:
                        updated =translate.get('updated').timestamp()
                        created =translate.get('created').timestamp()
                        print('int(updated)',int(updated))
                        get_now_timestamp = datetime.datetime.now().timestamp()

                        if int(get_timestamp) < int(updated):
                            print('2')
                            if translate.get('name_key') == 'sex':

                                response.append(
                                    {translate.get('name_key'): {'rus': [{'id':1, "value":"Музской"}, {'id':2, "value":"Женский"}], 'uz': [{'id':3, "value":"Музской УЗ"}, {'id':4, "value":"Женский УЗ"}]}})

                                resp[page.page_name] = response
                                resp['timestamp'] = int(get_now_timestamp)

                            else:
                                response.append(
                                    {translate.get('name_key'): {'rus': translate.get('name_ru'), 'uz': translate.get('name_uz')}})
                                resp[page.page_name] = response
                                resp['timestamp'] = int(get_now_timestamp)

                save_req = save_user_request(url='/api/translate', req=get_request, res=resp, req_headers=request.headers)
                resp['req_id'] = save_req
                return JsonResponse(data=resp)
            else:

                save_req = save_user_request(url='/api/translate', req=get_request, res=resp,
                                             req_headers=request.headers)
                resp['req_id'] = save_req
                resp["error_title"] = 'json'
                resp["error_description"]= 'need timestamp'

                return JsonResponse(data=resp)


        except Exception as e:
            print('3333')
            get_page_by_name = Page.objects.all()
            for page in get_page_by_name:
                response = []
                translates = Translates.objects.filter(page_id=page.id).values()
                for translate in translates:
                    updated = translate.get('updated').timestamp()
                    created = translate.get('created').timestamp()
                    get_now_timestamp = datetime.datetime.now().timestamp()


                    if translate.get('name_key') == 'sex':

                        response.append(
                            {translate.get('name_key'): {
                                'rus': [{'id': 1, "value": "Музской"}, {'id': 2, "value": "Женский"}],
                                'uz': [{'id': 3, "value": "Музской УЗ"}, {'id': 4, "value": "Женский УЗ"}]}})

                        resp[page.page_name] = response
                        resp['timestamp'] = int(get_now_timestamp)

                    else:
                        response.append(
                            {translate.get('name_key'): {'rus': translate.get('name_ru'),
                                                         'uz': translate.get('name_uz')}})
                        resp[page.page_name] = response
                        resp['timestamp'] = int(get_now_timestamp)

            save_req = save_user_request(url='/api/auth/code/', req={}, res=resp, req_headers=request.headers)
            resp['req_id'] = save_req
            return JsonResponse(data=resp)



    else:
        return JsonResponse(data={"error_title": 'request metod', "error_description": 'Incorrect'})


@csrf_exempt
def device_auth(request):
    if request.method == 'POST':
        try:
            get_request = json.loads(request.body)
            get_phone = get_request.get('phone_number')
            get_device_type = request.headers.get('device')
            get_device_token = get_request.get('device_token')
            get_push_token = get_request.get('push_token')
            get_sms = get_request.get('sms_code')
            timestamp = datetime.datetime.now().timestamp()
            hash = (str(get_device_token)+ str(timestamp)).encode()
            gen_hash = hashlib.sha256(hash).hexdigest()



            get_device, create_device = UserDevices.objects.get_or_create(device_type=get_device_type,
                                                                          device_token=get_device_token)
            print(get_device, create_device)
            get_available_lang = Languages.objects.all().values('header_key', 'lang_val')

            if create_device:
                update_device = UserDevices.objects.get(pk=get_device.pk)

                update_device.hash = gen_hash
                gen_sms_code = sms(phone_number=get_phone)
                update_device.sms = gen_sms_code
                update_device.phone_number = get_phone
                update_device.push_token = get_push_token
                update_device.save()
                response = {'status': 200, 'sms_status': 'sended', 'sms_resend_time': update_device.time_to_resend_sms,
                            'data': {'device_id': get_device.pk, 'hash': gen_hash, 'new_device': True},
                            'languages': list(get_available_lang)}

                save_req = save_user_request(url='/api/auth/code/', req=get_request, res=response, req_headers=request.headers)
                response['req_id'] = save_req
                return JsonResponse(data=response)
            else:
                update_device = UserDevices.objects.get(pk=get_device.pk)
                update_device.hash = gen_hash
                update_device.phone_number = get_phone
                gen_sms_code = sms(phone_number=get_phone)
                update_device.sms = gen_sms_code
                update_device.push_token = get_push_token
                update_device.save()
                response = {'status': 200, 'req_id': '', 'sms_status': 're_sended',
                            'sms_resend_time': get_device.time_to_resend_sms,
                            'data': {'device_id': get_device.pk, 'hash': gen_hash, "new_device": False},
                            'languages': list(get_available_lang)}

                save_req = save_user_request(url='/api/auth/code/', req=get_request, res=response,req_headers=request.headers)
                response['req_id'] = save_req
                return JsonResponse(data=response)
        except Exception as e:
            return JsonResponse(data={"error_title": 'Exception', "error_description": str(e)})

    else:
        return JsonResponse(data={"error_title": 'request metod', "error_description": 'Incorrect'})


@csrf_exempt
def code_confirm(request):
    if request.method == 'POST':
        try:
            get_request = json.loads(request.body)
            get_device_type = request.headers.get('device')
            get_sms = get_request.get('sms_code')
            gen_hash = get_request.get('hash')
            get_available_lang = Languages.objects.all().values('header_key', 'lang_val')

            get_device = UserDevices.objects.get(device_type=get_device_type, hash=
            gen_hash)
            if int(get_sms) == int(get_device.sms):
                gen_auth_key = generate_device_token(request)
                get_device.is_activate = True
                get_device.auth_token = gen_auth_key
                get_device.save()

                response = {'status': 200,
                            'data': {'auth': gen_auth_key}, 'languages': list(get_available_lang)}
                save_req = save_user_request(url='auth/code/confirm', req=get_request, res=response,req_headers=request.headers)
                response['req_id'] = save_req

                return JsonResponse(data=response)



            else:
                response = {"error_title": 'sms', 'error_description': 'sms_code not valid',
                            'languages': list(get_available_lang)}
                save_req = save_user_request(url='auth/code/confirm', req=get_request, res=response,req_headers=request.headers)
                response['req_id'] = save_req
                return JsonResponse(data=response)

        except Exception as e:
            return JsonResponse(data={"error_title": 'Exception', "error_description": str(e)})
    else:
        return JsonResponse(data={"error_title": 'request metod', "error_description": 'Incorrect'})


@csrf_exempt
def user_profile(request):
    get_request = None
    response = {}
    sock_settings = socket_settings()
    auth = check_user_auth(auth=request.headers.get('auth'))
    if request.method == 'POST' and auth.get('result'):
        try:
            get_request = json.loads(request.body)


            if get_request.get('is_user'):
                profile = User().get_or_create_profile(request)
                if profile.get('data'):
                    chek_follow = Follow().check_active_follow(profile.get('data').get('user_id'))


                    if chek_follow.get('status'):
                        profile['active_follow'] = chek_follow.get('follow')

                # print('profile',profile)
                profile['socket'] = sock_settings.get('socket')


                return JsonResponse(data=profile)

            else:

                profile = UserTrener().get_or_create_profile(request)
                # print('profile1', profile)
                profile['socket'] = sock_settings.get('socket')

                return JsonResponse(data=profile)


        except Exception as e:
            get_device_type = request.headers.get('device')
            get_auth_key = request.headers.get('auth')
            get_device = UserDevices.objects.get(device_type=get_device_type, auth_token=get_auth_key)

            try:
                get_user = User.objects.get(phone_number=get_device.phone_number)
                get_user_week_stat = Statistics().get_stat_by_day(request, get_request={}, user_id=get_user.id,
                                                                  order_by='week')
                print('wssss', get_user_week_stat)
                chek_follow = Follow().check_active_follow(get_user.pk)
                print(11111, chek_follow)

                if get_user.trener_id:

                    response = {'status': 200, "message": "user_profile",
                                'data': {'is_user':True,'user_id': get_user.pk, 'name': get_user.name, 'age': get_user.age,
                                         'phone': get_user.phone_number, 'img': get_user.avatar, 'normativ_from_trainer':get_user.normativ_from_trainer,
                                         'sex': get_user.sex, 'weight': get_user.weight, 'growth': get_user.growth,
                                         'date_of_birth': get_user.date_of_birth, "trener_id": get_user.trener_id}}
                    response['statistics'] = get_user_week_stat.get('statistics')
                    response['socket'] = sock_settings.get('socket')
                    if chek_follow.get('status'):
                        response['active_follow'] = chek_follow
                else:
                    response = {'status': 200, "message": "user_profile",
                                'data': {'is_user':True,'user_id': get_user.pk, 'name': get_user.name, 'age': get_user.age,
                                         'phone': get_user.phone_number, 'img': get_user.avatar,'normativ_from_trainer':get_user.normativ_from_trainer,
                                         'sex': get_user.sex, 'weight': get_user.weight, 'growth': get_user.growth,
                                         'date_of_birth': get_user.date_of_birth, "trener_id": None}}
                    response['statistics'] = get_user_week_stat.get('statistics')
                    response['socket'] = sock_settings.get('socket')
                    if chek_follow.get('status'):
                        response['active_follow'] = chek_follow



            except User.DoesNotExist:
                print('DoesNotExist')

                try:
                    get_trener = UserTrener.objects.get(phone_number=get_device.phone_number)
                    trener_follows = Follow().get_all_active_trener_follows(trener_id=get_trener.pk)


                    # trener_follows = Follow.objects.filter(
                    #     Q(is_trial=True, is_active=False, trener_id=get_trener.pk)) | Follow.objects.filter(
                    #     Q(is_trial=False, is_active=True, trener_id=get_trener.pk)) | Follow.objects.filter(
                    #     Q(is_trial=True, is_active=True, trener_id=get_trener.pk))

                    if trener_follows:
                        trener_users = User.objects.filter(trener_id=get_trener.pk).values()

                        print('ddddf', trener_follows.get('follow_filter'))

                        response = {'status': 200, "message": "trener_profile",
                                    'data': {'is_user':False,'trener_id': get_trener.pk, 'name': get_trener.name, 'age': get_trener.age,
                                             'phone': get_trener.phone_number, 'img': get_trener.avatar,
                                             'sex': get_trener.sex, 'price': get_trener.price,'rate':get_trener.rate,
                                             'experience': get_trener.experience, 'date_of_birth': get_trener.date_of_birth,
                                             "trener_users_follows": trener_follows.get('trener_follows'), "follow_filter": trener_follows.get('follow_filter'), 'sort':trener_follows.get('sort')}}


                        response['follow'] = trener_follows.get('trener_follows')
                        response['socket'] = sock_settings.get('socket')


                        # else:
                        #     response['follow'] = None
                        #     response['socket'] = sock_settings.get('socket')
                        #     response["follow_filter"]: trener_follows.get('follow_filter')
                        #     response["sort"]: trener_follows.get('sort')


                    else:
                        trener_follows = Follow().get_all_active_trener_follows(trener_id=get_trener.pk)

                        response = {'status': 200, "message": "trener_profile",
                                    'data': {'is_user':False,'trener_id': get_trener.pk, 'name': get_trener.name, 'age': get_trener.age,
                                             'phone': get_trener.phone_number, 'img': get_trener.avatar,
                                             'sex': get_trener.sex, 'price': get_trener.price,'rate':get_trener.rate,
                                             'experience': get_trener.experience, 'date_of_birth': get_trener.date_of_birth,
                                             "trener_users_follows": None}}

                        response['follow'] = None
                        response['socket'] = sock_settings.get('socket')
                        response["follow_filter"]: trener_follows.get('follow_filter')
                        response["sort"]: trener_follows.get('sort')
                except:
                    response = {'status': 200, "message": "no_user",
                                'data': {}}


            # response = {'status': 200,
            #             'data': {}, 'error_title': 'Exception', 'error_description': str(e)}
            save_req = save_user_request(url='profile/', req=get_request, res=response, req_headers=request.headers)
            response['req_id'] = save_req
            return JsonResponse(response)

    else:
        response = {'status': 200,
                    'data': {}, 'error_title': 'Auth', 'error_description': 'auth_key not found'}
        save_req = save_user_request(url='profile/', req=get_request, res=response, req_headers=request.headers)
        response['req_id'] = save_req
        return JsonResponse(response)



@csrf_exempt
def get_treners(request):
    get_request = None
    auth = check_user_auth(auth=request.headers.get('auth'))
    if request.method == 'POST' and auth.get('result'):
        get_user = User.objects.get(userdevices__auth_token=request.headers.get('auth'))
        try:
            get_request = json.loads(request.body)
            trener_list = []

            if get_request.get('page'):
                print('1')
                trener_list = UserTrener().get_treners_list(request, user_id=get_user.id,get_request=get_request, page=get_request.get('page'),)

            if get_request.get('order_by'):
                trener_list = UserTrener().get_treners_list(request, order_by=get_request.get('order_by') ,user_id=get_user.id,get_request=get_request)

            return JsonResponse(data=trener_list)






        except Exception as e:
            trener_list = UserTrener().get_treners_list(request, user_id=get_user.id, get_request=get_request)
            print('profile1', trener_list)
            return JsonResponse(data=trener_list)




    else:
        response = {'status': 200,
                    'data': {}, 'error_title': 'Auth', 'error_description': 'auth_key not found'}
        save_req = save_user_request(url='profile/', req=get_request, res=response, req_headers=request.headers)
        response['req_id'] = save_req
        return JsonResponse(response)





@csrf_exempt
def stat(request):
    get_request = None
    auth = check_user_auth(auth=request.headers.get('auth'))
    print('auth',auth)
    print('tok',request.headers.get('auth'))
    if request.method == 'POST' and auth.get('result'):
        try:

            get_user = User.objects.get(userdevices__auth_token=request.headers.get('auth'))
        except Exception as e:
            response = {'status': 200,
                        'data': {}, 'error_title': 'Exception_get_user', 'error_description': str(e)}
            save_req = save_user_request(url='user_statistics/', req=get_request, res=response,
                                         req_headers=request.headers)
            response['req_id'] = save_req

            return JsonResponse(data=response)
        try:
            # get_user = User.objects.get(userdevices__auth_token=request.headers.get('auth'))

            get_request = json.loads(request.body)
            user_stat= []
            order_by = get_request.get('order_by')
            user_id = get_request.get('user_id')

            if order_by and not user_id:
                get_stat = Statistics().get_stat_by_day(request,get_request=get_request,user_id=get_user.pk, order_by=order_by)
                if get_stat:
                    return JsonResponse(data=get_stat)
                else:
                    response = {'status': 200,
                                'data': {}, 'error_title': 'Statistics',
                                'error_description': 'Statistics not found'}
                    save_req = save_user_request(url='user_statistics/', req=get_request, res=response,
                                                 req_headers=request.headers)
                    response['req_id'] = save_req

                    return JsonResponse(data=response)
            elif order_by and user_id:
                get_stat = Statistics().get_stat_by_day(request, get_request=get_request, user_id=user_id,
                                                        order_by=order_by)
                if get_stat:
                    return JsonResponse(data=get_stat)
                else:
                    response = {'status': 200,
                                'data': {}, 'error_title': 'Statistics',
                                'error_description': 'Statistics not found'}
                    save_req = save_user_request(url='user_statistics/', req=get_request, res=response,
                                                 req_headers=request.headers)
                    response['req_id'] = save_req

                    return JsonResponse(data=response)


            else:
                response = {'status': 200,
                            'data': {}, 'error_title': 'Invalid json parament', 'error_description': 'need order_by'}
                save_req = save_user_request(url='user_statistics/', req=get_request, res=response,
                                             req_headers=request.headers)
                response['req_id'] = save_req

                return JsonResponse(data=response)


        except Exception as e:
            response = {'status': 200,
                        'data': {}, 'error_title': 'Exception Json', 'error_description': str(e)}
            save_req = save_user_request(url='user_statistics/', req=get_request, res=response,
                                         req_headers=request.headers)
            response['req_id'] = save_req

            return JsonResponse(data=response)

    else:
        response = {'status': 200,
                    'data': {}, 'error_title': 'Auth', 'error_description': str(auth)+' or chack request body / request method'}
        save_req = save_user_request(url='user_statistics/', req=get_request, res=response, req_headers=request.headers)
        response['req_id'] = save_req
        return JsonResponse(response)



    # return JsonResponse({'stat':get_s})

@csrf_exempt
def add_stat(request):
    get_request = None
    auth = check_user_auth(auth=request.headers.get('auth'))
    print('auth',auth)
    print('tok',request.headers.get('auth'))
    if request.method == 'POST' and auth.get('result'):
        try:
            get_user = User.objects.get(userdevices__auth_token=request.headers.get('auth'))
        except Exception as e:
            response = {'status': 200,
                        'data': {}, 'error_title': 'Exception_get_user', 'error_description': str(e)}
            save_req = save_user_request(url='user_statistics/add', req=get_request, res=response,
                                         req_headers=request.headers)
            response['req_id'] = save_req

            return JsonResponse(data=response)
        try:
            get_request = json.loads(request.body)
            print('get_request',get_request)
            user_stat= []
            stat_list = get_request.get('stat_list')
            if stat_list:
                for item in stat_list:
                    statistic_model = Statistics()
                    statistic_model.user_id=get_user.pk
                    statistic_model.time_counts = item.get('time_counts')
                    statistic_model.step_counts = item.get('step_counts')
                    statistic_model.kkal = item.get('kkal')
                    statistic_model.meters_counts = item.get('meters')
                    statistic_model.created_at = item.get('created_at')
                    statistic_model.save()

                response = {'status': 200,
                            'data': {}, 'message': 'saved',
                            }
                save_req = save_user_request(url='user_statistics/add', req=get_request, res=response,
                                             req_headers=request.headers)
                response['req_id'] = save_req

                return JsonResponse(data=response)

            else:
                response = {'status': 200,
                                'data': {}, 'error_title': 'Statistics',
                                'error_description': 'Statistics add faild nedd stat_list=[]'}
                save_req = save_user_request(url='user_statistics/add', req=get_request, res=response,
                                                 req_headers=request.headers)
                response['req_id'] = save_req

                return JsonResponse(data=response)



        except Exception as e:
            response = {'status': 200,
                        'data': {}, 'error_title': 'Exception Json', 'error_description': str(e)}
            save_req = save_user_request(url='user_statistics/add', req=get_request, res=response,
                                         req_headers=request.headers)
            response['req_id'] = save_req

            return JsonResponse(data=response)

    else:
        response = {'status': 200,
                    'data': {}, 'error_title': 'Auth', 'error_description': auth}
        save_req = save_user_request(url='user_statistics/add', req=get_request, res=response, req_headers=request.headers)
        response['req_id'] = save_req
        return JsonResponse(response)











@csrf_exempt
def create_follow(request):
    get_request = None
    today = datetime.datetime.now()

    auth = check_user_auth(auth=request.headers.get('auth'))
    print('auth', auth)
    print('tok', request.headers.get('auth'))
    if request.method == 'POST' and auth.get('result'):
        try:
            get_user = User.objects.get(userdevices__auth_token=request.headers.get('auth'))
        except Exception as e:
            response = {'status': 200,
                        'data': {}, 'error_title': 'Exception_get_user', 'error_description': str(e)}
            save_req = save_user_request(url='follow/add', req=get_request, res=response,
                                         req_headers=request.headers)
            response['req_id'] = save_req

            return JsonResponse(data=response)
        try:
            get_request = json.loads(request.body)
            trener_id = get_request.get('trener_id')
            if trener_id:
                check_active_follow = Follow().check_active_follow(user_id=get_user.id)
                print('check_active_follow',check_active_follow)
                if check_active_follow.get('is_trial') and not check_active_follow.get('trial_expired'):
                        response = {'status': 200,
                                    'data': {'follow_id':check_active_follow.get('follow_id')}, 'error_title': 'Подписка', 'error_description': 'У вас уже имеется активная подписка'}
                        save_req = save_user_request(url='follow/add', req=get_request, res=response,
                                                     req_headers=request.headers)
                        response['req_id'] = save_req
                        return JsonResponse(data=response)

                elif check_active_follow.get('is_active'):
                    response = {'status': 200,
                                'data': {'follow_id': check_active_follow.get('follow_id')}, 'error_title': 'Подписка',
                                'error_description': 'У вас уже имеется активная подписка'}
                    save_req = save_user_request(url='follow/add', req=get_request, res=response,
                                                 req_headers=request.headers)
                    response['req_id'] = save_req
                    return JsonResponse(data=response)



                else:
                    get_or_create_user_follow = Follow().get_or_create_user_follow(user_id=get_user.pk, trener_id=trener_id,request=request)
                    return JsonResponse(data=get_or_create_user_follow)
        except Exception as e:
            print(e)
            response = {'status': 200,
                        'data': {}, 'error_title': 'Exception Json', 'error_description': str(e)}
            save_req = save_user_request(url='Follow/add', req=get_request, res=response,
                                         req_headers=request.headers)
            response['req_id'] = save_req

            return JsonResponse(data=response)

    else:
        response = {'status': 200,
                    'data': {}, 'error_title': 'Auth', 'error_description': auth}
        save_req = save_user_request(url='Follow/add', req=get_request, res=response,
                                     req_headers=request.headers)
        response['req_id'] = save_req
        return JsonResponse(response)


@csrf_exempt
def get_main_page(request):
    get_request = None
    get_user = None

    auth = check_user_auth(auth=request.headers.get('auth'))
    if request.method == 'POST' and auth.get('result'):
        try:
            get_user = User.objects.get(userdevices__auth_token=request.headers.get('auth'))

            get_user_week_stat = Statistics().get_stat_by_day(request, get_request={}, user_id=get_user.id,order_by='week')
            response = get_user_week_stat
            response['user'] = {'user_name':get_user.name}
            response['socket'] = {'socket_server':'94.158.54.101', 'socket_port':8099, 'type':'socketIO'}



            return JsonResponse(data=response)






        except Exception as e:
            response = {'status': 200,
                        'data': {}, 'error_title': 'Auth', 'error_description': 'auth_key not found', 'message': str(e)}
            save_req = save_user_request(url='main_page/', req=get_request, res=response, req_headers=request.headers)
            response['req_id'] = save_req
            return JsonResponse(response)




    else:
        response = {'status': 200,
                    'data': {}, 'error_title': 'Auth', 'error_description': 'auth_key not found', 'message':auth}
        save_req = save_user_request(url='main_page/', req=get_request, res=response, req_headers=request.headers)
        response['req_id'] = save_req
        return JsonResponse(response)



@csrf_exempt
def normativ_add(request):
    response = {}
    auth = check_user_auth(auth=request.headers.get('auth'))
    print('auth',auth)
    if auth.get('result'):
        try:
            get_request =  json.loads(request.body)
            if get_request.get('user_id') and get_request.get('normativ'):
                set_normativ = User().add_normativ(user_id=get_request.get('user_id'), normativ=get_request.get('normativ'))
                print('set_normativ',set_normativ)
                if set_normativ.get('status'):
                    response = {'status': 200,
                                'data': {'result':True, 'normativ':set_normativ.get('normativ')},
                                'message': 'add normativ to user'}
                    save_req = save_user_request(url='normativ/add/', req=get_request, res=response,
                                                 req_headers=request.headers)
                    response['req_id'] = save_req

                else:
                    response = {'status': 200,
                                'data': {}, 'error_title': 'Auth', 'error_description': 'auth_key not found',
                                'message': ''}
                    save_req = save_user_request(url='normativ/add', req=get_request, res=response,
                                                 req_headers=request.headers)
                    response['req_id'] = save_req


                # return JsonResponse(data=response)

            else:
                response = {'status': 200,
                            'data': {}, 'error_title': 'Fields', 'error_description': 'need user_id and normativ fields',
                            'message': ''}
                save_req = save_user_request(url='normativ/add', req=get_request, res=response,
                                             req_headers=request.headers)
                response['req_id'] = save_req

        except Exception as e:
            return JsonResponse(data={"error":str(e)})
    else:
        response = {'status': 200,
                    'data': {}, 'error_title': 'Auth', 'error_description': 'auth_key not found', 'message': auth}
        save_req = save_user_request(url='normativ/add', req='', res=response, req_headers=request.headers)
        response['req_id'] = save_req
        # return JsonResponse(response)

    return JsonResponse(data=response)

@csrf_exempt
def rate_trener(request):
    response = {}
    auth = check_user_auth(auth=request.headers.get('auth'))
    print('auth', auth)
    if auth.get('result'):
        try:
            get_request = json.loads(request.body)
            get_user = User.objects.get(userdevices__auth_token=request.headers.get('auth'))
            check_user_rate = TrenerRate.objects.filter(user_id=get_user.pk,trener_id=get_request.get('trener_id'))
            print('check_user_rate', check_user_rate)

            if get_request.get('trener_id') and get_request.get('rate') and not check_user_rate:
                response = UserTrener().rate_trener(request,rate=get_request.get('rate'), trener_id=get_request.get('trener_id'),user_id=get_user.pk)
                save_req = save_user_request(url='trener_rate/', req=get_request, res=response,
                                             req_headers=request.headers)
                response['req_id'] = save_req

            elif get_request.get('trener_id') and get_request.get('rate') and check_user_rate:
                response = {'status': 200,
                            'data': {}, 'error_title': 'Rate',
                            'error_description': 'Вы ранее оценивали тренера',
                            'message': ''}
                save_req = save_user_request(url='trener_rate/', req=get_request, res=response,
                                             req_headers=request.headers)
                response['req_id'] = save_req


            else:
                response = {'status': 200,
                            'data': {}, 'error_title': 'Fields',
                            'error_description': 'need trener_id and rate fields',
                            'message': ''}
                save_req = save_user_request(url='trener_rate/', req=get_request, res=response,
                                             req_headers=request.headers)
                response['req_id'] = save_req

        except Exception as e:
            return JsonResponse(data={"error": str(e)})
    else:
        response = {'status': 200,
                    'data': {}, 'error_title': 'Auth', 'error_description': 'auth_key not found', 'message': auth}
        save_req = save_user_request(url='trener_rate', req='', res=response, req_headers=request.headers)
        response['req_id'] = save_req
        # return JsonResponse(response)

    return JsonResponse(data=response)





@csrf_exempt
def activate_follow(request):
    auth = check_user_auth(auth=request.headers.get('auth'))
    if auth.get('result'):
        try:
            get_request =  json.loads(request.body)
            if get_request.get('is_trial') and get_request.get('follow_id'):
                follow = Follow().activate_follow(follow_id=get_request.get('follow_id'), request=request, is_trial=True)
                print(follow)
                return JsonResponse(data=follow)
            elif get_request.get('follow_id') and get_request.get('period_id'):
                follow = Follow().activate_follow(follow_id=get_request.get('follow_id'), request=request, is_trial=False, period=get_request.get('period_id'))

                return JsonResponse(data=follow)

        except Exception as e:
            return JsonResponse(data={"error":str(e)})
    else:
        return JsonResponse(data={"error_title": "Auth", "error_description":"Auth faild"})


@csrf_exempt

def filter_follow(request):
    try:
        get_request =  json.loads(request.body)
        get_trener = UserTrener.objects.get(userdevices__auth_token=request.headers.get('auth'))
        print('k')

        if get_request.get('is_plan') and not  get_request.get('day_left') and not get_request.get('order_by'):
            follows = Follow().sort_follows(request, trener_id=get_trener.pk,is_plan=True, three_days_left=None )
            # print(follows)
            return JsonResponse(data=follows)
        elif get_request.get('is_plan') and get_request.get('day_left')and not get_request.get('order_by'):
            print('lll')
            follows = Follow().sort_follows(request, trener_id=get_trener.pk, is_plan=True, three_days_left=True)
            print(follows)
            return JsonResponse(data=follows)
        elif get_request.get('is_plan') and get_request.get('day_left') and get_request.get('order_by'):

            follows = Follow().sort_follows(request, trener_id=get_trener.pk, is_plan=True, three_days_left=True, order_by=get_request.get('order_by'))
            # print(follows)
            return JsonResponse(data=follows)

        elif get_request.get('is_plan') and not get_request.get('day_left') and get_request.get('order_by'):
            follows = Follow().sort_follows(request, trener_id=get_trener.pk, is_plan=True, three_days_left=False, order_by=get_request.get('order_by'))
            # print(follows)
            return JsonResponse(data=follows)

        elif not get_request.get('is_plan') and not get_request.get('day_left') and get_request.get('order_by'):
            follows = Follow().sort_follows(request, trener_id=get_trener.pk, is_plan=False, three_days_left=False, order_by=get_request.get('order_by'))
            # print(follows)
            return JsonResponse(data=follows)

        elif not  get_request.get('is_plan') and  get_request.get('day_left') and not get_request.get('order_by'):
            follows = Follow().sort_follows(request, trener_id=get_trener.pk, is_plan=False, three_days_left=True, order_by=get_request.get('order_by'))
            # print(follows)
            return JsonResponse(data=follows)

    except Exception as e:
        print(e)
        # print(e)
        return JsonResponse(data={"error":str(e)})



@csrf_exempt
def get_all_chats(request):
    auth = check_user_auth(auth=request.headers.get('auth'))
    response = None
    if auth.get('result'):
        users_chat = {}
        try:
            get_user = UserDevices.objects.get(auth_token=request.headers.get('auth'))
            print('get_user',get_user.user_id)
            if get_user.user_id:
                chek_follow = Follow().check_active_follow(user_id=get_user.user_id)
                if chek_follow.get('status'):
                    print('2')
                    print(chek_follow.get('status'),)
                    users_chat = ChatMessages().get_active_chat(user_id=get_user.user_id)
                    print('users_chat',users_chat)
                else:
                    print('NOOTOT')
                    users_chat = []

            if get_user.trener_id:
                users_chat = ChatMessages().get_active_chat(trener_id=get_user.trener_id)

            if users_chat:
                for message in users_chat.get('chat_list'):
                    get_message_last = ChatMessages().get_last_massage(chat_id=message.get('id'))
                    if get_message_last:
                        message['last_message'] = get_message_last.get('last_message')
                        if get_user.user_id and get_user.user_id == message.get('user_id') and not get_user.trener_id:
                            get_message_last.get('last_message')['is_my_message'] = True
                        elif get_user.trener_id and get_user.trener_id == message.get('trener_id') and not get_user.user_id:
                            get_message_last.get('last_message')['is_my_message'] = True
                        else:
                            get_message_last.get('last_message')['is_my_message'] = False
                response = {'active_chat':users_chat.get('chat_list')}
            else:
                response = {'active_chat': []}

            save_req = save_user_request(url='get_all_chats', req='', res=response, req_headers=request.headers)
            response['req_id'] = save_req
            return JsonResponse(response)


        except Exception as e :
            print(e)

            response = {'error_title':"Device",'error_description':str(e)}
            return JsonResponse(data=response)


@csrf_exempt
def mark_message_as_read(request):
    auth = check_user_auth(auth=request.headers.get('auth'))
    response = None
    print(auth.get('result'))
    if auth.get('result'):
        users_chat = {}
        try:
            get_request = json.loads(request.body)
            print('get_request',get_request)
            if get_request.get('message_id'):
                print('2')
                mark_message = ChatMessages().mark_messages_as_read(message_list_id=get_request.get('message_id'))
                print('mark_message',mark_message)
                response = {'messages':mark_message.get('marked_messages'), 'is_read':True}
            else:
                response = {'error_title':'Invalid field', 'error_description':'need list of message_id'}


            save_req = save_user_request(url='mark_messages_ad_read', req=get_request, res=response, req_headers=request.headers)
            response['req_id'] = save_req
            return JsonResponse(response)


        except Exception as e :
            print(e)

            response = {'error_title':"Device",'error_description':str(e)}
            return JsonResponse(data=response)

    else:
        response = {'error_title': "Auth", 'error_description': 'Auth Failed'}
        return JsonResponse(data=response)


@csrf_exempt
def push_notifications_add_token(request):
    auth = check_user_auth(auth=request.headers.get('auth'))
    response = None
    print(auth.get('result'))
    if auth.get('result'):

        try:
            get_request = json.loads(request.body)
            if get_request.get('push_token'):
                get_device = UserDevices.objects.get(auth_token=request.headers.get('auth'))
                get_device.push_token = get_request.get('push_token')
                get_device.save()
                response = {'save':True, 'status':True, 'push_token':get_device.push_token}
                save_req = save_user_request(url='add push token', req=get_request, res=response,
                                             req_headers=request.headers)
                response['req_id'] = save_req
                return JsonResponse(response)
            else:
                response = {'error_title': "params", 'error_description': 'need field push_token'}
                return JsonResponse(response)

        except:
            response = {'error_title': "Json", 'error_description': 'Json decode error'}
            return JsonResponse(data=response)
    else:
        response = {'error_title': "Auth", 'error_description': 'Auth Failed'}
        return JsonResponse(data=response)

@csrf_exempt
def check_payment_upay(request):
    import hashlib
    response = {}
    now = datetime.datetime.now()
    today = datetime.datetime.now()
    days_count_in_month = 0

    try:
        get_request =  json.loads(request.body)
        period = get_request.get('period')
        mystring = str(get_request.get('upayTransId')) +str(get_request.get('upayPaymentAmount')) +str(get_request.get('personalAccount'))
        accesstokenmd5 = hashlib.md5(mystring.encode())
        print(accesstokenmd5.hexdigest())
        if get_request.get('upayTransId') and get_request.get('upayTransTime') and get_request.get('period') and get_request.get('upayPaymentAmount')\
                and get_request.get('personalAccount') and get_request.get('accessToken') == accesstokenmd5.hexdigest():

            get_follow = Follow.objects.get(pk=int(get_request.get('personalAccount')))
            if period == '1':
                days_count_in_month = calendar.monthrange(now.year, now.month)[1]
            elif period == '2':
                cur_month = calendar.monthrange(now.year, now.month)[1]
                days_count_in_month = calendar.monthrange(now.year, now.month + 1)[1] + cur_month
            elif period == '3':
                cur_month = calendar.monthrange(now.year, now.month)[1]
                cur_next_month = calendar.monthrange(now.year, now.month + 1)[1] + cur_month
                days_count_in_month = calendar.monthrange(now.year, now.month + 2)[1] + cur_next_month

            else:
                days_count_in_month = calendar.monthrange(now.year, now.month)[1]

            if get_follow.is_active:
                till = datetime.timedelta(days=days_count_in_month)
                get_follow.follow_period_end += (days_count_in_month * 86400)
                get_follow.payment_type = 'Upay'
                get_follow.total_price = int(get_request.get('upayPaymentAmount'))
                get_follow.is_trial = False
                get_follow.save()
                response = {"status": 1, 'message': 'Успешно'}
                save_req = save_user_request(url='check_payment/', req=get_request, res=response,
                                             req_headers=request.headers)
                response['req_id'] = save_req
                try:
                    get_trener = get_follow.trener.name
                    get_trener_avatar = get_follow.trener.avatar
                    get_devices = UserDevices.objects.filter(user_id=get_follow.user.id).values(
                        'push_token', 'device_type')

                    if get_trener_avatar:

                        push_service = SentPush().send_push(message_title='Вы успешно продлили подписку', message_body='Ваш тренер ' + str(get_trener.title()), userdevices=get_devices, icon_url=get_trener_avatar)
                    else:
                        push_service = SentPush().send_push(message_title='Вы успешно продлили подписку',
                                                            message_body='Ваш тренер ' + str(get_trener.title()),
                                                            userdevices=get_devices)

                except:
                    pass

                return JsonResponse(response)

            if get_follow.is_trial and not get_follow.is_active:
                till = datetime.timedelta(days=days_count_in_month)
                get_follow.follow_period_start = now.timestamp()
                get_follow.follow_period_end = now.timestamp() + (days_count_in_month * 86400)
                get_follow.payment_type = 'Upay'
                get_follow.is_active = True
                get_follow.trial_expired = True
                get_follow.is_trial = False
                get_follow.save()
                response = {"status": 1, 'message': 'Успешно'}
                save_req = save_user_request(url='check_payment/', req=get_request, res=response,
                                             req_headers=request.headers)
                try:
                    get_trener = get_follow.trener.name
                    get_trener_avatar = get_follow.trener.avatar
                    get_devices = UserDevices.objects.filter(user_id=get_follow.user.id).values(
                        'push_token', 'device_type')

                    if get_trener_avatar:

                        push_service = SentPush().send_push(message_title='Вы успешно активировали подписку', message_body='Ваш тренер ' + str(get_trener.title()), userdevices=get_devices, icon_url=get_trener_avatar)
                    else:
                        push_service = SentPush().send_push(message_title='Вы успешно активировали подписку',
                                                            message_body='Ваш тренер ' + str(get_trener.title()),
                                                            userdevices=get_devices)

                except:
                    pass

                response['req_id'] = save_req
                return JsonResponse(response)

            if not get_follow.is_trial and not get_follow.is_active:
                get_follow.follow_period_start = now.timestamp()
                get_follow.follow_period_end = now.timestamp() + (days_count_in_month * 86400)
                get_follow.payment_type = 'Upay'
                get_follow.is_active = True
                get_follow.trial_expired = True
                get_follow.is_trial = False
                get_follow.save()
                # create_chat = Chat.objects.get_or_create(user_trener_id=get_follow.trener_id, user_id=get_follow.user_id)
                get_chat, create_chat = Chat.objects.get_or_create(user_trener_id=get_follow.trener_id,
                                                                   user_id=get_follow.user_id)

                try:
                    get_devices = UserDevices.objects.filter(user_id=get_follow.user.id).values(
                        'push_token', 'device_type')
                    get_trener = get_follow.trener.name
                    get_trener_avatar = get_follow.trener.avatar
                    push_service = SentPush().send_push(message_title='Вы успешно активировали подписку',
                                                        message_body='Ваш тренер ' + str(get_trener.title()),
                                                        userdevices=get_devices)

                except:
                    pass

                response = {"status": 1, 'message': 'Успешно'}
                save_req = save_user_request(url='check_payment/', req=get_request, res=response, req_headers=request.headers)
                response['req_id'] = save_req
                response['chat_id'] = get_chat.pk
                return JsonResponse(response)
        else:
            response = { "status": 2, 'message': 'Ошибка оплаты заказ не найден'}
            save_req = save_user_request(url='check_payment/', req=get_request, res=response,
                                         req_headers=request.headers)
            response['req_id'] = save_req
            return JsonResponse(response)

    except Exception as e:
        response = {"status": 3, 'message': 'Ошибка оплаты не заполнены необходимые параметры', "error": str(e)}
        save_req = save_user_request(url='check_payment/', req=None, res=response,
                                     req_headers=request.headers)
        response['req_id'] = save_req
        return JsonResponse(response)




@csrf_exempt
def check_payment_click(request):
    pass
    # import hashlib
    # response = {}
    # now = datetime.datetime.now()
    # today = datetime.datetime.now()
    # days_count_in_month = now.month
    #
    # try:
    #     get_request =  json.loads(request.body)
    #     period = get_request.get('period')
    #     mystring = str(get_request.get('upayTransId')) +str(get_request.get('upayPaymentAmount')) +str(get_request.get('personalAccount'))
    #     accesstokenmd5 = hashlib.md5(mystring.encode())
    #     if get_request.get('upayTransId') and get_request.get('upayTransTime') and get_request.get('period') and get_request.get('upayPaymentAmount')\
    #             and get_request.get('personalAccount') and get_request.get('accessToken') == accesstokenmd5.hexdigest():
    #
    #         get_follow = Follow.objects.get(pk=int(get_request.get('personalAccount')))
    #         if period == 1:
    #             days_count_in_month = calendar.monthrange(now.year, now.month)[1]
    #         elif period == 2:
    #             days_count_in_month = calendar.monthrange(now.year, now.month + 1)[1]
    #
    #         elif period == 3:
    #             days_count_in_month = calendar.monthrange(now.year, now.month + 2)[1]
    #         else:
    #             days_count_in_month = calendar.monthrange(now.year, now.month)[1]
    #
    #         # get_follow.is_active = True
    #         if get_follow.is_active:
    #
    #             till = datetime.timedelta(days=days_count_in_month)
    #
    #             get_follow.follow_period_end = till
    #             get_follow.save()
    #             response = {"status": 1, 'message': 'Успешно'}
    #
    #         if get_follow.is_trial:
    #             till = datetime.timedelta(days=days_count_in_month)
    #             get_follow.follow_period_start = now.timestamp()
    #             get_follow.follow_period_end = till
    #             get_follow.is_active = True
    #             get_follow.save()
    #             response = {"status": 1, 'message': 'Успешно'}
    #         save_req = save_user_request(url='check_payment/', req=get_request, res=response, req_headers=request.headers)
    #         response['req_id'] = save_req
    #         return JsonResponse(response)
    #     else:
    #         response = { "status": 2, 'message': 'Ошибка оплаты заказ не найден'}
    #         save_req = save_user_request(url='check_payment/', req=get_request, res=response,
    #                                      req_headers=request.headers)
    #         response['req_id'] = save_req
    #         return JsonResponse(response)
    #
    # except Exception as e:
    #     response = {"status": 3, 'message': 'Ошибка оплаты не заполнены необходимые параметры', "error": str(e)}
    #     save_req = save_user_request(url='check_payment/', req=None, res=response,
    #                                  req_headers=request.headers)
    #     response['req_id'] = save_req
    #     return JsonResponse(response)


@csrf_exempt
def check_payment_payme(request):
    pass
    # import hashlib
    # response = {}
    # now = datetime.datetime.now()
    # today = datetime.datetime.now()
    # days_count_in_month = now.month
    #
    # try:
    #     get_request =  json.loads(request.body)
    #     period = get_request.get('period')
    #     mystring = str(get_request.get('upayTransId')) +str(get_request.get('upayPaymentAmount')) +str(get_request.get('personalAccount'))
    #     accesstokenmd5 = hashlib.md5(mystring.encode())
    #     if get_request.get('upayTransId') and get_request.get('upayTransTime') and get_request.get('period') and get_request.get('upayPaymentAmount')\
    #             and get_request.get('personalAccount') and get_request.get('accessToken') == accesstokenmd5.hexdigest():
    #
    #         get_follow = Follow.objects.get(pk=int(get_request.get('personalAccount')))
    #         if period == 1:
    #             days_count_in_month = calendar.monthrange(now.year, now.month)[1]
    #         elif period == 2:
    #             days_count_in_month = calendar.monthrange(now.year, now.month + 1)[1]
    #
    #         elif period == 3:
    #             days_count_in_month = calendar.monthrange(now.year, now.month + 2)[1]
    #         else:
    #             days_count_in_month = calendar.monthrange(now.year, now.month)[1]
    #
    #         # get_follow.is_active = True
    #         if get_follow.is_active:
    #
    #             till = datetime.timedelta(days=days_count_in_month)
    #
    #             get_follow.follow_period_end = till
    #             get_follow.save()
    #             response = {"status": 1, 'message': 'Успешно'}
    #
    #         if get_follow.is_trial:
    #             till = datetime.timedelta(days=days_count_in_month)
    #             get_follow.follow_period_start = now.timestamp()
    #             get_follow.follow_period_end = till
    #             get_follow.is_active = True
    #             get_follow.save()
    #             response = {"status": 1, 'message': 'Успешно'}
    #         save_req = save_user_request(url='check_payment/', req=get_request, res=response, req_headers=request.headers)
    #         response['req_id'] = save_req
    #         return JsonResponse(response)
    #     else:
    #         response = { "status": 2, 'message': 'Ошибка оплаты заказ не найден'}
    #         save_req = save_user_request(url='check_payment/', req=get_request, res=response,
    #                                      req_headers=request.headers)
    #         response['req_id'] = save_req
    #         return JsonResponse(response)
    #
    # except Exception as e:
    #     response = {"status": 3, 'message': 'Ошибка оплаты не заполнены необходимые параметры', "error": str(e)}
    #     save_req = save_user_request(url='check_payment/', req=None, res=response,
    #                                  req_headers=request.headers)
    #     response['req_id'] = save_req
    #     return JsonResponse(response)


