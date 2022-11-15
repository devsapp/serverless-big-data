package oss;

import com.alibaba.fastjson.JSONObject;
import com.alibaba.fastjson.JSON;
import com.aliyun.fc.runtime.Context;
import com.aliyun.fc.runtime.Credentials;
import com.aliyun.oss.OSS;
import com.aliyun.oss.OSSClientBuilder;
import com.aliyun.oss.model.*;
import com.aliyun.oss.OSSException;
import com.aliyun.oss.ClientException;
import transformer.*;

import java.io.*;

public class OssOperator  {
    private static volatile OssOperator ossOp;
    private static volatile OSS ossClient;
    private static volatile Config config;

    private static String tmpSourceFile = "/tmp/source";
    private static String tmpTargetFile = "/tmp/result.orc";

    private static transformer.DataFmtTransformer dataFmtTransformWriter;

    private OssOperator(Context context, Credentials creds) {
        String configStr = System.getenv("SINK_CONFIG");
        config = JSONObject.parseObject(configStr, Config.class);
        String ossEndpoint = String.format("https://oss-%s-internal.aliyuncs.com", config.getRegion());
        ossClient = new OSSClientBuilder().build(ossEndpoint, creds.getAccessKeyId(), creds.getAccessKeySecret(), creds.getSecurityToken());
        switch(config.getObjectFmt().toLowerCase()) {
            case "orc":
                context.getLogger().info(String.format("using data format: %s", "orc"));
                dataFmtTransformWriter = new ORCFmtTransformer();
                break;
            case "csv":
                context.getLogger().info(String.format("using data format: %s", "csv"));
                dataFmtTransformWriter = new CSVTransformer();
                break;
            case "json":
                context.getLogger().info(String.format("using data format: %s", "json"));
                dataFmtTransformWriter = new JsonFmtTransformer();
                break;
            case "avsc":
                context.getLogger().info(String.format("using data format: %s", "avsc"));
                dataFmtTransformWriter = new AVSCFmtTransformer();
                break;
            case "parquet":
                context.getLogger().info(String.format("using data format: %s", "parquet"));
                dataFmtTransformWriter = new ParquetFmtTransformer();
                break;
            default:
                context.getLogger().info(String.format("using data format: %s", "default"));
                dataFmtTransformWriter = new JsonFmtTransformer();
        }
        context.getLogger().info(String.format("inited x data format: %s", dataFmtTransformWriter.Name()));
    }

    public static OssOperator getOSSOperator(Context context) {
        if (ossOp == null) {
            synchronized (OssOperator.class) {
                if (ossOp == null) {
                    Credentials creds = context.getExecutionCredentials();
                    ossOp = new OssOperator(context, creds);
                }
            }
        }
        return ossOp;
    }

    public static void shutdown() {
        synchronized (OssOperator.class) {
            if (ossClient != null) {
                ossClient.shutdown();
            }
        }
    }

    private void downloadOSSFile (Context context) throws IOException, ClientException, OSSException {
        context.getLogger().info(String.format("now trying to get task origin data."));
        try {
            ossClient.getObject(new GetObjectRequest(config.getBucketName(), config.getObjectPath()), new File(tmpSourceFile));
        } catch (OSSException oe) {
            context.getLogger().info("Caught an OSSException, which means your request made it to OSS, "
                    + "but was rejected with an error response for some reason.");
            context.getLogger().info( String.format(UnRetryableException.OSSExceptionMessageFmt, oe.getRequestId(), oe.getErrorCode(), oe.getErrorMessage()));
            throw oe;
        } catch (ClientException ce) {
            context.getLogger().info("Caught an ClientException, which means the client encountered "
                    + "a serious internal problem while trying to communicate with OSS, "
                    + "such as not being able to access the network.");
            context.getLogger().info("Error Message:" + ce.getMessage());
            throw ce;
        }
        return;
    }

    private void uploadOSSFile (Context context) throws IOException, ClientException, OSSException {
        context.getLogger().info(String.format("now trying to upload result."));
        try {
            InputStream inputStream = new FileInputStream(tmpTargetFile);
            // 创建PutObject请求。
            ossClient.putObject(config.getBucketName(), config.getTargetPath(), inputStream);
        } catch (OSSException oe) {
            context.getLogger().info("Caught an OSSException, which means your request made it to OSS, "
                    + "but was rejected with an error response for some reason.");
            context.getLogger().info( String.format(UnRetryableException.OSSExceptionMessageFmt, oe.getRequestId(), oe.getErrorCode(), oe.getErrorMessage()));
            throw oe;
        } catch (ClientException ce) {
            context.getLogger().info("Caught an ClientException, which means the client encountered "
                    + "a serious internal problem while trying to communicate with OSS, "
                    + "such as not being able to access the network.");
            context.getLogger().info("Error Message:" + ce.getMessage());
            throw ce;
        }
        return;
    }

    public void startTask(Context context) throws IOException, ClientException, OSSException, UnRetryableException {
        // 1st, download oss file
        downloadOSSFile(context);
        // 2nd, transform the data.
        dataFmtTransformWriter.Transform(context, tmpSourceFile, tmpTargetFile);
        // 3rd, upload file.
        uploadOSSFile(context);
        return;
    }

}