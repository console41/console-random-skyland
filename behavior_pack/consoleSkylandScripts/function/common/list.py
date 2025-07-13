# -*- coding: utf-8 -*-

def QueryElementByKeyword(queryList, keyword):
    # type: (list[str], str) -> list
    """
    查找一个列表中所有含有关键词的元素
    :param queryList: 被查询的列表
    :param keyword: 关键词
    :return: 匹配上的元素的列表 没有则返回空列表
    """
    result = []
    for i in queryList:
        if keyword in i:
            result.append(i)
    return result