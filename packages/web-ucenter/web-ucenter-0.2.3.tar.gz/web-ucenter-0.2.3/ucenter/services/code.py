# -*- coding: utf-8 -*-
from asyncio import get_event_loop
from config import EMAIL, SMS
from ucenter.services.email import send_email
from ucenter.services.sms import send_message


async def send_sms_code(business_id, mobile, code, tpl_type=0):
    """
    发送短信验证码
    :param business_id:
    :param mobile:
    :param code:
    :param tpl_type:
    :return:
    """
    code_tpl = SMS['tpl']['code']
    content = code_tpl['content']
    msg = content.format(code)
    send_message(mobile, msg)


async def send_email_code_sync(email, code):
    """
    发送邮箱验证码
    :param email:
    :param code:
    :return:
    """
    args = email, code
    return await get_event_loop().run_in_executor(None, send_email_code, *args)


def send_email_code(email, code):
    code_tpl = EMAIL['tpl']['code']
    title = code_tpl['title']
    content = code_tpl['content']
    msg = {
        'subject': title,
        'message': content.format(code)
    }
    send_email(email, msg)
