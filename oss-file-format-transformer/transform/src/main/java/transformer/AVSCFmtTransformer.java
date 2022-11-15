package transformer;

import com.aliyun.fc.runtime.Context;
import java.io.IOException;

public class AVSCFmtTransformer implements DataFmtTransformer {
    @Override
    public String Transform(Context context, String fileName, String outputFileName) throws IOException {
        return outputFileName;
    }

    @Override
    public String Name() {
        return "AVS";
    }
}