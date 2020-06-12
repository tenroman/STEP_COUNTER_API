import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "STEP_COUNTER_API.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from STEP_COUNTER_API_APP.views import check_user_auth
from aiohttp import web
import socketio
import json
import requests

HOST = "94.158.54.101"
PORT = 7000

# creates a new Async Socket IO Server
sio = socketio.AsyncServer(cors_allowed_origins='*')
# Creates a new Aiohttp Web Application
app = web.Application()
# Binds our Socket.IO server to our Web App
# instance
sio.attach(app)

from STEP_COUNTER_API_APP.models import Chat


def check_access_from_firdaus_API(auth_key):
    user_has_access = requests.request(method='POST', url='http://player.spg.uz/api/mic/user',
                                       json={"auth_token": auth_key})

    return user_has_access.json()


@sio.event
async def begin_chat(sid, message=None, chat_id=None, chat_user_info=None, envirion=None):
    if not chat_id:
        create_chat = Chat.objects.create()
        sio.enter_room(sid, str(create_chat.id))
        user_status = {'id':1, 'is_user':True, 'status':"online"}
        await sio.emit('message', user_status)
    else:
        sio.enter_room(sid, str(chat_id))
        user_status = {'id': 1, 'is_user': True, 'status': "online"}
        await sio.emit('message', user_status)


@sio.event
async def exit_chat(sid, chat_):

    get_user_from_session = await sio.get_session(sid)
    sio.leave_room(sid, str(get_user_from_session.get('watch_room_id')))
    user_message = {'chat': {'watch_room_id': str(get_user_from_session.get('watch_room_id')), 'message': str(
        get_user_from_session.get('user_name') + ' покинул комнату № ' + str(
            get_user_from_session.get('watch_room_id'))), 'user_name': str(get_user_from_session.get('user_name'))}, }
    await sio.emit('message', user_message, room=str(get_user_from_session.get('watch_room_id')))



@sio.event
async def connect(sid, environ):
    print('environ',environ)

    chek_access = check_user_auth(auth=environ.get('HTTP_AUTH_KEY'))
    print('chek_access',chek_access)

    if chek_access.get('result'):
        await begin_chat(sid)
        print('chat_startes')

    else:

        await sio.emit('message', {"error":"no access"})

@sio.event
async def disconnect(sid):
    users_count = 0
    get_user_from_session = await sio.get_session(sid)
    for i in sio.environ.items():
        print('i=', i)
        if i[1].get('HTTP_WATCH_ROOM_ID') == get_user_from_session.get('watch_room_id'):
            users_count = get_user_from_session.get('users_count')
            print('users_count discon', users_count)
            print('get_user_from_session.get',get_user_from_session.get('users_count'))
            if users_count ==1:
                users_count = get_user_from_session.get('users_count')
            else:
                users_count -=1


    user_message = {'chat': {'watch_room_id': str(get_user_from_session.get('watch_room_id')), 'message': str(
        get_user_from_session.get('user_name') + ' отключился от ' + str(
            get_user_from_session.get('watch_room_id'))), 'user_name': str(get_user_from_session.get('user_name')),
                             'users_count': users_count}, }
    await sio.emit('message', user_message, room=str(get_user_from_session.get('watch_room_id')))




@sio.event

async def message(sid, data):
    print('data=', data)
    message_json = ''
    try:
        message_json = json.loads(str(data))
        get_user_from_session = await sio.get_session(sid)
        print('get_user_from_session',get_user_from_session)



        if message_json.get('type') == 'chat':
            message_from_user = str(message_json.get("message"))
            user_message = {
                'chat': {'watch_room_id': str(get_user_from_session.get('watch_room_id')), 'message': message_from_user,
                         'user_name': get_user_from_session.get('user_name')}}

            try:
                save_message = MysqlDB().save_user_messages(user_id=get_user_from_session.get('user_id'),watchroom_id=str(get_user_from_session.get('watch_room_id')),content={"message":message_json.get("message"), "user_name":get_user_from_session.get('user_name')})
                print('save_message', 'saved')
                await sio.emit('message', user_message, room=str(get_user_from_session.get('watch_room_id')))
            except Exception as e:
                print(e)
                await sio.emit('message', user_message, room=str(get_user_from_session.get('watch_room_id')))




        elif message_json.get('type') == 'action' and str(message_json.get('message')).lower() == 'start':


            user_message = {'action':{'watch_room_id':str(get_user_from_session.get('watch_room_id')), 'message':str(get_user_from_session.get('user_name')) + ': начал просмотр'}}
            await sio.emit('message', user_message, room=str(get_user_from_session.get('watch_room_id')))

        elif message_json.get('type') == 'action' and str(message_json.get('message')).lower() == 'stop':

            user_message = {'action': {'watch_room_id': str(get_user_from_session.get('watch_room_id')), 'message': str(
            get_user_from_session.get('user_name')) + ': остановил просмотр'}}
            await sio.emit('message', user_message, room=str(get_user_from_session.get('watch_room_id')))

        elif message_json.get('type') == 'action' and str(message_json.get('message')).lower() == 'pause':

            user_message = {'action': {'watch_room_id': str(get_user_from_session.get('watch_room_id')), 'message': str(
                get_user_from_session.get('user_name')) + ': приостановил просмотр'}}
            await sio.emit('message', user_message, room=str(get_user_from_session.get('watch_room_id')))

        elif message_json.get('type') == 'action' and str(message_json.get('message')).lower() == 'rewind_down' and message_json.get('time'):

            user_message = {'action': {'watch_room_id': str(get_user_from_session.get('watch_room_id')), 'message': str(
            get_user_from_session.get('user_name')) + ': перемотал просмотр назад'}, 'time':message_json.get('time')}
            await sio.emit('message', user_message, room=str(get_user_from_session.get('watch_room_id')))

        elif message_json.get('type') == 'action' and str(message_json.get('message')).lower() == 'rewind_up' and message_json.get('time'):

            user_message = {'action': {'watch_room_id': str(get_user_from_session.get('watch_room_id')), 'message': str(
            get_user_from_session.get('user_name')) + ': перемотал просмотр вперед'}, 'time':message_json.get('time')}
            await sio.emit('message', user_message, room=str(get_user_from_session.get('watch_room_id')))



        else:
            await sio.emit('message', "incorrect message type", room=str(get_user_from_session.get('watch_room_id')))



    except json.JSONDecodeError:
        pass


    # print('awited')

# We bind our aiohttp endpoint to our app
# router
app.router.add_get('/', index)

# We kick off our server
if __name__ == '__main__':
    web.run_app(app, host=HOST, port=PORT)