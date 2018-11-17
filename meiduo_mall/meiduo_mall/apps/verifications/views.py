import random

from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView

from celery_tasks.sms.tasks import send_sms_code

# url('^sms_codes/(?P<mobile>1[3-9]\d{9})/$')



class SMSCodeView(APIView):
    '''
    Short Messaging Service
    '''

    def get(self, request, mobile):
        """
        >短信验证码
        >>校验参数
        >>校验是否已发送
        >>生成验证码,并保存到redis sms_{mobile}
        >>生成发送状态,并保存到redis sms_flag_{mobile}
        >>发送短信验证码
        >>返回client信息
        >>response
        :param request:
        :param mobile:
        :return:
        """
        redis_conn = get_redis_connection('verifications')
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        print(send_flag)
        if send_flag:
            return Response({'message': '请求频繁'}, status=status.HTTP_400_BAD_REQUEST)

        # 生成短信验证码

        sms_code = '%6d' % random.randint(0, 999999)
        # 代码优化 :.setex()每次均与数据库进行交互,有响应时间,故同一函数内进行提取　　
        # # 保存sms
        # redis_conn.setex('sms_%s' % mobile,2*60,sms_code)
        # # save_flag
        # redis_conn.setex('sms_flag_%s' % mobile,60,1)
        print(sms_code)
        pl = redis_conn.pipeline()
        pl.setex("sms_%s" % mobile, 2 * 60, sms_code)
        pl.setex("sms_flag_%s" % mobile, 60, 1)
        pl.execute()
        # 发送短信验证码
        send_sms_code.delay(mobile, sms_code, 2)
        return Response({"message": "OK"})



