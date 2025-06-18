# -*- coding: utf-8 -*-

from ...config.configUtils import DEFAULT
from ...constant.clientConstant import *


def SendLocalMessage(msg, color=ENUM.ColorCode.WHITE, header=DEFAULT):
    """
    聊天框发送一条消息
    (原SetServerMessage)
    :param msg: 消息内容
    :param color: 颜色 默认白色
    :rtype: None
    """
    TextNotifyComp.SetLeftCornerNotify(header + color + msg)
