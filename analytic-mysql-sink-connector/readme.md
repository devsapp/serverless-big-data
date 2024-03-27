# FCMysqlSinkConnector 帮助文档

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

> ***函数计算 mysql sink connector***

</description>

## 应用简介
本应用可以将您的原始输入数据进过预处理之后，写入到您创建应用时填写的数据库中。

如果您需要对数据进行转换，可以编写应用创建后的 transform 函数。否则您只需调用 sink 函数即可。

## 前期准备
使用该项目，推荐您拥有以下的产品权限 / 策略：

| 服务/业务 | 函数计算 |     
| --- |  --- |   
| 权限/策略 | AliyunFCFullAccess<br>AliyunLogFullAccess |     


<codepre id="codepre">



</codepre>

<deploy>

## 部署 & 体验

<appcenter>

- :fire: 通过 [Serverless 应用中心](https://fcnext.console.aliyun.com/applications/create?template=FCMysqlSinkConnector) ，
[![Deploy with Severless Devs](https://img.alicdn.com/imgextra/i1/O1CN01w5RFbX1v45s8TIXPz_!!6000000006118-55-tps-95-28.svg)](https://fcnext.console.aliyun.com/applications/create?template=FCMysqlSinkConnector)  该应用。 

</appcenter>

- 通过 [Serverless Devs Cli](https://www.serverless-devs.com/serverless-devs/install) 进行部署：
    - [安装 Serverless Devs Cli 开发者工具](https://www.serverless-devs.com/serverless-devs/install) ，并进行[授权信息配置](https://www.serverless-devs.com/fc/config) ；
    - 初始化项目：`s init FCMysqlSinkConnector -d FCMysqlSinkConnector`   
    - 进入项目，并进行项目部署：`cd FCMysqlSinkConnector && s deploy -y`

</deploy>

<appdetail id="flushContent">


## 使用步骤
您可以通过应用中心或直接使用 s 工具进行部署。
1. 准备资源：创建 mysql 实例，并开启公网访问；
2. 部署应用；参数按照需要进行填写；
>注：应用模板内参数中的 user 以及 password 均为敏感信息，因此不建议将应用放到任何代码仓库(Github, Gitee, Gitlab 等)上允许公开访问

3. 进行测试。构建输入参数（dataSchema：cloudEvent）
```
{
    "data":{
        "requestId":"xx",
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


### 高级功能
#### 通过 vpc 连接 mysql 实例 
本应用默认使用的是公网连接 mysql 实例，在实际使用中需要考虑安全问题，因此建议您使用 VPC 连接 mysql 实例。具体参考：https://help.aliyun.com/document_detail/147916.html
#### 自定义数据转储处理逻辑
本应用创建后会生成两个函数：transform 函数及 sink 函数。如果您需要对原始数据进行处理，可以编写 transform 函数中的 transform 方法，以便按照您需要的方式对数据进行预处理。
#### 修改数据库存入点及存入方式
本应用默认将原始数据每条生成一个记录，并将整体 json decode 后存入 data 表中。如果您需要自定义转储方式，可以对 sink 函数 sink() 方法中的 mysql 语句进行修改。

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