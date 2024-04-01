
> 注：当前项目为 Serverless Devs 应用，由于应用中会存在需要初始化才可运行的变量（例如应用部署地区、函数名等等），所以**不推荐**直接 Clone 本仓库到本地进行部署或直接复制 s.yaml 使用，**强烈推荐**通过 `s init ${模版名称}` 的方法或应用中心进行初始化，详情可参考[部署 & 体验](#部署--体验) 。

# mysql-sink-connector-v3 帮助文档
<p align="center" class="flex justify-center">
    <a href="https://www.serverless-devs.com" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=mysql-sink-connector-v3&type=packageType">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=mysql-sink-connector-v3" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=mysql-sink-connector-v3&type=packageVersion">
  </a>
  <a href="http://www.devsapp.cn/details.html?name=mysql-sink-connector-v3" class="ml-1">
    <img src="http://editor.devsapp.cn/icon?package=mysql-sink-connector-v3&type=packageDownload">
  </a>
</p>

<description>

Sink Connector for MySQL

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
| 函数计算 |  AliyunFCFullAccess | [帮助文档](https://help.aliyun.com/product/2508973.html) [计费文档](https://help.aliyun.com/document_detail/2512928.html) |

</service>

<remark>



</remark>

<disclaimers>



</disclaimers>

## 部署 & 体验

<appcenter>
   
- :fire: 通过 [Serverless 应用中心](https://fcnext.console.aliyun.com/applications/create?template=mysql-sink-connector-v3) ，
  [![Deploy with Severless Devs](https://img.alicdn.com/imgextra/i1/O1CN01w5RFbX1v45s8TIXPz_!!6000000006118-55-tps-95-28.svg)](https://fcnext.console.aliyun.com/applications/create?template=mysql-sink-connector-v3) 该应用。
   
</appcenter>
<deploy>
    
- 通过 [Serverless Devs Cli](https://www.serverless-devs.com/serverless-devs/install) 进行部署：
  - [安装 Serverless Devs Cli 开发者工具](https://www.serverless-devs.com/serverless-devs/install) ，并进行[授权信息配置](https://docs.serverless-devs.com/fc/config) ；
  - 初始化项目：`s init mysql-sink-connector-v3 -d mysql-sink-connector-v3`
  - 进入项目，并进行项目部署：`cd mysql-sink-connector-v3 && s deploy -y`
   
</deploy>

## 案例介绍

<appdetail id="flushContent">

本应用可以将您的原始输入数据写入到您创建应用时填写的 MySQL Table 中，如果您需要对数据进行转换，可以在函数中对 event 输入数据做加工处理。

使用 Serverless 函数计算实现 mysql proxy，您只需专注于业务逻辑的开发和创新，无需过多关注底层基础设施的管理和运维，平台会以弹性伸缩、高可靠性、按量付费、低延迟的方式托管运行您的业务。



</appdetail>

## 使用流程

<usedetail id="flushContent">

### 资源准备
1. 开通阿里云 RDS MySQL 服务，并创建一个 MySQL 实例，详见[文档](https://help.aliyun.com/zh/rds/apsaradb-rds-for-mysql/create-an-apsaradb-rds-for-mysql-instance) 。
2. 在 MySQL 实例下创建一个数据库和账号，账号需拥有对数据库的操作权限，详见[文档](https://help.aliyun.com/zh/rds/apsaradb-rds-for-mysql/create-databases-and-accounts-for-an-apsaradb-rds-for-mysql-instance) 。
3. 此应用要求预先创建 Table 表，可在数据库中执行以下 sql，创建固定格式的 table。
```
CREATE Table Data (
      id BIGINT,
      data TEXT(256)
)
```

### 应用测试

1. 按照提示填写参数。

|参数|含义|
|----|----|
|region|创建应用所在的地区|
|functionName|函数名称|
|host|数据库连接地址，请填写公网地址|
|port|mysql 数据库端口号|
|user|mysql 数据库登录用户名|
|password|mysql 数据库登录密码|
|database|mysql 数据库库名|

2. 成功部署应用后，通过函数资源信息跳转到函数页面，如下图。
![](https://img.alicdn.com/imgextra/i3/O1CN01mLSxbh22Ah5aI8pRw_!!6000000007080-0-tps-1119-989.jpg)
3. 在函数页面中，点击配置测试参数，可将下面 demo 复制粘贴到控制台。
```
{
    "data": "testData",
    "id": 1
}
```
![](https://img.alicdn.com/imgextra/i3/O1CN01TxRJa71QKoRKMXyrI_!!6000000001958-0-tps-1641-787.jpg)

4. 点击测试函数，完成测试。

### 结果验证
登陆到 [DMS 控制台](https://dms.aliyun.com/) 查看测试数据是否成功写入目标 mysql table，如下图。
![](https://img.alicdn.com/imgextra/i2/O1CN013lWPPl1HHIrZkXqYy_!!6000000000732-0-tps-1198-814.jpg)




</usedetail>

## 注意事项

<matters id="flushContent">

1. 本应用默认使用的是公网连接 mysql 实例，在实际使用中需要考虑安全问题，因此建议您使用 VPC 连接 mysql 实例。具体参考：https://help.aliyun.com/document_detail/147916.html。
2. 应用模板内参数中的 user 以及 password 均为敏感信息，请注意信息安全。

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
