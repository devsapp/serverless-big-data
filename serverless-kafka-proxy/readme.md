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

> ***函数计算 kafka http proxy***

</description>

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

## 应用简介
本应用可以将您的原始输入数据进过预处理之后，传输到您的 kafka topic 中。 整个应用由两个函数构成

- Transform Function： 数据预处理函数，可自定义预处理逻辑，处理后的源端数据会返回。触发方式为 http POST 触发，http 触发 url 可以从函数的触发器中获取；
- Sink Function：数据投递函数，接收数据后将其投递到下游服务中。触发方式为 http POST 同步/异步触发(如果您需要指定触发时采用异步方式，即在 header 中添加：'x-fc-invocation-type': 'Async'),
  http 触发 url 可以从函数的触发器中获取。

如果您需要对数据进行转换，可以编写应用创建后的 transform 函数。否则您只需调用 sink 函数即可。
注意：
1. transform 函数及 sink 函数都是由 http 触发方式触发；
2. 建议 sink 函数使用异步方式触发，否则死信队列将不支持，当 sink 函数执行失败后，系统会将失败详情自动发送到您创建应用指定的 mns 队列中。如果您采用同步调用方式，请关注调用后的返回信息。

## 使用步骤
您可以通过应用中心或直接使用 s 工具进行部署。
1. 准备资源：创建 kafka 实例，创建 mns 死信队列；
2. 部署应用；参数按照需要进行填写。参数如下：
    region: 应用所在的地区
    serviceName: 服务名称，只能包含字母、数字、下划线和中划线。不能以数字、中划线开头。长度在 1-128 之间
    eventSchema: 输入消息 schema 类型。应用内函数将对特定类型的消息进行入参校验。支持的类型如下：
      enum:
        - customized
        - cloudEvent
    vpcId: Kafka 所在的 VPC id。请注意需要填写函数计算支持的 az
    vswitchIds: Kafka 所在 VPC 中的 vswitch id，用于内网访问 kafka
    securityGroupId: Kafka 所在 VPC 中的安全组 id，用于内网访问 kafka
    bootstrapServers: Kafka bootstrapServers, 可以从 kafka 控制台获取
    topicName: Kafka 实例 topic name，数据将被放入该 topic 中
    batchOrNot: 输入消息的类型：是否为批量消息
      enum:
        - "True"
        - "False"
    failureDestinationNotification: 执行失败死信队列 destination resource arn。如果使用 mns，请参考如下格式： acs:mns:{region}:{accountID}:/queues/{queueName}/messages
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
