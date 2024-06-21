
> 注：当前项目为 Serverless Devs 应用，由于应用中会存在需要初始化才可运行的变量（例如应用部署地区、函数名等等），所以**不推荐**直接 Clone 本仓库到本地进行部署或直接复制 s.yaml 使用，**强烈推荐**通过 `s init ${模版名称}` 的方法或应用中心进行初始化，详情可参考[部署 & 体验](#部署--体验) 。

# sls-to-splunk-service-sink-connector-v3 帮助文档
<p align="center" class="flex justify-center">
    <a href="https://www.serverless-devs.com" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=sls-to-splunk-service-sink-connector-v3&type=packageType">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=sls-to-splunk-service-sink-connector-v3" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=sls-to-splunk-service-sink-connector-v3&type=packageVersion">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=sls-to-splunk-service-sink-connector-v3" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=sls-to-splunk-service-sink-connector-v3&type=packageDownload">
  </a>
</p>

<description>

使用函数计算将 SLS 日志投递至 Splunk 目标服务。

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
| 函数计算 |  AliyunLogFullAccess | [帮助文档](https://help.aliyun.com/product/2508973.html) [计费文档](https://help.aliyun.com/document_detail/2512928.html) |

</service>

<remark>



</remark>

<disclaimers>



</disclaimers>

## 部署 & 体验

<appcenter>
   
- :fire: 通过 [Serverless 应用中心](https://fcnext.console.aliyun.com/applications/create?template=sls-to-splunk-service-sink-connector-v3) ，
  [![Deploy with Severless Devs](https://img.alicdn.com/imgextra/i1/O1CN01w5RFbX1v45s8TIXPz_!!6000000006118-55-tps-95-28.svg)](https://fcnext.console.aliyun.com/applications/create?template=sls-to-splunk-service-sink-connector-v3) 该应用。
   
</appcenter>
<deploy>
    
- 通过 [Serverless Devs Cli](https://www.serverless-devs.com/serverless-devs/install) 进行部署：
  - [安装 Serverless Devs Cli 开发者工具](https://www.serverless-devs.com/serverless-devs/install) ，并进行[授权信息配置](https://docs.serverless-devs.com/fc/config) ；
  - 初始化项目：`s init sls-to-splunk-service-sink-connector-v3 -d sls-to-splunk-service-sink-connector-v3`
  - 进入项目，并进行项目部署：`cd sls-to-splunk-service-sink-connector-v3 && s deploy -y`
   
</deploy>

## 案例介绍

<appdetail id="flushContent">

基于函数计算+SLS触发器实现，将 SLS 日志通过 http 协议投递至 Splunk 目标服务。

本应用可以将您的原始输入数据固定格式化并投递到目标服务，如格式不满足需求可改写代码自定义实现格式化需求。

使用 Serverless 开发平台实现，您只需专注于业务逻辑的开发和创新，无需过多关注底层基础设施的管理和运维，平台会以弹性伸缩、高可靠性、按量付费、低延迟的方式托管运行您的业务。

</appdetail>

## 使用流程

<usedetail id="flushContent">

### 资源准备
1. 创建一个 SLS project，在 project 下创建两个 logstore：1）一个做为触发源 logstore；2）另一个用于记录函数运行日志；
2. 注册并配置 Splunk，[Splunk 官网](https://www.splunk.com/)

### 应用测试
 
1. 按照提示填写参数。

|参数|含义|
|----|----|
|region|创建应用所在的地区|
|functionName|函数名称|
|functionRoleArn|函数所使用的角色 ARN，从而使函数可以获得角色所拥有的权限，此角色需至少包含 sls 服务的读权限或 GetCursorOrData 操作权限。(注意：在 RAM 控制台创建服务所使用的角色时，需要选择“阿里云服务”，并且“受信服务”需要选择“函数计算”。)|
|splunkHTTPHost|Splunk HEC host（数据接收端）|
|splunkHTTPPort|Splunk HEC port（数据接收端）|
|splunkHTTPToken|Splunk HEC token（数据接收端）|
|splunkEnableHTTPS|Splunk HEC 是否开启了 HTTPS|
|splunkHTTPTimeout|Splunk HEC 的超时时间|
|splunkEnableSSLVerify|Splunk HEC 是否开启 SSL Verfify 验证|
|splunkSourceType|Splunk SourceType|
|splunkIndex|Splunk Index|
|splunkSource|Splunk Source|

 如下图示例：
![](https://img.alicdn.com/imgextra/i1/O1CN01TQCMez1OFelT1lfd6_!!6000000001676-0-tps-1704-589.jpg)

2.成功部署应用，跳转到 FC 函数页面，如下图：
![](https://img.alicdn.com/imgextra/i1/O1CN01Cv7PaO1KBIX6Fs69N_!!6000000001125-0-tps-1116-1015.jpg)

3.手动创建 SLS 触发器，参数如下，更多信息可阅读[官方文档](https://help.aliyun.com/zh/fc/configure-a-log-service-trigger?spm=a2c4g.11186623.0.0.7af17ffckK0BBG#section-pz6-4oj-c28) ：

|参数|含义|
|----|----|
|触发器类型|SLS 触发器|
|名称|sls 触发器名称|
|版本或别名|指定的函数版本或别名|
|日志库项目|触发源 logstore 所在的 project|
|日志库|触发源 logstore 名称|
|触发间隔|日志服务触发函数运行的间隔，比如每隔 120 秒将 logstore 在最近 120 秒内的数据取出到函数服务，以执行自定义计算。|
|重试次数|取值范围为 0～100。日志服务根据触发间隔每次触发函数执行时，如果遇到错误（例如权限不足、网络失败、函数执行异常返回等），该参数定义本次触发所允许的最大重试次数。对于本次触发，若最大重试次数耗尽，那么会切换到退避重试的方式持续对函数进行调用，直到函数执行成功。|
|触发器日志| 触发函数运行过程中发生的异常和函数执行统计信息会记录到该 Logstore|
|调用参数| 如果您想传入自定义参数，可以在此处配置。该参数将作为event的parameter参数传入函数。该参数取值必须是JSON格式的字符串。默认值为空。|
|角色名称| 选择AliyunLogETLRole。如果您第一次创建该类型的触发器，则需要在单击确定后，在弹出的对话框中选择立即授权。|

![](https://img.alicdn.com/imgextra/i4/O1CN01ztWiov1ZIMspzuXEb_!!6000000003171-0-tps-1745-1106.jpg)


4. 部署成功后向触发器配置的日志库发送日志，如下图：
![](https://img.alicdn.com/imgextra/i3/O1CN01zlmEri1JdrcU6aY1F_!!6000000001052-0-tps-951-373.jpg)


### 结果验证

在目标 Splunk 服务中查询日志文件判断 sls 日志通过 FC 投递到目标服务成功。

</usedetail>

## 注意事项

<matters id="flushContent">

1. 部署应用时，请确保角色包含 AliyunFCFullAccess 和 AliyunLogFullAccess 权限。
![](https://img.alicdn.com/imgextra/i3/O1CN01bJb2xn1GWaTowEPIy_!!6000000000630-0-tps-1445-592.jpg)
2. 应用模板仅供功能验证使用，平台不保证应用模板 SLA。用户需根据个人需求完善模版，保证性能、可用性和定制化功能等需求。

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