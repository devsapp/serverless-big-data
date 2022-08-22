# KafkaHTTPProxy 帮助文档

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

> ***函数计算 kafka oss window sink connector***

</description>

## 前期准备
使用该项目，推荐您拥有以下的产品权限 / 策略：

| 服务/业务 | 函数计算                                                               |     
| --- |--------------------------------------------------------------------|   
| 权限/策略 | AliyunFCFullAccess</br>AliyunLogFullAccess</br>AliyunOSSFullAccess |     


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

## 应用简介
本应用可以将您的原始输入数据进过预处理之后，按照 window 逻辑攒批生成 oss bucket 文件。 整个应用由两个函数构成

- Transform Function： 数据预处理函数，可自定义预处理逻辑，处理后的数据会进入到 sink 函数中攒批上传；
- Sink Function：数据投递函数，接收数据后将其投递到下游服务中。该函数支持了 window 逻辑，支持按照批大小、批时间上传文件。

Sink 函数逻辑描述：Sink 函数处理仍是单条消息，当消息上传时，会按照 window 条件进行判断。如果满足 window 的 batch size 或文件时间以满足时间窗口，
则将会生成新的文件继续上传。整个逻辑采用了 oss append 的方式生成文件，因此逻辑是串行的。如果您的并发量较大，请考虑按照业务逻辑并行分函数进行处理的方式。

如果您需要对数据进行转换，可以编写应用创建后的 transform 函数。否则您只需调用 sink 函数即可。

## 使用步骤
您可以通过应用中心或直接使用 s 工具进行部署。
1. 准备资源：创建 kafka 实例；
2. 部署应用；参数按照需要进行填写。参数如下：
```
    region: 应用所在的地区
    serviceName: 服务名称，只能包含字母、数字、下划线和中划线。不能以数字、中划线开头。长度在 1-128 之间
    eventSchema: 输入消息 schema 类型。应用内函数将对特定类型的消息进行入参校验。支持的类型如下：
      enum:
        - customized
        - cloudEvent
    batchOrNot: 输入消息的类型：是否为批量消息
      enum:
        - "True"
        - "False"
    cacheSizeInMB: 窗口的 batch size 大小。当上传的单一文件满足该 batch size 后，则生成新的文件继续上传。
    cacheTimeWindowInSec: 时间窗口大小。当上传的单一文件存活时间（当前时间 - 创建时间）大于该窗口时，则生成新的文件继续上传。
    bucketName: 上传的文件 bucket 名称。
    objectPath: 上传文件的目录名称。
    objectPrefix: 上传的文件名称前缀。生成的文件将根据以下规则：{objectPath}/{objectPrefix}_{file_num} 生成。其中 file_num 为系统自动生成，每个满足窗口条件的文件将对应一个具体数值。
```

3. 进行测试。构建输入参数（以 dataSchema：cloudEvent 为例）
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
之后调用 invokeFunction（使用http 调用）进行测试。


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
