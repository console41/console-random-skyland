# -*- coding: utf-8 -*-

import random

from ..registerer.modMain import clientSystems
from ...config.configUtils import *
from ...constant.serverConstant import *
from ...function.serverFunctionUtils import SendGlobalMessage, FillSkylandBlocks, FillSkylandBottomBlocks, \
    IsInCommandBlock

__eventList = []


def Listen(funcOrStr=None, namespace=serverApi.GetEngineNamespace(), systemName=serverApi.GetEngineSystemName(),
           priority=0):
    def wrapper(func):
        __eventList.append(
            (namespace, systemName, funcOrStr if isinstance(funcOrStr, str) else func.__name__, func, priority))
        return func

    return wrapper(funcOrStr) if callable(funcOrStr) else wrapper


def InitListen(instance):
    for namespace, systemName, eventName, callback, priority in __eventList:
        instance.ListenForEvent(namespace, systemName, eventName, instance, callback, priority)


class Main(serverApi.GetServerSystemCls()):
    def __init__(self, namespace, systemName):
        super(Main, self).__init__(namespace, systemName)
        InitListen(self)
        self.currentBlock = None
        # 判断是否是第一次进入
        self.extraData = ExtraDataComp(LEVEL_ID).GetExtraData(KEY)
        self.allBlocks = BlockInfoComp.GetLoadBlocks()
        # 是第一次进入
        if not self.extraData:
            self.remainingTime = 180
            self.maxTime = 180.0
            self.blacklist = []
            self.nextBlock = None
            # 设置重生点 防止死亡后掉进虚空
            GameComp.SetSpawnDimensionAndPosition(0, SKYLAND)
        # 不是第一次进入
        else:
            self.maxTime = self.extraData[TIME_MAX]
            self.remainingTime = self.extraData[TIME_REMAINING]
            self.blacklist = self.extraData[BLACK_LIST]  # type: list
            self.nextBlock = self.extraData[NEXT_BLOCK]
            for x in self.blacklist:
                self.allBlocks.remove(x)

        self.timer = GameComp.AddRepeatedTimer(1.0, self.RemoveTimer)

    def RemoveTimer(self):
        '''
        计时器事件 时间减少时
        '''
        self.remainingTime -= 1
        self.BroadcastToAllClient('SetTime',
                                  {'time': self.remainingTime, 'percentage': self.remainingTime / self.maxTime})
        if not self.extraData:
            if not ChunkSourceComp.CheckChunkState(0, (0, 100, 0)):
                return
            # 放置结构
            GameComp.PlaceStructure(None, (1.0, 120.0, 1.0), STRUCTURE_NAME, 0)
            self.extraData = -1
            for pid in serverApi.GetPlayerList():
                PosComp(pid).SetFootPos((9.5, 124.5, 7.5))
        if self.remainingTime <= 0:
            self.remainingTime = self.maxTime
            block = random.choice(self.allBlocks) if not self.nextBlock else self.nextBlock
            self.nextBlock = None
            self.currentBlock = block
            FillSkylandBlocks(block)
            SendGlobalMessage('方块已刷新')
            RunCommand('/playsound random.levelup @a')

    @Listen('SetUpdateTime', MOD_NAME, clientSystems[0][1])
    def SetUpdateTime(self, args):
        pid = args['playerId']
        time = args['time']
        operation = PlayerComp(pid).GetPlayerOperation()
        if operation == 2:
            SendGlobalMessage(pid, '设置成功')
            self.maxTime = time
            self.remainingTime = time
        else:
            SendGlobalMessage(pid, '设置失败 需要操作员权限')

    @Listen
    def CustomCommandTriggerServerEvent(self, args):
        command = args['command']
        origin = args['origin']
        variant = args['variant']
        param = args['args']
        if command == 'hub':
            if IsInCommandBlock(args):
                pid = origin['entityId']
                if DimensionComp(pid).ChangePlayerDimension(0, SKYLAND):
                    # 播放音效
                    RunCommand('/playsound mob.shulker.teleport {}'.format(NameComp(pid).GetName()))
                    args['return_msg_key'] = DEFAULT + '成功回到岛屿'
            else:
                args['return_failed'] = True
                args['return_msg_key'] = '该指令在命令方块中禁止使用'
        elif command == 'skyland_controller':
            if IsInCommandBlock(args):
                if variant == 0:
                    if param[0]['value'] == 'blacklist':
                        block = param[2]['value'] if param[2]['value'] != '$CURRENT' else self.currentBlock
                        if param[1]['value'] == 'add':
                            if block in self.blacklist:
                                args['return_failed'] = True
                                args['return_msg_key'] = '该方块已在黑名单内'
                                return
                            self.blacklist.append(block)
                            self.allBlocks.remove(block)
                            args['return_msg_key'] = '已将方块{}加入黑名单'.format(block)
                        elif param[1]['value'] == 'list':
                            args['return_msg_key'] = '当前黑名单:{}'.format(self.blacklist)
                        elif param[1]['value'] == 'remove':
                            if block not in self.blacklist:
                                args['return_failed'] = True
                                args['return_msg_key'] = '该方块不在黑名单内'
                                return
                            self.blacklist.remove(block)
                            self.allBlocks.append(block)
                            args['return_msg_key'] = '已删除{}'.format(block)
                elif variant == 1:
                    if param[0]['value'] == 'next':
                        block = param[1]['value']
                        if block in self.blacklist:
                            args['return_failed'] = True
                            args['return_msg_key'] = '不能将{}设置为下次刷新的方块 因为该方块在黑名单内'.format(block)
                            return
                        self.nextBlock = block
                        args['return_msg_key'] = '已将下次刷新的方块设为{}'.format(block)
                elif variant == 2:
                    if param[0]['value'] == 'land':
                        if param[1]['value'] == 'bedrock':
                            if param[2]['value'] == 'destroy':
                                FillSkylandBottomBlocks('minecraft:air')
                                args['return_msg_key'] = '已将岛屿下的基岩摧毁'
                            else:
                                FillSkylandBottomBlocks('minecraft:bedrock')
                                args['return_msg_key'] = '成功放置岛屿下的基岩'

    def Destroy(self):
        ExtraDataComp(LEVEL_ID).SetExtraData(KEY, {TIME_MAX: self.maxTime, 'remaining': self.remainingTime,
                                                   BLACK_LIST: self.blacklist, NEXT_BLOCK: self.nextBlock})
        GameComp.CancelTimer(self.timer)
