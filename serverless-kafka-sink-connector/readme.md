# FCKafkaSinkConnector 帮助文档

<p align="center" class="flex justify-center">
    <a href="https://www.serverless-devs.com" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=FCMysqlSinkConnector&type=packageType">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=FCMysqlSinkConnector" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=FCMysqlSinkConnector&type=packageVersion">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=FCMysqlSinkConnector" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=FCMysqlSinkConnector&type=packageDownload">
  </a>
</p>

<description>

> ***函数计算 kafka sink connector***

</description>

## 应用简介
本应用可以将您的原始输入数据进过预处理之后，传输到您的 kafka topic 中。 

本应用在事件数据传输中主要负责数据的数据预处理以及数据投递，其流程可参考下图：

![简介图](https://img.alicdn.com/imgextra/i1/O1CN01E9a3ZD230u3yoFO84_!!6000000007194-2-tps-2864-1082.png)

Poller Service 从源端拉取数据后，再推送给本应用对应的 Sink Service，最终投递到下游服务中，Sink Service 中包含两个功能函数：
- Transform Function： 数据预处理函数，可自定义预处理逻辑，处理后的源端数据会被发送到 Sink Function 中。
- Sink Function：数据投递函数，接收数据后将其投递到下游服务中。

如果您需要对数据进行转换，可以编写应用创建后的 transform 函数。否则您只需调用 sink 函数即可。

## 前期准备
使用该项目，推荐您拥有以下的产品权限 / 策略：

| 服务/业务 | 函数计算 |     
| --- |  --- |   
| 权限/策略 | AliyunFCFullAccess</br>AliyunLogFullAccess</br>AliyunVPCReadOnlyAccess |     


<codepre id="codepre">



</codepre>

<deploy>

## 部署 & 体验

<appcenter>

- :fire: 通过 [Serverless 应用中心](https://fcnext.console.aliyun.com/applications/create?template=FCKafkaSinkConnector) ，
[![Deploy with Severless Devs](https://img.alicdn.com/imgextra/i1/O1CN01w5RFbX1v45s8TIXPz_!!6000000006118-55-tps-95-28.svg)](https://fcnext.console.aliyun.com/applications/create?template=FCMysqlSinkConnector)  该应用。 

</appcenter>

- 通过 [Serverless Devs Cli](https://www.serverless-devs.com/serverless-devs/install) 进行部署：
    - [安装 Serverless Devs Cli 开发者工具](https://www.serverless-devs.com/serverless-devs/install) ，并进行[授权信息配置](https://www.serverless-devs.com/fc/config) ；
    - 初始化项目：`s init FCKafkaSinkConnector -d FCKafkaSinkConnector`   
    - 进入项目，并进行项目部署：`cd FCKafkaSinkConnector && s deploy -y`

</deploy>

<appdetail id="flushContent">


## 使用步骤
您可以通过应用中心或直接使用 s 工具进行部署。
1. 准备资源：创建 mysql 实例，并开启公网访问；
2. 部署应用；参数按照需要进行填写；
3. 进行测试。构建输入参数（dataSchema：cloudEvent）
```
{
    "data":{
        "requestId":"xx"
    },
    "id":"xx",
    "source":"acs:mns",
    "specversion":"1.0",
    "type":"mns:Queue:SendMessage",
    "datacontenttype":"application/json; charset\\u003dutf-8",
    "time":"xx-xx-xxT00:00:00.000Z",
    "subject":"acs:mns:cn-hangzhou:xxxx:queues/xxx",
    "aliyunaccountid":"xx"
}
```
之后调用 invokeFunction（控制台测试或使用 SDK）进行测试。

#### 控制台调用

应用部署完成后，按照如下步骤进行在控制台进行函数调用：
1. 进入[函数计算控制台](https://fcnext.console.aliyun.com/cn-hangzhou/services)，找到对应的 sink 函数
2. 进入测试函数页面，将[参数介绍](#参数介绍)中的参数输入事件输入框中，点击测试函数即可。
![函数测试](https://img.alicdn.com/imgextra/i2/O1CN01VWhwGH1Rx70AiHRfr_!!6000000002177-2-tps-3576-1908.png)

#### s 工具调用
应用部署完成后，按照如下步骤进行通过 s 工具进行函数调用：
1. 进入应用项目工程下，在 s.yaml 查找应用初始化时输入的 `batchOrNot` 值，若：
   - `batchOrNot` 为 False：将文件 event-template/sink-single-event.json 中的值修改为目标值后，执行 `s sink invoke --event-file event-template/sink-single-event.json` 进行函数调用
   - `batchOrNot` 为 True：将文件 event-template/sink-batch-event.json 中的值修改为目标值后，执行 `s sink invoke --event-file event-template/sink-batch-event.json` 进行函数调用
2. 函数调用完成后，可以登陆到 [kafka 控制台](https://kafka.console.aliyun.com/)查看目标数据表中是否已经写入数据。


### 高级功能
#### 自定义数据转储处理逻辑
本应用创建后会生成两个函数：transform 函数及 sink 函数。如果您需要对原始数据进行处理，可以编写 transform 函数中的 transform 方法，以便按照您需要的方式对数据进行预处理。

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
