# KafkaToOSSConnector 帮助文档

<p align="center" class="flex justify-center">
    <a href="https://www.serverless-devs.com" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=KafkaToOSSConnector&type=packageType">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=KafkaToOSSConnector" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=KafkaToOSSConnector&type=packageVersion">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=KafkaToOSSConnector" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=KafkaToOSSConnector&type=packageDownload">
  </a>
</p>

<description>

> ***Kafka to OSS Connector***

</description>

<table>

## 前期准备
使用该项目，推荐您拥有以下的产品权限 / 策略：

| 服务/业务 | 函数计算 |     
| --- |  --- |   
| 权限/策略 | AliyunFCFullAccess</br>AliyunOSSFullAccess</br>AliyunVPCReadOnlyAccess |     


</table>

<codepre id="codepre">



</codepre>

<deploy>

## 部署 & 体验

<appcenter>

- :fire: 通过 [Serverless 应用中心](https://fcnext.console.aliyun.com/applications/create?template=KafkaToOSSConnector) ，
[![Deploy with Severless Devs](https://img.alicdn.com/imgextra/i1/O1CN01w5RFbX1v45s8TIXPz_!!6000000006118-55-tps-95-28.svg)](https://fcnext.console.aliyun.com/applications/create?template=KafkaToOSSConnector)  该应用。 

</appcenter>

- 通过 [Serverless Devs Cli](https://www.serverless-devs.com/serverless-devs/install) 进行部署：
    - [安装 Serverless Devs Cli 开发者工具](https://www.serverless-devs.com/serverless-devs/install) ，并进行[授权信息配置](https://www.serverless-devs.com/fc/config) ；
    - 初始化项目：`s init KafkaToOSSConnector -d KafkaToOSSConnector`   
    - 进入项目，并进行项目部署：`cd KafkaToOSSConnector && s deploy -y`

</deploy>

<appdetail id="flushContent">


## 应用简介
本应用支持将 kafka 某个 topic 中的消息定时导入到 oss 对应 bucket 中。入参：
```json
{
    "consumer_service_name":"",
    "consumer_function_name":"",
    "kafka_instance_id":"alikafka_post-cn-****",
    "topic_name": "******",
    "consumer_group_id":"******",
    "bucket_name":"******",
    "kafka_endpoint": ["alikafka-post-cn-****-3-vpc.alikafka.aliyuncs.com:9092"]
}
```
说明：
consumer_service_name：调用的 consumer 服务名称
consumer_function_name：调用的 consumer 函数名称
kafka_instance_id：消费的实例 id
topic_name：消费的实例 topic 名称
consumer_group_id：消费组名称
bucket_name：结果存储 bucket 名称
kafka_endpoint：kafka 地址

## 使用步骤

1. 在 kafka 控制台创建实例、topic 及消费组，填入上述的 kafka_instance_id、consumer_group_id 及 topic_name 中；
2. 在 ram 控制台创建一个 ram 角色，并赋予如下权限策略（也可使用示例中的 fc default role）：
```json
{
    "Version": "1",
    "Statement": [
        {
            "Action": [
                "fc:InvokeFunction",
                "log:*",
                "oss:*"
            ],
            "Resource": "*",
            "Effect": "Allow"
        }
    ]
}
```
3. 更新最新版 S 工具；s build --use-docker
4. git clone 本项目。更改 s.yaml 中触发器触发参数为上述实际参数，在项目目录中执行如下命令： `s deploy -t s.yaml`


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