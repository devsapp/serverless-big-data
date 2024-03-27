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
### 基于函数计算实现的 kafka proxy，通过 HTTP 方式将消息传递至 Kafka 特定 Topic

本应用可以将您的原始输入数据进过预处理之后，传输到您的 kafka topic 中。 函数的触发方式为 http POST 同步/异步触发(如果您需要指定触发时采用异步方式，即在 header 中添加：'x-fc-invocation-type': 'Async'),
  http 触发 url 可以从函数的触发器中获取。您也可以通过创建自定义域名，使用自定义域名进行触发。

当 sink 函数执行失败后，如果您进行了死信队列配置，系统会将失败详情自动发送到您创建应用指定的 mns 队列中。如果您采用同步调用方式，请关注调用后的返回信息。

## 使用步骤
您可以通过应用中心或直接使用 s 工具进行部署。
1. 准备资源：创建 kafka 实例，如果您需要使用异步调用，并在失败时通知您的死信队列，创建 mns 死信队列；
2. 部署应用；参数按照需要进行填写。参数如下：
    region: 应用所在的地区
    serviceName: 服务名称，只能包含字母、数字、下划线和中划线。不能以数字、中划线开头。长度在 1-128 之间
    vpcId: Kafka 所在的 VPC id。请注意需要填写函数计算支持的 az
    vswitchIds: Kafka 所在 VPC 中的 vswitch id，用于内网访问 kafka
    securityGroupId: Kafka 所在 VPC 中的安全组 id，用于内网访问 kafka
    bootstrapServers: Kafka bootstrapServers, 可以从 kafka 控制台获取
    topicName: Kafka 实例 topic name，数据将被放入该 topic 中
    failureDestinationNotification: 执行失败死信队列 destination resource arn。如果使用 mns，请参考如下格式： acs:mns:{region}:{accountID}:/queues/{queueName}/messages
3. 进行测试。构建输入参数
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
如果您需要对原始数据进行处理，可以修改函数中的 transform 方法，以便按照您需要的方式对数据进行预处理。

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
