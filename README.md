# gw2-fishing-man

激战2 钓鱼脚本, 钓力足够的情况下可以帮你解放双手，提高钓鱼效率。


<p style="font-size: 20px; color: rgb(255,255,84);">问就是封，用就别怕！</p>

<p style="font-size: 20px; color: rgb(255,255,84);">哪家小孩天天哭，哪个辅助天天封？</p>


## 使用说明

脚本会先读取 `config.yaml` 文件获取钓鱼坐标设置，该坐标用于 `dxcam` 截图使用。

    `exclamation_offset`: 钓鱼时红色感叹号的抓取坐标

    `drag_bar_offset`:  钓鱼时拖动条的抓取坐标

    `drag_hook_offset`: 钓鱼拉扯时的钓力的抓取坐标

脚本会根据 `config.yaml` 文件中的设置，自动坐标偏移，并进行截图，识别钓鱼红色感叹号、拖动条、钓力等元素，最后根据坐标位置进行操作。

用户可以根据自己游戏环境进行坐标设置，默认坐标支持 1080p 屏幕

### 安装与启动

```shell
pip install -r requirements.txt

# 查看位置
python show_position.py

# 启动脚本
python main.py
```

## 后续更新(画饼……)
1. 钓鱼状态判断优化
2. 支持自定义按键操作
3. 增加鱼饵 和 鱼钩识别
4. 钓鱼拉扯算法优化
5. 减少配置项
6. ......
7. Ai 钓鱼拉扯！
## 声明

本脚本仅供学习交流使用，请勿用于商业用途！
