# douyuquiz

** v0.2** - [Change log](CHANGELOG.md)

**douyuquiz** 是一个基于**python3.7**开发用于获取 **斗鱼直播间互动竞猜结果** 的脚本。该程序能自动侦测特定主播是否上线，上线后识别互动竞猜内容，竞猜结果将会以 **数据文件(quizdata.db)** 的形式保存。

## 介绍
斗鱼（www.douyu.com) 是一个游戏直播网站。在直播间中，主播可以发起有关直播内容的互动竞猜。
本程序运行后可以自动保存特定主播的互动竞猜记录。记录内容包括竞猜标题，竞猜封盘时鱼丸总数，竞猜封盘时双方赔率和竞猜结果等。


## 特点
* 功能简单（有且只有一个功能）
* 自动侦测主播是否上线。若主播上线则获取竞猜消息，若主播下线或未开播，则每隔10分钟自动识别主播是否上线
* 使用底层socket而不是网页爬虫来获取互动竞猜信息，低配置服务器也能轻松运行

## 安装

使用**pip命令**来安装douyuquiz

```bash
pip install douyuquiz
```
或
```bash
pip3 install douyuquiz
```

## 用法

```python
from douyuquiz import douyuquiz

douyuquiz('room_id')
 #room_id 可以是string或int
```
**room_id** 为主播的房间号，通常在直播房间的url中可以获取  例如 ‘https://www.douyu.com/74751’ **74751** 就是该直播间的房间号。  

**注意：** 在斗鱼的一些特殊活动直播页面中，该数字并不是主播的房间号。如遇到这种情况，可以通过其他方式获取主播的房间号。

运行该python脚本。如果运行成功，将会显示如下信息：
![](https://ws3.sinaimg.cn/large/006tNc79gy1g2d1ocxca7g30qa0d4jtf.gif)
**注:** 程序需要后台挂起  

程序自动生成**douyuquiz.log**文件
![](https://ws3.sinaimg.cn/large/006tNc79gy1g2d04chcz2j31tc08agov.jpg)

当获取到竞猜消息时,将会显示如下内容：
![](https://ws2.sinaimg.cn/large/006tNc79gy1g2d1ec48ixg30r20fn40v.gif)

竞猜结果将会储存到当前文件夹内的**quizdata.db**文件中。如果没有该文件，程序将自动新建**quizdata.db**。

### 竞猜结果

|time|room_id|quiz_id|title|left_title|left_total|left_odd|right_title|right_total|right_odd|result|
|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|:-|
|2019-04-23 18:06:02|......|......|极难模....|不存在的啊|21477867|0.0|可以|1762690|9.9|1

**time:** 产生竞猜结果的时间  
**room_id:** 房间号  
**quiz_id:** 对每一次互动竞猜有斗鱼服务器自动生成的独特ID  
**title:** 互动竞猜的标题  
**left(right)_title:** 该竞猜左边或右边的标题  
**left (right)_total:** 该竞猜左边或右边封盘时的鱼丸总数  
**left (right)_odd:** 该竞猜左边或右边封盘时的赔率  
**result:** 该次竞猜的结果。 ‘1’代表左边胜，‘2’或‘3’代表右边胜。‘0’代表流局

## 感谢

感谢知乎大神 **@天白才痴** 关于如何获取斗鱼弹幕的教程  
感谢各位斗鱼主播
由于技术有限，欢迎大家对于本程序提出建议或意见。  
邮箱：youbao2@hotmail.com  
![](https://ws2.sinaimg.cn/large/006tNc79gy1g2d2wykjwzg30h609mkjm.gif)
