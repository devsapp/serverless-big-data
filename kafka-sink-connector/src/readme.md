
> 注：当前项目为 Serverless Devs 应用，由于应用中会存在需要初始化才可运行的变量（例如应用部署地区、函数名等等），所以**不推荐**直接 Clone 本仓库到本地进行部署或直接复制 s.yaml 使用，**强烈推荐**通过 `s init ${模版名称}` 的方法或应用中心进行初始化，详情可参考[部署 & 体验](#部署--体验) 。

# kafka-sink-connector-v3 帮助文档
<p align="center" class="flex justify-center">
    <a href="https://www.serverless-devs.com" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=kafka-sink-connector-v3&type=packageType">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=kafka-sink-connector-v3" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=kafka-sink-connector-v3&type=packageVersion">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=kafka-sink-connector-v3" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=kafka-sink-connector-v3&type=packageDownload">
  </a>
</p>

<description>

基于函数计算实现的 kafka proxy，通过 SDK Invoke Function 的方式将消息传递至 Kafka 特定 Topic

</description>

<codeUrl>



</codeUrl>
<preview>



</preview>


## 前期准备

使用该项目，您需要有开通以下服务并拥有对应权限：

<service>



| 服务/业务 |  权限  | 相关文档 |
| --- |  --- | --- |
| 函数计算 |  AliyunFCFullAccess,AliyunLogFullAccess,AliyunVPCReadOnlyAccess | [帮助文档](https://help.aliyun.com/product/2508973.html) [计费文档](https://help.aliyun.com/document_detail/2512928.html) |

</service>

<remark>



</remark>

<disclaimers>



</disclaimers>

## 部署 & 体验

<appcenter>
   
- :fire: 通过 [Serverless 应用中心](https://fcnext.console.aliyun.com/applications/create?template=kafka-sink-connector-v3) ，
  [![Deploy with Severless Devs](https://img.alicdn.com/imgextra/i1/O1CN01w5RFbX1v45s8TIXPz_!!6000000006118-55-tps-95-28.svg)](https://fcnext.console.aliyun.com/applications/create?template=kafka-sink-connector-v3) 该应用。
   
</appcenter>
<deploy>
    
- 通过 [Serverless Devs Cli](https://www.serverless-devs.com/serverless-devs/install) 进行部署：
  - [安装 Serverless Devs Cli 开发者工具](https://www.serverless-devs.com/serverless-devs/install) ，并进行[授权信息配置](https://docs.serverless-devs.com/fc/config) ；
  - 初始化项目：`s init kafka-sink-connector-v3 -d kafka-sink-connector-v3`
  - 进入项目，并进行项目部署：`cd kafka-sink-connector-v3 && s deploy -y`
   
</deploy>

## 案例介绍

<appdetail id="flushContent">

基于函数计算实现的 kafka proxy，通过 SDK Invoke Function 的方式将消息传递至 Kafka 特定 Topic。

本应用可以将您的原始输入数据进过预处理之后，传输到您的 kafka topic 中。如果您需要对数据进行转换，可以编写代码中的 transform 函数。

</appdetail>

## 使用流程

<usedetail id="flushContent">

### 资源准备
创建一个 Kafka 实例，并在实例下创建一个 topic。

### 应用测试
 
1. 按照提示填写参数。

|参数|含义|
|----|----|
|functionName|函数名称|
|bootstrapServers|kafka bootstrapServers, 可以从 kafka 控制台获取|
|topicName|kafka topic 名称|
|vpcId|kafka 实例所在 vpc id|
|vswitchIds|kafka 实例所在 vswitchId|
|securityGroupId|vpc 下安全组 id，用于内网访问 kafka|

2. 成功部署应用。
3. 进入函数页面，点击测试函数，如下图返回 true response 则表示请求成功。
![](http://image.editor.devsapp.cn/BS2av6DGSuFggCyGwSjh4biiz7vvtbAwykZSgbrkE46eEycrle/k6GxvkAC2Zjdg9fuCiCb.png)

### 结果验证

登陆到 [kafka 控制台](https://kafka.console.aliyun.com/) 查看目标 topic 中是否已经写入测试数据。



</usedetail>

## 注意事项

<matters id="flushContent">
</matters>


<devgroup>


## 开发者社区

您如果有关于错误的反馈或者未来的期待，您可以在 [Serverless Devs repo Issues](https://github.com/serverless-devs/serverless-devs/issues) 中进行反馈和交流。如果您想要加入我们的讨论组或者了解 FC 组件的最新动态，您可以通过以下渠道进行：

<p align="center">  

| <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407298906_20211028074819117230.png" width="130px" > | <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407044136_20211028074404326599.png" width="130px" > | <img src="https://serverless-article-picture.oss-cn-hangzhou.aliyuncs.com/1635407252200_20211028074732517533.png" width="130px" > |
| --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| <center>微信公众号：`serverless`</center>                                                                                         | <center>微信小助手：`xiaojiangwh`</center>                                                                                        | <center>钉钉交流群：`33947367`</center>                                                                                           |
</p>
</devgroup>
