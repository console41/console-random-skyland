# -*- coding: utf-8 -*-
from ...config.configUtils import *
from ...constant.clientConstant import *
from ...library.consoleMod.clientApi import Listen
from ...library.consoleMod.config.configUtils import SERVER_SYSTEM_NAME, CLIENT_SYSTEM_NAME

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

uiNode = None  # type: None | clientApi.GetScreenNodeCls()


@Listen
def UiInitFinished(_):
    clientApi.RegisterUI(MOD_NAME, UI_NAME, CLS_PATH, SCREEN_PATH)
    global uiNode
    uiNode = clientApi.CreateUI(MOD_NAME, UI_NAME, CREATE_PARAM)


@Listen(namespace=MOD_NAME, systemName=SERVER_SYSTEM_NAME)
def SetTime(args):
    # 防止ui未创建
    if not uiNode:
        return
    text = uiNode.GetBaseUIControl(TEXT).asLabel()
    text.SetText('距离方块刷新还有{}秒'.format(int(args['time'])))
    uiNode.GetBaseUIControl(PROGRESS_BAR).asProgressBar().SetValue(
        args['percentage'])
