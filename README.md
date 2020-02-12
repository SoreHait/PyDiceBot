# PyDiceBot

## 概述

用Python写的跑团机器人，使用Nonebot和CQHttp插件

目前版本为0.2.0

## 部署

Python版本要求：3.8.0+ 并安装[Nonebot](https://github.com/richardchien/nonebot "Nonebot GitHub页面")

```
> pip install nonebot
```

需要[酷Q Air](https://cqp.cc/t/23253 "酷Q Air官方页面")/[酷Q Pro](https://cqp.cc/t/14901 "酷Q Pro官方页面")并安装[CQHttp](https://github.com/richardchien/coolq-http-api "CoolQ Http Api GitHub页面")插件

请按照[Nonebot帮助文档](https://nonebot.cqp.moe/guide/getting-started.html "Nonebot帮助文档 #开始使用")设置地址以及端口，config.py在config文件夹内

设置完成后双击main.py启动或运行以下命令

```
> python main.py
```

## 主要设定

除在 **部署** 一节中提到的config.py外，第一次启动后会在同一目录下生成whitelist.json

其中`accept`项为是否同意邀请入群请求

当`accept`为`true`时自动接受**所有**邀请入群请求

当`accept`为`false`时自动接受`whiteusers`内用户的邀请请求或`whitegroups`内群的邀请请求

`whiteusers`和`whitegroups`内填写的分别是用户qq号和群号

## 主要命令

`.help`查看帮助文件

里面什么都写了（主要是懒得再打一次