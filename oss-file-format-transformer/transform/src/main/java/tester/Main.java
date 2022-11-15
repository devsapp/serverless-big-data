package tester;

import com.alibaba.fastjson.JSONObject;
import org.eclipse.microprofile.faulttolerance.Retry;
import oss.Config;
import com.opencsv.*;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.logging.Logger;

public class Main {
    // retry policy: https://download.eclipse.org/microprofile/microprofile-fault-tolerance-1.1.2/microprofile-fault-tolerance-spec.html#_retry_usage
    public static void main(String[] args) {
        String confStr = "{\"region\":\"cn-hangzhou\", \"concurrency\":\"16\", \"cacheSizeInMB\": \"128\",\"cacheTimeWindowInSec\": \"300\",\"bucketName\": \"sdk\",\"objectPath\": \"file\",\"objectPrefix\": \"file\", \"objectShardingPath\":\"YYYYMMdd/HH\"}";
        Config config = JSONObject.parseObject(confStr, Config.class);
        Logger logger = Logger.getGlobal();
        logger.info(config.getRegion());

        long currentTime=System.currentTimeMillis();
        Date date = new Date(currentTime);
        SimpleDateFormat dateFormat = new SimpleDateFormat("YYMMDDHH");
        logger.info(dateFormat.format(date));

        try {
            retry();
        } catch (Exception xx) {

        }
    }

    @Retry(retryOn = {Exception.class})
    private static void retry() throws Exception {
        Logger logger = Logger.getGlobal();
        logger.info("in retry function");
        throw new Exception("hahaha");
    }

}