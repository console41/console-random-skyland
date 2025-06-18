# -*- coding: utf-8 -*-
from ...config.configUtils import DEFAULT
from ...constant.serverConstant import *


def SendGlobalMessage(msg, color=ENUM.ColorCode.WHITE, header=DEFAULT):
    """
    聊天框发送一条消息
    (原SetServerMessage)
    :param msg: 消息内容
    :param color: 颜色 默认白色
    :return: 是否成功
    :rtype: bool
    """
    return GameComp.SetNotifyMsg(header + msg, color)
