from pyfcm import FCMNotification



class SentPush:
    def __init__(self):
        self.api_key_ios = 'AAAAQ5KGrb0:APA91bHCFf0itNOWQ5zK0daVg-omgWME_McWJBESc3eYa2haWt5ICSztTB9cTs2BiNUNYE8HVA3rvXfnWLBaVlbORN_GHqztuh2X8PYY3n2fekdN8GW1hvgizgitSZ5IITq-fWo5ZjB6'
        self.api_key_android = 'AAAASjSfaSE:APA91bEQXd7racDFvsYh5vLYKMqL6kBYaGR4HvRmKblcJfUOVdFIpZdnTTMjMyJJL3hddGMBefP82VI_hFdjg8CE4MbWdypdyXYnh3rwcWb_edkFEW24HPHND26_GLSzuNnxWTIDWRed'
        self.push_service_ios = FCMNotification(api_key=self.api_key_ios)
        self.push_service_android = FCMNotification(api_key=self.api_key_android)

    def send_push_notification_ios(self, registration_id, message_title,message_body, icon_url=None):
        data_message = {'message_title':message_title, 'message_body':message_body,'icon_url':icon_url }
        if icon_url:

            result = self.push_service_ios.notify_multiple_devices(registration_ids=registration_id, message_title=message_title,
                                                                   message_body=message_body, message_icon=icon_url, sound='default')
            result_data = self.push_service_ios.notify_multiple_devices(registration_ids=registration_id, data_message=data_message)

        else:
            result = self.push_service_ios.notify_multiple_devices(registration_ids=registration_id,
                                                                   message_title=message_title,
                                                                   message_body=message_body, message_icon=None,sound='default')
            result_data = self.push_service_ios.notify_multiple_devices(registration_ids=registration_id, data_message=data_message)


        return {'status':True, 'result':result, 'result_data':result_data}

    def send_push_notification_android(self, registration_id, message_title,message_body, icon_url=None):
        data_message = {'message_title':message_title, 'message_body':message_body,'icon_url':icon_url }
        if icon_url:

            result = self.push_service_android.notify_multiple_devices(registration_ids=registration_id, sound='default',message_title=message_title, message_body=message_body,message_icon=icon_url)
            result_data = self.push_service_android.notify_multiple_devices(registration_ids=registration_id, data_message=data_message)

        else:
            result = self.push_service_android.notify_multiple_devices(registration_ids=registration_id,
                                                                       message_title=message_title,sound='default',
                                                                       message_body=message_body, message_icon=None)
            result_data = self.push_service_android.notify_multiple_devices(registration_ids=registration_id, data_message=data_message)


        return {'status':True, 'result':result, 'result_data':result_data}



    def send_push(self,message_title, message_body, userdevices, icon_url=None,):
        ios_list = []
        android_list = []
        result = ''
        result_and = ''
        if userdevices:
            for push_token in userdevices:
                if push_token.get('device_type') == 'ios' and push_token.get('push_token'):
                    ios_list.append(push_token.get('push_token'))
                if push_token.get('device_type') == 'android' and push_token.get('push_token'):
                    android_list.append(push_token.get('push_token'))

            if ios_list:
                if icon_url:
                    result = self.send_push_notification_ios(registration_id=ios_list, message_title=message_title, message_body=message_body, icon_url=icon_url)


                else:
                    result = self.send_push_notification_ios(registration_id=ios_list, message_title=message_title, message_body=message_body)

            if android_list:
                if icon_url:
                    result_and = self.send_push_notification_android(registration_id=android_list, message_title=message_title, message_body=message_body)
                else:
                    result_and = self.send_push_notification_android(registration_id=android_list, message_title=message_title, message_body=message_body,icon_url=icon_url)


            return {"status":True, 'android':str(result_and), 'ios':str(result)}
        else:
            return False


#
# #
# # # #
# # # # #
# clients = ['eqlRSdQgTT21bVgOX6_fqJ:APA91bGj7LVQoiIPDpS7MW9H8Dz8rwDOrXsc1owdrBpRcPIM8TlTascsNlVfIcDCOzF8HQR1nePMSj5fx43NgBeigi-Cp446tZteolJfyFX5fCkzs17HioGHVeWHX4DOixenRa5Zy7OD',]
# aaa = SentPush().send_push_notification_ios(registration_id=clients,
#                                          message_title='ТЕСТ', message_body='666666')
# # # #
# # #
# andr_cl = ['etm4OQkNTs2Fs6H2gRJGEP:APA91bFoNu9JFrk2ekXrU4ks3KgJ62kb92PLQkXFUVn4wtZcJ93SWlAah57b9DXCzr2IFHg6ogO25OSN18XFPgdPnCxP-PcsYx6kj9-6JIdBxsKdam8mWT4-zXB72wss4AKkzD3Duxk2']
# aaba = SentPush().send_push_notification_android(registration_id=clients,
#                                          message_title='ТЕСТ', message_body='666666')
# # # # #
# # # # # #
# print(aaa)
# # # # # #
# print(aaba)
# # # # # #
# # # #
