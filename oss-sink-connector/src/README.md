
> 注：当前项目为 Serverless Devs 应用，由于应用中会存在需要初始化才可运行的变量（例如应用部署地区、函数名等等），所以**不推荐**直接 Clone 本仓库到本地进行部署或直接复制 s.yaml 使用，**强烈推荐**通过 `s init ${模版名称}` 的方法或应用中心进行初始化，详情可参考[部署 & 体验](#部署--体验) 。

# oss-sink-connector-v3 帮助文档
<p align="center" class="flex justify-center">
    <a href="https://www.serverless-devs.com" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=oss-sink-connector-v3&type=packageType">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=oss-sink-connector-v3" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=oss-sink-connector-v3&type=packageVersion">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=oss-sink-connector-v3" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=oss-sink-connector-v3&type=packageDownload">
  </a>
</p>

<description>

OSS Sink Connector

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
| 函数计算 |  AliyunFCFullAccess,AliyunOSSFullAccess | [帮助文档](https://help.aliyun.com/product/2508973.html) [计费文档](https://help.aliyun.com/document_detail/2512928.html) |

</service>

<remark>



</remark>

<disclaimers>



</disclaimers>

## 部署 & 体验

<appcenter>
   
- :fire: 通过 [Serverless 应用中心](https://fcnext.console.aliyun.com/applications/create?template=oss-sink-connector-v3) ，
  [![Deploy with Severless Devs](https://img.alicdn.com/imgextra/i1/O1CN01w5RFbX1v45s8TIXPz_!!6000000006118-55-tps-95-28.svg)](https://fcnext.console.aliyun.com/applications/create?template=oss-sink-connector-v3) 该应用。
   
</appcenter>
<deploy>
    
- 通过 [Serverless Devs Cli](https://www.serverless-devs.com/serverless-devs/install) 进行部署：
  - [安装 Serverless Devs Cli 开发者工具](https://www.serverless-devs.com/serverless-devs/install) ，并进行[授权信息配置](https://docs.serverless-devs.com/fc/config) ；
  - 初始化项目：`s init oss-sink-connector-v3 -d oss-sink-connector-v3`
  - 进入项目，并进行项目部署：`cd oss-sink-connector-v3 && s deploy -y`
   
</deploy>

## 案例介绍

<appdetail id="flushContent">

本应用可以将您的原始输入数据写入到您创建应用时填写的 OSS bucket 中，如果您需要对数据进行转换，可以编写应用创建后的 transform 函数。否则只需调用 sink 函数即可。

使用 Serverless 函数计算实现  oss proxy，您只需专注于业务逻辑的开发和创新，无需过多关注底层基础设施的管理和运维，平台会以弹性伸缩、高可靠性、按量付费、低延迟的方式托管运行您的业务。



</appdetail>

## 使用流程

<usedetail id="flushContent">

### 资源准备

开通 oss 服务，并创建一个 oss bucket。


### 应用测试

1. 按照提示填写参数。

|参数|含义|
|----|----|
|region|创建应用所在的地区|
|functionName|函数名称|
|serviceRoleARN|配置服务中函数所使用的角色 ARN，从而使函数可以获得角色所拥有的权限，此角色需至少包含 AliyunOSSFullAccess 权限。|
|endpoint|OSS访问域名|
|bucket|目标存储 bucket 名称|
|object_prefix|目标存储 object前缀名|

2. 成功部署应用后，通过函数资源信息跳转到函数页面，如下图。
![](https://img.alicdn.com/imgextra/i4/O1CN01X5NF6A218ZdZi6YwM_!!6000000006940-0-tps-1072-952.jpg)
3. 在函数页面中，点击测试函数，可直接使用控制台提供的默认 event 值测试。
![](https://img.alicdn.com/imgextra/i1/O1CN013ZM3ii1NU1YXzZRdT_!!6000000001572-0-tps-913-820.jpg)
### 结果验证
登陆到 [oss 控制台](https://oss.console.aliyun.com/) 查看测试数据是否成功写入目标 oss bucket。

</usedetail>

## 注意事项

<matters id="flushContent">

可通过不同网络访问 oss 实例，有如下三种网络访问方式：
1经典网络访问：通过阿里云内网进行访问，不会产生公网流量，同时安全性也高于公网访问。
2.公网访问：函数环境变量中的 endpoint 为公网访问地址时，需要 oss 开启“公网访问”能力，同时会产生公网流量。
3.vpc 访问：通过 vpc 网络进行访问，不会产生公网流量，需要为 sink 函数配置 vpc

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
