package transformer;

import com.aliyun.fc.runtime.Context;
import java.io.IOException;

public interface DataFmtTransformer {
    public String Transform(Context context, String fileName, String outputFileName) throws IOException;
    public String Name();
}