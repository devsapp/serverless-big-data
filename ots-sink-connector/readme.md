# TableStoreSinkConnector 帮助文档

<p align="center" class="flex justify-center">
    <a href="https://www.serverless-devs.com" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=TableStoreSinkConnector&type=packageType">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=TableStoreSinkConnector" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=TableStoreSinkConnector&type=packageVersion">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=TableStoreSinkConnector" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=TableStoreSinkConnector&type=packageDownload">
  </a>
</p>

<description>

> ***fc tablestore sink connector***

</description>

## 应用简介
本应用可以将您的原始输入数据进过预处理之后，写入到您创建应用时填写的 Tablestore 数据表中，支持批量传输及单条数据传输，传输的数据格式支持 cloudEvent Schema 以及自定义格式。


## 前期准备
使用该项目，推荐您拥有以下的产品权限 / 策略：

| 服务/业务 | 函数计算 |     
| --- |  --- |   
| 权限/策略 | AliyunFCFullAccess<br>AliyunLogFullAccess<br>AliyunOTSFullAccess |     

<codepre id="codepre">



</codepre>

<deploy>

## 部署 & 体验

<appcenter>

- :fire: 通过 [Serverless 应用中心](https://fcnext.console.aliyun.com/applications/create?template=TableStoreSinkConnector) ，
[![Deploy with Severless Devs](https://img.alicdn.com/imgextra/i1/O1CN01w5RFbX1v45s8TIXPz_!!6000000006118-55-tps-95-28.svg)](https://fcnext.console.aliyun.com/applications/create?template=TableStoreSinkConnector)  该应用。 

</appcenter>

- 通过 [Serverless Devs Cli](https://www.serverless-devs.com/serverless-devs/install) 进行部署：
    - [安装 Serverless Devs Cli 开发者工具](https://www.serverless-devs.com/serverless-devs/install) ，并进行[授权信息配置](https://www.serverless-devs.com/fc/config) ；
    - 初始化项目：`s init TableStoreSinkConnector -d TableStoreSinkConnector`   
    - 进入项目，并进行项目部署：`cd TableStoreSinkConnector && s deploy -y`

</deploy>

<appdetail id="flushContent">

## 使用步骤

### 资源准备

依次创建如下资源：
- tablestore 实例
- tablestore 数据表，按需创建主键

### 应用部署

您可以通过应用中心或直接使用 s 工具进行部署。部署之前，需要对函数的环境变量进行如下检查：
- endpoint 以及 instanceName：是否与目标 tablestore 实例名称匹配
- tableName：是否与目标 tablestore 数据表名称匹配
- primaryKeysName：是否与目标 tablestore 数据表主键匹配


### 应用调用
参数构造完成后，可以通过控制台或者 s 工具进行调用，本文以控制台调用为例，对这两种方式进行介绍。

#### 控制台调用

应用部署完成后，按照如下步骤进行在控制台进行函数调用：
1. 进入[函数计算控制台](https://fcnext.console.aliyun.com/cn-hangzhou/services)，找到对应的 sink 函数
2. 进入测试函数页面，将[参数介绍](#参数介绍)中的参数输入事件输入框中，点击测试函数即可。
![函数测试](https://img.alicdn.com/imgextra/i2/O1CN01VWhwGH1Rx70AiHRfr_!!6000000002177-2-tps-3576-1908.png)

### 高级功能

#### 通过不同网络访问 tablestore 实例
有如下三种网络访问方式：
- 经典网络访问：通过阿里云内网进行访问，不会产生公网流量，同时安全性也高于公网访问,推荐使用
- 公网访问：函数环境变量中的 endpoint 为公网访问地址时，需要 tablestore 开启“公网访问”能力，同时会产生公网流量
- vpc 访问：通过 vpc 网络进行访问，不会产生公网流量，需要为 sink 函数配置 vpc

#### 修改数据库存入点及存入方式
本应用默认将原始数据每条生成一个记录，并将整体 json decode 后存入 data 表中。如果您需要自定义转储方式，可以对 sink 函数 deliver() 方法中的 tablestore 语句进行修改。



</appdetail>

<devgroup>

## 开发者社区

您如果有关于错误的反馈或者未来的期待，您可以在 [Serverless Devs repo Issues](https://github.com/serverless-devs/serverless-devs/issues) 中进行反馈和交流。如果您想要加入我们的讨论组或者了解 FC 组件的最新动态，您可以通过以下渠道进行：

<p align="center">

| <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407298906_20211028074819117230.png" width="130px" > | <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407044136_20211028074404326599.png" width="130px" > | <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407252200_20211028074732517533.png" width="130px" > |
|--- | --- | --- |
| <center>微信公众号：`serverless`</center> | <center>微信小助手：`xiaojiangwh`</center> | <center>钉钉交流群：`33947367`</center> | 

</p>

</devgroup>