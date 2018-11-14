from rest_framework.views import exception_handler as  drf_exception_handler
import logging
from django.db import DatabaseError
from redis.exceptions import RedisError
from rest_framework.response import Response
from rest_framework import status
logger  = logging.getLogger('django')
def exception_handler(exc,context):
    """

    :param exc:
    :param context:
    :return:
    """
    # 1.DRF 处理异常
    # 2.处理异常
    response = drf_exception_handler(exc,context)
    if not response:
        # 处理其余异常
        logger.error('[%s] %s' % (context['view'],exc))
        if isinstance(exc,DatabaseError) or isinstance(exc,RedisError):

            return Response({'error':'服务器内部错误'},status=507)
    return Response