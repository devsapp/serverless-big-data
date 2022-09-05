package oss;
import lombok.Data;

@Data
public class TaskInfo {
    private int partition;
    private String path;

    public String str() {
        return String.format("partition:%d, path:%s", partition, path);
    }
}