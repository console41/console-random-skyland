# -*- coding: utf-8 -*-
from ...modMain import clientSystems
from ...config.configUtils import *
from ...constant.clientConstant import *
from ...pack.clientUtils import *

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
        self.uiNode = clientApi.GetUI(MOD_NAME, UI_NAME)
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
            FullScreenUI(True)
        else:
            PostProcessComp.SetEnableGaussianBlur(False)
            self.GetBaseUIControl(SETTING_UI).SetVisible(False)
            FullScreenUI(False)

    @AddButtonTouchEvent(SUBMIT_BUTTON)
    def SubmitValue(self, args):
        text = self.GetBaseUIControl(EDIT_BOX).asTextEditBox().GetEditText()
        self.GetBaseUIControl(SETTING_UI).SetVisible(False)
        PostProcessComp.SetEnableGaussianBlur(False)
        textNew = text.strip().isdigit()
        if not textNew or '.' in text:
            SendLocalMessage('设置失败 请输入正整数', DEFAULT)
            FullScreenUI(False)
            return
        textNumber = float(text)
        if textNumber <= 1.0:
            SendLocalMessage('设置失败 值需要大于1', DEFAULT)
            FullScreenUI(False)
            return
        client.NotifyToServer('SetUpdateTime', {'time': textNumber, 'playerId': PLAYER_ID})
        SendLocalMessage('正在设置..', DEFAULT)
        FullScreenUI(False)
