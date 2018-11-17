import  logging
from celery_tasks.main import app
from .yuntongxun.sms import CCP


logger = logging.getLogger('django')

# 验证码模板
SMS_CODE_TEMP_ID = 1

@app.task(name = 'send_sms_code')
def send_sms_code(mobile,sms_code,expires):
    try:
        ccp = CCP()
        result = ccp.send_template_sms(mobile,[sms_code,expires],SMS_CODE_TEMP_ID)
    except Exception as e:
        logger.error('发送验证码短信[异常][mobile: %s,message: %s ]' % (mobile,e))
    else:
        if result==0:
            logger.info('送验证码短信[正常][mobile: %s ]' % (mobile))
        else:
            logger.warning('送验证码短信[失败][mobile: %s ]' % mobile)


