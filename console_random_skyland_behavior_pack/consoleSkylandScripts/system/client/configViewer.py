# -*- coding: utf-8 -*-
from mod.client.plugin.generalSetting.SettingInst import SettingInst

from ...config.configUtils import *
from ...constant.clientConstant import *
from ...library.consoleLib.clientApi import *
from ...library.consoleMod.clientApi import Listen
from ...library.consoleMod.config.configUtils import CLIENT_SYSTEM_NAME

clientSystem = clientApi.GetSystem(MOD_NAME, CLIENT_SYSTEM_NAME)

NotifyToServer = clientSystem.NotifyToServer
CreateEngineSfx = clientSystem.CreateEngineSfx
CreateEngineSfxFromEditor = clientSystem.CreateEngineSfxFromEditor
CreateEngineParticle = clientSystem.CreateEngineParticle
CreateEngineEffectBind = clientSystem.CreateEngineEffectBind
DestroyEntity = clientSystem.DestroyEntity
CreateClientEntityByTypeStr = clientSystem.CreateClientEntityByTypeStr
DestroyClientEntity = clientSystem.DestroyClientEntity
BroadcastEvent = clientSystem.BroadcastEvent

settingInst = None  # type: None | SettingInst

maxTimeStr = ''


def SetMaxTime(_, value):
    global maxTimeStr
    maxTimeStr = value


def Submit(_, __):
    # 关闭界面
    NeteaseWindowComp.CloseSettingUI()
    if not maxTimeStr.isdigit() or '.' in maxTimeStr:
        SendLocalMessage('设置失败 请输入正整数', DEFAULT)
        return
    textNumber = float(maxTimeStr)
    if textNumber <= 1.0:
        SendLocalMessage('设置失败 值需要大于1', DEFAULT)
        return
    NotifyToServer('SetUpdateTime', {'time': textNumber, 'playerId': PLAYER_ID})
    SendLocalMessage('正在设置..', DEFAULT)


@Listen
def UiInitFinished(_):
    global settingInst
    settingInst = NeteaseWindowComp.RegisterSettingInst(ITEM_ID)
    # 添加控件
    settingInst.AddText('$GLOBAL_CONFIG_TEXT', '全局配置(需管理员权限)')
    settingInst.AddInput('$UPDATE_TIME_INPUT', '设置刷新间隔(秒)', SetMaxTime, default='180.0')
    settingInst.AddButton('$SUBMIT_MAX_TIME', '提交', '确定', Submit)
