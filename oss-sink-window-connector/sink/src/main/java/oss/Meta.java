package oss;

import com.alibaba.fastjson.annotation.JSONField;
import lombok.Data;

@Data
public class Meta {
    @JSONField(name = "nextAppendPosition")
    public long nextAppendPosition;
    @JSONField(name = "currentFileID")
    public long currentFileID;
    @JSONField(name = "currentFileCreatedTime")
    public long currentFileCreatedTime;
    @JSONField(name = "currentFileSizeInByte")
    public long currentFileSizeInByte;

    public boolean Empty() {
        return (nextAppendPosition == 0 && currentFileCreatedTime == 0 && currentFileSizeInByte == 0 && currentFileID == 0);
    }
}