package oss;

import com.alibaba.fastjson.annotation.JSONField;
import lombok.Data;

@Data
public class Config {
    @JSONField(name = "region")
    public String region;
    @JSONField(name = "bucketName")
    public String bucketName;
    @JSONField(name = "objectPath")
    public String objectPath;
    @JSONField(name = "targetPath")
    public String targetPath;
    @JSONField(name = "objectFmt")
    public String objectFmt;
}
