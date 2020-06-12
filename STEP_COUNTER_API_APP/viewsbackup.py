from django.shortcuts import render
import random
from STEP_COUNTER_API_APP.models import User, UserDevices, UserTrener, Saverequest, Languages, Translates, Page
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib
import uuid
import datetime


# Create your views here.

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


"""generate sms number"""


def check_user_auth(auth):
    try:
        check_auth = UserDevices.objects.get(auth_token=auth)
        if check_auth:
            return {'result': True}

    except Exception as e:
        return {'result': False, 'error': str(e)}


"""registraion new user device"""


@csrf_exempt
def get_available_languages(request):
    """EMPTY POST REQUST"""
    if request.method == 'POST':
        get_langs = Languages.objects.all().values('header_key', 'lang_val', 'url', 'header_value')
        get_translate = Translates.objects.filter(page__page_name='language').values()
        if get_translate:
            response = {'status': 200, 'req_id': '', 'languages': list(get_langs)}
        else:
            response = {'status': 200, 'req_id': '', 'languages': list(get_langs)}

        save_req = save_user_request(url='/api/available_langs/', req='empty', res=response,
                                     req_headers=request.headers)
        response['req_id'] = save_req
        return JsonResponse(data=response)


    else:
        return JsonResponse(data={"error_title": 'request metod', "error_description": 'Incorrect'})


@csrf_exempt
def page_translate(request):
    """EMPTY POST REQUST"""
    ta = {}
    if request.method == 'POST':
        get_page_by_name = Page.objects.all()
        for page in get_page_by_name:
            response = []
            translates = Translates.objects.filter(page_id=page.id).values()
            for translate in translates:
                response.append(
                    {translate.get('name_key'): {'rus': translate.get('name_ru'), 'uz': translate.get('name_uz')}})
                ta[page.page_name] = response


        return JsonResponse(data=ta)



        # print('111translate', ta)







    # try:
    #     get_request = json.loads(request.body)
    #     get_page = get_request.get('page')
    #     get_page_by_name = Page.objects.get(page_name=get_page)
    #     print('get_page_by_name',get_page_by_name)
    #     translate = Translates.objects.filter(page_id=get_page_by_name.id).values('name_ru', 'name_key', 'name_uz', 'list_sex')
    #     if request.headers.get('lang') == 'rus':
    #         for trans in translate:
    #             translate_dic[trans['name_key']]= trans['name_ru']
    #             if trans['name_key'] == 'sex':
    #                 print(2)
    #                 translate_dic['sex'] = [{'id':1,"value":"Мужской"},{"id":2, "value":'Женский'}]
    #
    #             print('trans',trans)
    #
    #
    #         response = {'status': 200, 'req_id': '', 'translate':translate_dic}
    #
    #     else:
    #         for trans in translate:
    #             translate_dic[trans['name_key']]= trans['name_uz']
    #             if trans['name_key'] == 'sex':
    #                 print(2)
    #                 translate_dic['sex'] = [{'id':3,"value":"Мужской УЗ"},{"id":4, "value":'Женский УЗ'}]
    #
    #             print('trans', trans)
    #             response = {'status': 200, 'req_id': '', 'translate': translate_dic}
    #
    #
    #     save_req = save_user_request(url='/api/translate/', req=get_request, res=response,
    #                                  req_headers=request.headers)
    #     response['req_id'] = save_req
    #     return JsonResponse(data=response)
    #
    # except Exception as e:
    #     return JsonResponse(data={"error_title": 'Exception', "error_description": str(e)})

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
            hash = (str(get_device_token) + str(timestamp)).encode()
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
                update_device.save()
                response = {'status': 200, 'sms_status': 'sended', 'sms_resend_time': update_device.time_to_resend_sms,
                            'data': {'device_id': get_device.pk, 'hash': gen_hash, 'new_device': True},
                            'languages': list(get_available_lang)}

                save_req = save_user_request(url='/api/auth/code/', req=get_request, res=response,
                                             req_headers=request.headers)
                response['req_id'] = save_req
                return JsonResponse(data=response)
            else:
                update_device = UserDevices.objects.get(pk=get_device.pk)
                update_device.hash = gen_hash
                update_device.phone_number = get_phone
                gen_sms_code = sms(phone_number=get_phone)
                update_device.sms = gen_sms_code
                update_device.save()
                response = {'status': 200, 'req_id': '', 'sms_status': 're_sended',
                            'sms_resend_time': get_device.time_to_resend_sms,
                            'data': {'device_id': get_device.pk, 'hash': gen_hash, "new_device": False},
                            'languages': list(get_available_lang)}

                save_req = save_user_request(url='/api/auth/code/', req=get_request, res=response,
                                             req_headers=request.headers)
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
                save_req = save_user_request(url='auth/code/confirm', req=get_request, res=response,
                                             req_headers=request.headers)
                response['req_id'] = save_req

                return JsonResponse(data=response)



            else:
                response = {"error_title": 'sms', 'error_description': 'sms_code not valid',
                            'languages': list(get_available_lang)}
                save_req = save_user_request(url='auth/code/confirm', req=get_request, res=response,
                                             req_headers=request.headers)
                response['req_id'] = save_req
                return JsonResponse(data=response)

        except Exception as e:
            return JsonResponse(data={"error_title": 'Exception', "error_description": str(e)})
    else:
        return JsonResponse(data={"error_title": 'request metod', "error_description": 'Incorrect'})


@csrf_exempt
def user_profile(request):
    get_request = None
    auth = check_user_auth(auth=request.headers.get('auth'))
    if request.method == 'POST' and auth.get('result'):
        try:
            get_request = json.loads(request.body)

            if get_request.get('is_user'):
                profile = User().get_or_create_profile(request)

                print('profile', profile)
                return JsonResponse(data=profile)

            else:
                profile = UserTrener().get_or_create_profile(request)
                print('profile1', profile)
                return JsonResponse(data=profile)


        except Exception as e:
            response = {'status': 200,
                        'data': {}, 'error_title': 'Exception', 'error_description': str(e)}
            save_req = save_user_request(url='profile/', req=get_request, res=response, req_headers=request.headers)
            response['req_id'] = save_req
            return JsonResponse(response)

    else:
        response = {'status': 200,
                    'data': {}, 'error_title': 'Auth', 'error_description': 'auth_key not found'}
        save_req = save_user_request(url='profile/', req=get_request, res=response, req_headers=request.headers)
        response['req_id'] = save_req
        return JsonResponse(response)


def main_page(requests):
    pass
