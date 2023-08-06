from tweb.error_exception import ErrException, ERROR

from ucenter.services import ctrl_user
from ucenter.services.code import send_message
from ucenter.services.email import send_email

from asyncio import get_event_loop


async def send_notification_sync(uid, msg, types):
    args = uid, msg, types
    return await get_event_loop().run_in_executor(None, send_notification, *args)


def send_notification(uid, msg, types=None):
    """
    发送通知
    :param uid: 用户 id
    :param msg: 通知内容 包含 subject: '标题', message: '内容'
    :param types: 通知形式 ['email', 'sms'] 默认为 邮件、短信同时发送
    :return:
    """
    if types is None:
        types = ['email', 'sms']

    if isinstance(types, str):
        types = [types]

    if not isinstance(types, list):
        assert 'wrong types, should be list or string'

    user = ctrl_user.get(uid)

    if user is None:
        raise ErrException(ERROR.E40101)

    if 'sms' in types:
        mobile = user.get('mobile')
        if mobile is not None:
            send_message(mobile, '{} - {}'.format(msg.get('title'), msg.get('content')))

    if 'email' in types:
        email = user.get('email')
        if email is not None:
            send_email(email, msg)
