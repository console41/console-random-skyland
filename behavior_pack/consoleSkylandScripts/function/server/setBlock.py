# -*- coding: utf-8 -*-

from ...constant.serverConstant import *


def FillSkylandBlocks(blockId, fromPos1=(11, 121, 1), toPos1=(13, 123, 8), fromPos2=(10, 121, 6), toPos2=(7, 123, 8)):
    x1, y1, z1 = fromPos1
    x2, y2, z2 = toPos1

    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            for z in range(z1, z2 + 1):
                BlockInfoComp.SetBlockNew((x, y, z), {'name': blockId}, 0, 0, True, False)
    x3, y3, z3 = fromPos2
    x4, y4, z4 = toPos2
    for x in range(x4, x3 + 1):
        for y in range(y3, y4 + 1):
            for z in range(z3, z4 + 1):
                BlockInfoComp.SetBlockNew((x, y, z), {'name': blockId}, 0, 0, True, False)


def FillSkylandBottomBlocks(blockId, fromPos1=(11, 1), toPos1=(13, 8), fromPos2=(10, 6),
                            toPos2=(7, 8)):
    x1, z1 = fromPos1
    x2, z2 = toPos1
    y = 120
    for x in range(x1, x2 + 1):
        for z in range(z1, z2 + 1):
            BlockInfoComp.SetBlockNew((x, y, z), {'name': blockId}, 0, 0, True, False)
    x3, z3 = fromPos2
    x4, z4 = toPos2
    for x in range(x4, x3 + 1):
        for z in range(z3, z4 + 1):
            BlockInfoComp.SetBlockNew((x, y, z), {'name': blockId}, 0, 0, True, False)
