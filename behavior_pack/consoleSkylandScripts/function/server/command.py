# -*- coding: utf-8 -*-

def IsInCommandBlock(originArgs):
    """
    判断自定义指令是否在命令方块中运行
    :param originArgs: CustomCommandTriggerServerEvent事件触发后的原始数据
    :return: 是否是在命令方块中运行的
    :rtype: bool
    """
    return originArgs['origin'].has_key('entityId')