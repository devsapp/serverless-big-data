package function;

import com.aliyun.fc.runtime.Context;
import com.aliyun.fc.runtime.PreStopHandler;
import oss.OssOperator;

import java.io.IOException;

public class PreStopH implements PreStopHandler {

    @Override
    public void preStop(Context context) throws IOException {
        OssOperator.shutdown();
        context.getLogger().info("function instance doing preStop");
    }
}

