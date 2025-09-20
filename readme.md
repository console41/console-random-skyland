# 随机空岛生存

__(下滑查看模组玩法和指令)__

- GitHub开源项目
  
  https://github.com/console41/console-random-skyland

- 协议
  
  MIT License
  
  ```plaintext
  MIT License
  
  Copyright (c) 2025 Console
  
  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
  
  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
  
  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  ```

## 玩法

- 空岛生存经典版玩法 开局一棵树 装备全靠运气

- 刷新
  
  空岛默认每过`180`秒刷新一次 可以通过进度条右侧的齿轮按钮设置时间 需要有管理员权限
  
  所有方块都会刷新 包括模组方块和获取不到的方块 可以通过**黑名单**来控制(具体见下方)

- 工业玩法
  
  我们将原版高度改成了`[-512, 512]`的区间 可以建造任何大型机器 末地和地狱不受影响
  
  **注意**: 虚空地形会影响其他模组继承自主世界的维度 严禁安装在已将加载过地形的地图上 如果已经安装并导致新生成的地形变为虚空
  请立即退出游戏卸载模组 然后使用`Amulet`等工具删除受损区块

- 收集玩法
  
  所有方块都会刷新 所以一些特殊方块也可以获取 因为它们可以被**活塞**推动 甚至是被挖掘

- 肝帝玩法
  
  收集各种资源创建你自己的空岛帝国

- 休闲玩法

## 指令

### hub

- 作用
  
  无视距离和维度返回空岛

- 语法
  
  ```plaintext
  /hub [pos: x y z]
  ```

- 指令参数
  
  | 语法                 | 参数名 | 默认值         | 说明                        |
  | ------------------ | --- | ----------- | ------------------------- |
  | ```[pos: x y z]``` | 位置  | ```$BACK``` | 可不传 不传则返回你设置的返回点 传参则设置返回点 |

- 权限
  
  需要开启作弊 不能在命令方块中运行

- 示例
  
  ```plaintext
  /hub
  ```

### skyland_controller(需要有一定理解能力)

- 作用
  
  控制空岛刷新 删除下方的基岩和方块刷新黑名单 方便控制节目效果 快捷添加方块至黑名单或者快捷从黑名单删除方块

- 权限
  
  需要有操作员权限 不能在命令方块中运行

- 语法
  
  ```plaintext
  /skyland_controller blacklist <list|add|remove> [block: Block]
  
  /skyland_controller blacklist_fast_operate 
      <fast_add|fast_remove> <cake|candle|stairs|slab|door|flower|glass|concrete
       |banner|fence|carpet|terracotta|wall|rail|sign|button|seed|coral|pressure_plate>
  
  /skyland_controller land bedrock <set|destroy>
  
  /skyland_controller next <block: Block>
  ```
  
  - `blacklist`类型的参数说明
    
    | 语法                            | 参数名 | 默认值                 | 说明                                                                          |
    | ----------------------------- | --- | ------------------- | --------------------------------------------------------------------------- |
    | `list` `add` `remove` `reset` | 模式  | 无                   | `list`会列出所有黑名单方块 `add`会增加黑名单方块 `remove`会删除黑名单方块 会存档(下一次进入仍有效) `reset`会重置黑名单 |
    | `block: Block`                | 方块  | `$CURRENT`(当前刷新的方块) | 当模式为`list`时 会输出黑名单中的所有方块 并输出该方块是否在黑名单中 当模式为`reset`时 无需传参                    |
  
  - `land`类型的参数说明
    
    | 语法              | 参数名  | 默认值           | 说明                                       |
    | --------------- | ---- | ------------- | ---------------------------------------- |
    | `bedrock`       | 模式   | 只能输入`bedrock` | 控制空岛下的基岩是否存在                             |
    | `set` `destroy` | 是否存在 | 无             | `set`会放置基岩 `destroy`会删除基岩 并且无视基岩那一层是否有方块 |
  
  - `next`参数的类型说明
    
    | 语法             | 参数名 | 默认值 | 说明                 |
    | -------------- | --- | --- | ------------------ |
    | `block: Block` | 方块  | 无   | 控制下一次刷新要刷新什么方块 会存档 |
  
  - `blacklist_fast_operate`类型的参数说明
    
    | 语法                                              | 参数名  | 默认值 | 说明         |
    |-------------------------------------------------| ---- | --- | ---------- |
    | `fast_add` `fast_remove`                        | 类型   |     | 快速添加/减少    |
    | `cake` `candle` `stairs` `slab` `door` `flower` | 方块类型 |     | 要快速禁用的方块类型 |

- 备注
  
  快捷添加只会从可刷新方块中查找 不会处理已经添加过的方块 删除同理

## 更新内容

版本号: 1.10.0

更新时间: 2025年9月20日 22\:54:34

- 修复fence无法添加到黑名单的问题

- `skyland_controller blacklist_fast_operate fast_add/fast_remove`新增`button seed coral pressure_plate`种类

## 作者信息

- 代码 UI 贴图 策划 项目 测试 开发
  
  Console

- 玩家反馈QQ群
  
  682435163

- 玩家反馈QQ频道
  
  ConsoleGamer

<img src="data:image/png;base64,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" title="" alt="" data-align="center">