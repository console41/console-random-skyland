# -*- coding: utf-8 -*-

from ..registerer.modMain import serverSystems
from ...config.configUtils import *
from ...constant.clientConstant import *

__eventList = []


def Listen(funcOrStr=None, namespace=clientApi.GetEngineNamespace(), systemName=clientApi.GetEngineSystemName(),
           priority=0):
    def wrapper(func):
        __eventList.append(
            (namespace, systemName, funcOrStr if isinstance(funcOrStr, str) else func.__name__, func, priority))
        return func

    return wrapper(funcOrStr) if callable(funcOrStr) else wrapper


def InitListen(instance):
    for namespace, systemName, eventName, callback, priority in __eventList:
        instance.ListenForEvent(namespace, systemName, eventName, instance, callback, priority)


class Main(clientApi.GetClientSystemCls()):
    def __init__(self, namespace, systemName):
        super(Main, self).__init__(namespace, systemName)
        InitListen(self)
        self.uiNode = None

    @Listen
    def UiInitFinished(self, args):
        clientApi.RegisterUI(MOD_NAME, UI_NAME, CLS_PATH, SCREEN_PATH)
        self.uiNode = clientApi.CreateUI(MOD_NAME, UI_NAME, CREATE_PARAM)
        self.uiNode.GetBaseUIControl(SETTING_UI).SetVisible(False)

    @Listen('SetTime', MOD_NAME, serverSystems[0][1])
    def SetTime(self, args):
        # 防止ui未创建
        if not self.uiNode:
            return
        textUIControl = self.uiNode.GetBaseUIControl(TEXT).asLabel()
        textUIControl.SetText('距离方块刷新还有{}秒'.format(int(args['time'])))
        self.uiNode.GetBaseUIControl(PROGRESS_BAR).asProgressBar().SetValue(
            args['percentage'])