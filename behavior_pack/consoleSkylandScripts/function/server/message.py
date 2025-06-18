# -*- coding: utf-8 -*-
from ...config.configUtils import DEFAULT
from ...constant.serverConstant import *


def SendGlobalMessage(msg, header=DEFAULT, color=ENUM.ColorCode.WHITE):
    """
    聊天框发送一条消息
    (原SetServerMessage)
    :param header: 消息头
    :param msg: 消息内容
    :param color: 颜色 默认白色
    :return: 是否成功
    :rtype: bool
    """
    return GameComp.SetNotifyMsg(header + msg, color)


def SendMessageToPlayer(pid, msg, header=DEFAULT, color=ENUM.ColorCode.WHITE):
    """
    给指定玩家发送消息
    (原SetClientMessage)
    :param pid: 接收消息的玩家ID
    :param msg: 消息内容
    :param color: 颜色 默认白色
    :return: 无
    """
    MsgComp(LEVEL_ID).NotifyOneMessage(pid, header + msg, color)
