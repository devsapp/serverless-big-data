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

import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Iterator;
import java.util.Map;

public class OssOperator  {
    private static volatile OssOperator ossOp;
    private static volatile OSS ossClient;
    private static volatile Config config;

    private static String lockFile = ".oss_file_lock";
    private static String metaFile = ".oss_meta_file";
    private static String lockAndMetaFileObjectFmt = "%s/%s/%s_partition_%d";
    private static String dataFileObjectFmt = "%s/%s/%s_partition_%d_num_%d";

    private OssOperator(Credentials creds) {
        String configStr = System.getenv("SINK_CONFIG");
        config = JSONObject.parseObject(configStr, Config.class);
        String ossEndpoint = String.format("https://oss-%s-internal.aliyuncs.com", config.getRegion());
        ossClient = new OSSClientBuilder().build(ossEndpoint, creds.getAccessKeyId(), creds.getAccessKeySecret(), creds.getSecurityToken());
    }

    public static OssOperator getOSSOperator(Context context) {
        if (ossOp == null) {
            synchronized (OssOperator.class) {
                if (ossOp == null) {
                    Credentials creds = context.getExecutionCredentials();
                    ossOp = new OssOperator(creds);
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

    public TaskInfo generateTaskParams()  {
        TaskInfo task = new TaskInfo();
        task.setPartition((int)(Math.random()*config.getConcurrency()));
        long currentTime=System.currentTimeMillis();
        Date date = new Date(currentTime);
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyyMMdd");
        task.setPath(dateFormat.format(date));
        return task;
    }

    public void getLock (Context context, TaskInfo taskParams) throws OSSException, InterruptedException {
        // todo: timer to reset the lock file after some times
        do {
            try {
                // object: bucketName/path/date/.lock_partition_x
                PutObjectRequest putObjectRequest = new PutObjectRequest(config.getBucketName(),
                        String.format(lockAndMetaFileObjectFmt, config.getObjectPath(),
                                taskParams.getPath(), lockFile, taskParams.getPartition()),
                        new ByteArrayInputStream(context.getRequestId().getBytes()));

                // 指定上传文件操作时是否覆盖同名Object。
                // 不指定x-oss-forbid-overwrite时，默认覆盖同名Object。
                // 指定x-oss-forbid-overwrite为false时，表示允许覆盖同名Object。
                // 指定x-oss-forbid-overwrite为true时，表示禁止覆盖同名Object，如果同名Object已存在，程序将报错。
                ObjectMetadata metadata = new ObjectMetadata();
                metadata.setHeader("x-oss-forbid-overwrite", "true");
                putObjectRequest.setMetadata(metadata);

                // 上传文件。
                ossClient.putObject(putObjectRequest);
            } catch (OSSException oe) {
                if (oe.getErrorCode() == "FileAlreadyExists") {
                    Thread.sleep(2000);
                    continue;
                }
                if (oe.getErrorCode() == "InvalidResponse") {
                    if (oe.getRawResponseError().contains("FileAlreadyExists")) {
                        context.getLogger().info("decode error 'FileAlreadyExists' from unrecognized response, now continue.");
                        Thread.sleep(2000);
                        continue;
                    }
                }
                context.getLogger().info("Caught an OSSException, which means your request made it to OSS, "
                        + "but was rejected with an error response for some reason.");
                context.getLogger().info(String.format(UnRetryableException.OSSExceptionMessageFmt, oe.getRequestId(), oe.getErrorCode(), oe.getErrorMessage()));
                throw oe;
            } catch (ClientException ce) {
                context.getLogger().error("Caught an ClientException, which means the client encountered "
                        + "a serious internal problem while trying to communicate with OSS, "
                        + "such as not being able to access the network.");
                context.getLogger().error("Error Message:" + ce.getMessage());
                Thread.sleep(3000);
                continue;
            }
            break;
        } while (true);
        context.getLogger().info(String.format("get lock for %s succeeded", context.getRequestId()));
    }

    public void tryReleaseLock(Context context, TaskInfo taskParams)  {
        try {
            context.getLogger().info(String.format("now start releasing lock for request: %s", context.getRequestId()));
            ossClient.deleteObject(config.getBucketName(),  String.format(lockAndMetaFileObjectFmt,
                    config.getObjectPath(), taskParams.getPath(), lockFile, taskParams.getPartition()));
        } catch (OSSException oe) {
            context.getLogger().error("Caught an OSSException, which means your request made it to OSS, "
                    + "but was rejected with an error response for some reason.");
            context.getLogger().error( String.format(UnRetryableException.OSSExceptionMessageFmt, oe.getRequestId(), oe.getErrorCode(), oe.getErrorMessage()));
            if (oe.getErrorCode() == "NoSuchKey") {
                return;
            }
            if (oe.getErrorCode() == "InvalidResponse") {
                if (oe.getRawResponseError().contains("NoSuchKey")) {
                    context.getLogger().info("decode error 'NoSuchKey' from unrecognized response, ignored.");
                    return;
                }
            }
            throw oe;
        } catch (ClientException ce) {
            context.getLogger().error("Caught an ClientException, which means the client encountered "
                    + "a serious internal problem while trying to communicate with OSS, "
                    + "such as not being able to access the network.");
            context.getLogger().error("Error Message:" + ce.getMessage());
            throw ce;
        }
    }

    private Meta getTaskMeta (Context context, TaskInfo taskParams) throws IOException, ClientException, OSSException {
        context.getLogger().info(String.format("now trying to get task meta."));
        Meta meta = new Meta();
        // ossObject包含文件所在的存储空间名称、文件名称、文件元信息以及一个输入流。
        try {
            OSSObject ossObject = ossClient.getObject(config.getBucketName(),  String.format(lockAndMetaFileObjectFmt,
                    config.getObjectPath(), taskParams.getPath(), metaFile, taskParams.getPartition()));

            // 读取文件内容。
            BufferedReader reader = new BufferedReader(new InputStreamReader(ossObject.getObjectContent()));
            while (true) {
                String line = reader.readLine();
                if (line == null) break;
                meta = JSONObject.parseObject(line, Meta.class);
            }
            // 数据读取完成后，获取的流必须关闭，否则会造成连接泄漏，导致请求无连接可用，程序无法正常工作。
            reader.close();
            // ossObject对象使用完毕后必须关闭，否则会造成连接泄漏，导致请求无连接可用，程序无法正常工作。
            ossObject.close();
        } catch (OSSException oe) {
            context.getLogger().info("Caught an OSSException, which means your request made it to OSS, "
                    + "but was rejected with an error response for some reason.");
            context.getLogger().info( String.format(UnRetryableException.OSSExceptionMessageFmt, oe.getRequestId(), oe.getErrorCode(), oe.getErrorMessage()));
            if (oe.getErrorCode() == "NoSuchKey") {
                return meta;
            }
            if (oe.getErrorCode() == "InvalidResponse") {
                if (oe.getRawResponseError().contains("NoSuchKey")) {
                    context.getLogger().info("decode error 'NoSuchKey' from unrecognized response, now continue.");
                    return meta;
                }
            }
            throw oe;
        } catch (ClientException ce) {
            context.getLogger().info("Caught an ClientException, which means the client encountered "
                    + "a serious internal problem while trying to communicate with OSS, "
                    + "such as not being able to access the network.");
            context.getLogger().info("Error Message:" + ce.getMessage());
            throw ce;
        }

        return meta;
    }

    private Meta createTaskMetaFile (Context context, TaskInfo taskParams, long currentDataFileID)
            throws ClientException, OSSException {
        context.getLogger().info(String.format("now trying to create task meta."));

        Meta meta = new Meta();
        meta.setCurrentFileID(currentDataFileID);
        meta.setNextAppendPosition(0L);
        meta.setCurrentFileSizeInByte(0);
        meta.setCurrentFileCreatedTime(System.currentTimeMillis());

        try {
            PutObjectRequest putObjectRequest = new PutObjectRequest(config.getBucketName(),
                    String.format(lockAndMetaFileObjectFmt, config.getObjectPath(), taskParams.getPath(),
                            metaFile, taskParams.getPartition()), new ByteArrayInputStream(meta.toString().getBytes()));

            // 指定上传文件操作时是否覆盖同名Object。
            // 不指定x-oss-forbid-overwrite时，默认覆盖同名Object。
            // 指定x-oss-forbid-overwrite为false时，表示允许覆盖同名Object。
            // 指定x-oss-forbid-overwrite为true时，表示禁止覆盖同名Object，如果同名Object已存在，程序将报错。
            ObjectMetadata metadata = new ObjectMetadata();
            metadata.setHeader("x-oss-forbid-overwrite", "true");
            putObjectRequest.setMetadata(metadata);

            // 上传文件。
            ossClient.putObject(putObjectRequest);
        } catch (OSSException oe) {
            context.getLogger().error("Caught an OSSException, which means your request made it to OSS, "
                    + "but was rejected with an error response for some reason.");
            context.getLogger().error( String.format(UnRetryableException.OSSExceptionMessageFmt, oe.getRequestId(), oe.getErrorCode(), oe.getErrorMessage()));
            if (oe.getErrorCode() == "FileAlreadyExists") {
                context.getLogger().fatal("create meta file failed, which means there is an concurrency creation");
            }
            throw oe;
        } catch (ClientException ce) {
            context.getLogger().error("Caught an ClientException, which means the client encountered "
                    + "a serious internal problem while trying to communicate with OSS, "
                    + "such as not being able to access the network.");
            context.getLogger().info("Error Message:" + ce.getMessage());
            throw ce;
        }
        return meta;
    }

    private Meta updateTaskMetaFile (Context context, TaskInfo taskParams, Meta meta) throws ClientException, OSSException {
        context.getLogger().info(String.format("now trying to update task meta."));
        try {
            // 不指定x-oss-forbid-overwrite时，默认覆盖同名Object。
            PutObjectRequest putObjectRequest = new PutObjectRequest(config.getBucketName(),
                    String.format(lockAndMetaFileObjectFmt, config.getObjectPath(), taskParams.getPath(), metaFile, taskParams.getPartition()),
                    new ByteArrayInputStream(JSON.toJSONString(meta).getBytes()));

            // 上传文件。
            ossClient.putObject(putObjectRequest);
        } catch (OSSException oe) {
            context.getLogger().info("Caught an OSSException, which means your request made it to OSS, "
                    + "but was rejected with an error response for some reason.");
            context.getLogger().error(String.format(UnRetryableException.OSSExceptionMessageFmt, oe.getRequestId(), oe.getErrorCode(), oe.getErrorMessage()));
            throw oe;
        } catch (ClientException ce) {
            context.getLogger().info("Caught an ClientException, which means the client encountered "
                    + "a serious internal problem while trying to communicate with OSS, "
                    + "such as not being able to access the network.");
            context.getLogger().info("Error Message:" + ce.getMessage());
            throw ce;
        }
        return meta;
    }

    public void startUploadAppendTask (Context context, TaskInfo taskParams, String payload) throws UnRetryableException {
        Meta meta = new Meta();
        // 1. get meta file
        try {
            meta = getTaskMeta(context, taskParams);
        } catch (Exception ex) {
            context.getLogger().fatal("get Exception while get meta file: " + ex.toString());
            throw new UnRetryableException(String.format("get task meta failed, task aborted: %s", ex.toString()));
        }
        if (meta.Empty()) {
            // if meta file is empty, it means this is a new task.
            context.getLogger().info("start new oss file upload task.");
            try {
                meta = createTaskMetaFile(context, taskParams, 0L);
            } catch (Exception e) {
                context.getLogger().fatal(String.format("failed to create meta file: %s", e.toString()));
                throw new UnRetryableException(String.format("failed to create meta file: %s", e.toString()));
            }
        }
        // 2. check if the file satisfied the window
        if (meta.getCurrentFileSizeInByte() >= config.getCacheSizeInMB() * 1024 * 1024 ||
                (System.currentTimeMillis() - meta.currentFileCreatedTime)/1000 > config.getCacheTimeWindowInSec()) {
            // new file
            context.getLogger().info(String.format("append to new data file, current data file in Byte: %d, %d, %d, %d",
                    meta.getCurrentFileSizeInByte(), config.getCacheSizeInMB() *1024 *1024, (System.currentTimeMillis() -
                            meta.currentFileCreatedTime)/1000, config.getCacheTimeWindowInSec()));

            meta.setCurrentFileID(meta.getCurrentFileID() + 1);
            meta.setCurrentFileCreatedTime(System.currentTimeMillis());
            meta.setNextAppendPosition(0L);
            meta.setCurrentFileSizeInByte(0L);
        }
        // 3. start append oss file
        long nextPosition;
        try {
            nextPosition = appendFile(context, taskParams, meta, payload);
        } catch (Exception e) {
            context.getLogger().fatal(String.format("failed to append file: %s", e.toString()));
            throw new UnRetryableException(String.format("failed to append file: %s", e.toString()));
        }
        // 4. update meta
        meta.setNextAppendPosition(nextPosition);
        context.getLogger().info(String.format("calculated file length: %d, next position: %d",
                meta.getCurrentFileSizeInByte() + payload.length(), nextPosition));
        meta.setCurrentFileSizeInByte(nextPosition);
        try {
            updateTaskMetaFile(context, taskParams, meta);
        } catch (Exception e) {
            context.getLogger().fatal(String.format("failed to update meta file: %s", e.toString()));
            throw new UnRetryableException(String.format("failed to update meta file: %s", e.toString()));
        }
    }

    private long appendFile(Context context, TaskInfo taskParams, Meta taskMeta, String data)
            throws ClientException, OSSException {
        context.getLogger().info(String.format("now trying to append data to file."));
        boolean needRetry;
        long nextPosition = 0L;
        String dataFileName = String.format(dataFileObjectFmt, config.getObjectPath(),
                taskParams.getPath(), config.getObjectPrefix(), taskParams.getPartition(), taskMeta.currentFileID);
        do {
            needRetry = false;
            try {
                ObjectMetadata meta = new ObjectMetadata();
                // 指定上传的内容类型。
                meta.setContentType("text/plain");
                // 指定该Object被下载时的名称。
                meta.setContentDisposition(String.format("attachment;filename=%s", dataFileName));
                // 指定该Object的内容编码格式。
                //meta.setContentEncoding(OSSConstants.DEFAULT_CHARSET_NAME);
                // 该请求头用于检查消息内容是否与发送时一致。
                //meta.setContentMD5("ohhnqLBJFiKkPSBO1eNaUA==");
                // 指定过期时间。
                //try {
                //    meta.setExpirationTime(DateUtil.parseRfc822Date("Wed, 08 Jul 2022 16:57:01 GMT"));
                //} catch (ParseException e) {
                //    e.printStackTrace();
                //}
                // 指定服务器端加密方式。此处指定为OSS完全托管密钥进行加密（SSE-OSS）。
                //meta.setServerSideEncryption(ObjectMetadata.AES_256_SERVER_SIDE_ENCRYPTION);
                // 指定Object的访问权限。此处指定为私有访问权限。
                meta.setObjectAcl(CannedAccessControlList.Private);
                // 指定Object的存储类型。
                //meta.setHeader(OSSHeaders.OSS_STORAGE_CLASS, StorageClass.Standard);
                // 创建AppendObject时可以添加x-oss-meta-*，继续追加时不可以携带此参数。如果配置以x-oss-meta-*为前缀的参数，则该参数视为元数据。
                //meta.setHeader("x-oss-meta-author", "Alice");

                // 通过AppendObjectRequest设置多个参数。
                AppendObjectRequest appendObjectRequest = new AppendObjectRequest(config.getBucketName(), dataFileName, new ByteArrayInputStream(data.getBytes()),meta);

                // 通过AppendObjectRequest设置单个参数。
                // 设置Bucket名称。
                //appendObjectRequest.setBucketName(bucketName);
                // 设置Object名称。
                //appendObjectRequest.setKey(objectName);
                // 设置待追加的内容。可选类型包括InputStream类型和File类型。此处为InputStream类型。
                //appendObjectRequest.setInputStream(new ByteArrayInputStream(content1.getBytes()));
                // 设置待追加的内容。可选类型包括InputStream类型和File类型。此处为File类型。
                //appendObjectRequest.setFile(new File("D:\\localpath\\examplefile.txt"));
                // 指定文件的元信息，第一次追加时有效。
                //appendObjectRequest.setMetadata(meta);

                // 设置文件的追加位置。
                appendObjectRequest.setPosition(taskMeta.nextAppendPosition);
                AppendObjectResult appendObjectResult = ossClient.appendObject(appendObjectRequest);
                nextPosition = appendObjectResult.getNextPosition();
            } catch (OSSException oe) {
                context.getLogger().info("Caught an OSSException, which means your request made it to OSS, "
                        + "but was rejected with an error response for some reason.");
                context.getLogger().error(String.format(UnRetryableException.OSSExceptionMessageFmt, oe.getRequestId(), oe.getErrorCode(), oe.getErrorMessage()));
                if (oe.getErrorCode() == "PositionNotEqualToLength") {
                    taskMeta.setNextAppendPosition(getObjectNextPosition(context, dataFileName));
                    needRetry = true;
                    continue;
                }
                if (oe.getErrorCode() == "InvalidResponse") {
                    if (oe.getRawResponseError().contains("PositionNotEqualToLength")) {
                        context.getLogger().info("decode error 'PositionNotEqualToLength' from unrecognized response, now retry.");
                        taskMeta.setNextAppendPosition(getObjectNextPosition(context, dataFileName));
                        needRetry = true;
                        continue;
                    }
                }
                throw oe;
            } catch (ClientException ce) {
                context.getLogger().info("Caught an ClientException, which means the client encountered "
                        + "a serious internal problem while trying to communicate with OSS, "
                        + "such as not being able to access the network.");
                context.getLogger().info("Error Message:" + ce.getMessage());
                throw ce;
            }
        } while (needRetry);

        return nextPosition;
    }

    private long getObjectNextPosition(Context context, String fileName) {
        context.getLogger().info("now re-get the object header");

        HeadObjectRequest req = new HeadObjectRequest(config.getBucketName(), fileName);
        ObjectMetadata obj = ossClient.headObject(req);
        // print the object data
        Iterator<Map.Entry<String, Object>> entries = obj.getRawMetadata().entrySet().iterator();
        while (entries.hasNext()) {
            Map.Entry<String, Object> entry = entries.next();
            context.getLogger().info("Key = " + entry.getKey() + ", Value = " + entry.getValue());
        }
        return Long.parseLong(String.valueOf(obj.getRawMetadata().get("x-oss-next-append-position")));
    }
}