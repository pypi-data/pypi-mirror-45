# -*- coding: utf-8 -*-
from asyncio import get_event_loop
from message_tpl import Templates
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
    msg = Templates['code'].copy()
    content = msg['content'].format(code)
    send_message(mobile, content)


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
    msg = Templates['code'].copy()
    msg['content'] = msg['content'].format(code)

    send_email(email, msg)
