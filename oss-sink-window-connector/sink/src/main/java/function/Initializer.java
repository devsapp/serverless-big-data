package function;

import com.alibaba.fastjson.JSONObject;
import com.aliyun.fc.runtime.Context;
import com.aliyun.fc.runtime.Credentials;
import com.aliyun.fc.runtime.FunctionInitializer;
import oss.OssOperator;

import java.io.IOException;

public class Initializer implements FunctionInitializer {
    @Override
    public void initialize(Context context) throws IOException {
        // 获取密钥信息，执行前，确保函数所在的服务配置了角色信息，并且角色需要拥有AliyunOSSFullAccess权限
        // 建议直接使用AliyunFCDefaultRole 角色
        // lazy init oss client
        OssOperator ossOP = OssOperator.getOSSOperator(context);
        context.getLogger().info("function instance initialized");
    }
}