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
本应用可以将您的原始输入数据进过预处理之后，按照 window 逻辑攒批生成 oss bucket 文件。在数据投递函数中，接收数据后将其投递到下游服务中。该函数支持了 window 逻辑，支持按照批大小、批时间上传文件。

Sink 函数逻辑描述：Sink 函数处理仍是单条消息，当消息上传时，会按照 window 条件进行判断。如果满足 window 的 batch size 或文件时间以满足时间窗口，
则将会生成新的文件继续上传。整个逻辑采用了 oss append 的方式生成文件，因此逻辑是串行的。如果您的并发量较大，请考虑按照业务逻辑并行分函数进行处理的方式。

本应用一般与 Kafka connector 联合使用。您可以通过创建 Kafka connector 自动触发函数，将 Kafka 内消息按照攒批规则批量上传到 oss 中。

## 使用步骤
您可以通过应用中心或直接使用 s 工具进行部署。
1. 部署应用；参数按照需要进行填写。参数说明如下：
```
    region: 应用所在的地区
    serviceName: 服务名称，只能包含字母、数字、下划线和中划线。不能以数字、中划线开头。长度在 1-128 之间
    concurrency: 数据处理的并发度。并发度越大，吞吐越高，同时生成的文件数越多。
    cacheSizeInMB: 窗口的 batch size 大小。当上传的单一文件满足该 batch size 后，则生成新的文件继续上传。
    cacheTimeWindowInSec: 时间窗口大小。当上传的单一文件存活时间（当前时间 - 创建时间）大于该窗口时，则生成新的文件继续上传。
    bucketName: 上传的文件 bucket 名称。
    objectPath: 上传文件的目录名称。
    objectPrefix: 上传的文件名称前缀。生成的文件将根据以下规则：{objectPath}/{date}/{objectPrefix}_partition_{num}_{file_num} 生成。其中 date 为按照天自动生成，格式为 20220101；num 为系统自动生成，每个并发度对应一个数据，file_num 为系统自动生成，每个满足窗口条件的文件将对应一个具体数值。
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

4. 待测试完成后，您可以在 Kafka 控制台创建函数 connector，实时消费 topic 数据并攒批上传 oss。

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
