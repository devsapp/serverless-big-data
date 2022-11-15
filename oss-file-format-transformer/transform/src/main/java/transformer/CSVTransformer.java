package transformer;

import com.aliyun.fc.runtime.Context;
import com.opencsv.*;

import java.io.IOException;

public class CSVTransformer implements DataFmtTransformer {
    @Override
    public String Transform(Context context, String fileName, String outputFileName) throws IOException {
        return outputFileName;
    }
    @Override
    public String Name() {
        return "CSV";
    }
}