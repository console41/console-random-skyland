# -*- coding: utf-8 -*-

from ..registerer.modMain import clientSystems
from ...config.configUtils import *
from ...constant.clientConstant import *
from ...pack.packUtils import consoleLibClientApi

client = clientApi.GetSystem(MOD_NAME, clientSystems[0][1])  # type: clientApi.GetClientSystemCls()

screenNode = clientApi.GetScreenNodeCls()

__buttonList = []


def AddButtonTouchEvent(path, param={'isSwallow': True}):
    def __wrapper(func):
        __buttonList.append((path, func.__name__, param))
        return func

    return __wrapper


def InitButton(instance):
    for path, callback, param in __buttonList:
        control = instance.GetBaseUIControl(path).asButton()
        control.AddTouchEventParams(param)
        control.SetButtonTouchDownCallback(getattr(instance, callback))


class Main(screenNode):
    def __init__(self, namespace, name, param):
        screenNode.__init__(self, namespace, name, param)
        self.uiNode = None

    def Create(self):
        self.uiNode = clientApi.GetUI(DIR_ROOT, UI_NAME)
        InitButton(self)

    def Destroy(self):
        pass

    def Update(self):
        pass

    @AddButtonTouchEvent(SETTING_BUTTON)
    def ShowSettingUI(self, args):
        if not self.GetBaseUIControl(SETTING_UI).GetVisible():
            PostProcessComp.SetEnableGaussianBlur(True)
            PostProcessComp.SetGaussianBlurRadius(10)
            self.GetBaseUIControl(SETTING_UI).SetVisible(True)
        else:
            PostProcessComp.SetEnableGaussianBlur(False)
            self.GetBaseUIControl(SETTING_UI).SetVisible(False)

    @AddButtonTouchEvent(SUBMIT_BUTTON)
    def SubmitValue(self, args):
        text = self.GetBaseUIControl(EDIT_BOX).asTextEditBox().GetEditText()
        self.GetBaseUIControl(SETTING_UI).SetVisible(False)
        PostProcessComp.SetEnableGaussianBlur(False)

        if text.strip().isdigit() and '.' in text:
            consoleLibClientApi.SendLocalMessage('设置失败 请输入整数', header=DEFAULT)
        textNumber = float(text)
        if not 1.0 < textNumber < 10000.0:
            consoleLibClientApi.SendLocalMessage('设置失败 值需要满足1 < x < 10000 的条件', header=DEFAULT)
        client.NotifyToServer('SetUpdateTime', {'time': float(text), 'playerId': PLAYER_ID})
        consoleLibClientApi.SendLocalMessage('正在设置..', header=DEFAULT)
