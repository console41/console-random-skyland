# -*- coding: utf-8 -*-

import random

from ...modMain import clientSystems
from ...config.configUtils import *
from ...constant.serverConstant import *
from ...function.serverFunctionUtils import SendGlobalMessage, FillSkylandBlocks, FillSkylandBottomBlocks, \
    IsInCommandBlock, SendMessageToPlayer

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
            self.hubPos = SKYLAND
            # 设置重生点 防止死亡后掉进虚空
            GameComp.SetSpawnDimensionAndPosition(0, self.hubPos)
            # 将重生半径设为0 防止刷到别的地方去
            GameComp.SetGameRulesInfoServer(GAME_RULE)
        # 不是第一次进入
        else:
            self.remainingTime = self.extraData[TIME_REMAINING]  # type: float
            self.maxTime = self.extraData[TIME_MAX]  # type: float
            self.nextBlock = self.extraData[NEXT_BLOCK]  # type: str
            self.blacklist = self.extraData[BLACK_LIST]  # type: list
            self.currentBlock = self.extraData[CURRENT_BLOCK]  # type: str
            # 设置hub的位置
            self.hubPos = self.extraData[HUB_POS]
            # 把黑名单里的方块从刷新列表中删除
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
                PosComp(pid).SetFootPos(self.hubPos)
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
            SendMessageToPlayer(pid, '设置成功')
            self.maxTime = time
            self.remainingTime = time
        else:
            SendMessageToPlayer(pid, '设置失败 需要操作员权限')

    @Listen
    def CustomCommandTriggerServerEvent(self, args):
        command = args['command']
        origin = args['origin']
        variant = args['variant']
        param = args['args']
        if command == 'hub':
            if IsInCommandBlock(args):
                pid = origin['entityId']
                if param[0]['value'] == '$BACK':
                    DimensionComp(pid).ChangePlayerDimension(0, SKYLAND)
                    # 播放音效
                    RunCommand('/playsound mob.shulker.teleport {}'.format(NameComp(pid).GetName()))
                    args['return_msg_key'] = DEFAULT + '成功回到岛屿'
                else:
                    self.hubPos = param[0]['value']
                    args['return_msg_key'] = DEFAULT + '已将返回点设为({0:.0f}, {0:.0f}, {0:.0f})'.format(*SKYLAND)
            else:
                args['return_failed'] = True
                args['return_msg_key'] = DEFAULT + '该指令在命令方块中禁止使用'
        elif command == 'skyland_controller':
            if IsInCommandBlock(args):
                pid = origin['entityId']
                if variant == 0:
                    if param[0]['value'] == 'blacklist':
                        block = param[2]['value'] if param[2]['value'] != '$CURRENT' else self.currentBlock
                        if param[1]['value'] == 'add':
                            if block == '$CURRENT' and self.currentBlock == None:
                                args['return_failed'] = True
                                args['return_msg_key'] = DEFAULT + '还没有刷新过方块'
                                return
                            if block in self.blacklist:
                                args['return_failed'] = True
                                args['return_msg_key'] = DEFAULT + '该方块已在黑名单内'
                                return
                            self.blacklist.append(block)
                            self.allBlocks.remove(block)
                            args['return_msg_key'] = DEFAULT + '已将方块{}加入黑名单'.format(block)
                        elif param[1]['value'] == 'list':
                            # 这里修改args会比下面的晚发出
                            # args['return_msg_key'] = DEFAULT + '黑名单列表如下:'
                            args['return_msg_key'] = ''
                            SendMessageToPlayer(pid, '当前存档的黑名单列表如下')
                            for b in self.blacklist:
                                SendMessageToPlayer(pid, b)
                            SendMessageToPlayer(pid,
                                                '你所查询的方块{}在黑名单内'.format(
                                                    block) if block in self.blacklist else '你所查询的方块{}不在黑名单里'.format(
                                                    block))
                        elif param[1]['value'] == 'remove':
                            if block not in self.blacklist:
                                args['return_failed'] = True
                                args['return_msg_key'] = DEFAULT + '该方块不在黑名单内'
                                return
                            self.blacklist.remove(block)
                            self.allBlocks.append(block)
                            args['return_msg_key'] = DEFAULT + '已删除{}'.format(block)
                elif variant == 1:
                    if param[0]['value'] == 'next':
                        block = param[1]['value']
                        if block in self.blacklist:
                            args['return_failed'] = True
                            args[
                                'return_msg_key'] = DEFAULT + '不能将{}设置为下次刷新的方块 因为该方块在黑名单内'.format(
                                block)
                            return
                        self.nextBlock = block
                        args['return_msg_key'] = DEFAULT + '已将下次刷新的方块设为{}'.format(block)
                elif variant == 2:
                    if param[0]['value'] == 'land':
                        if param[1]['value'] == 'bedrock':
                            if param[2]['value'] == 'destroy':
                                FillSkylandBottomBlocks('minecraft:air')
                                args['return_msg_key'] = DEFAULT + '已将岛屿下的基岩摧毁'
                            else:
                                FillSkylandBottomBlocks('minecraft:bedrock')
                                args['return_msg_key'] = DEFAULT + '成功放置岛屿下的基岩'

    def Destroy(self):
        ExtraDataComp(LEVEL_ID).SetExtraData(KEY, {TIME_MAX: self.maxTime, 'remaining': self.remainingTime,
                                                   BLACK_LIST: self.blacklist, NEXT_BLOCK: self.nextBlock,
                                                   CURRENT_BLOCK: self.currentBlock, HUB_POS: self.hubPos})
        GameComp.CancelTimer(self.timer)
