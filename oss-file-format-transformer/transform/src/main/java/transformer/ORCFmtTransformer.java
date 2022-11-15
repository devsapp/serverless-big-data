package transformer;

import com.aliyun.fc.runtime.Context;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.hive.ql.exec.vector.BytesColumnVector;
import org.apache.hadoop.hive.ql.exec.vector.LongColumnVector;
import org.apache.hadoop.hive.ql.exec.vector.VectorizedRowBatch;
import org.apache.orc.CompressionKind;
import org.apache.orc.OrcFile;
import org.apache.orc.TypeDescription;
import org.apache.orc.Writer;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;

public class ORCFmtTransformer implements DataFmtTransformer{
    @Override
    public String Transform(Context context, String fileName, String outputFileName) throws IOException {
        Configuration conf = new Configuration();
        conf.set("fs.hdfs.impl", org.apache.hadoop.hdfs.DistributedFileSystem.class.getName());
        conf.set("fs.file.impl", org.apache.hadoop.fs.LocalFileSystem.class.getName());
        //确定每一列的数据类型
        TypeDescription schema = TypeDescription.createStruct()
                .addField("x",TypeDescription.createInt())
                .addField("y",TypeDescription.createString());

        //设置写入流时的参数，
        Writer writer = OrcFile.createWriter(new Path(outputFileName),OrcFile.writerOptions(conf)
                .setSchema(schema)
                .stripeSize(67108864)
                .bufferSize(64*1024)
                .blockSize(128*1024*1024)
                .rowIndexStride(10000)
                .blockPadding(true)
                //默认压缩算法为zlib,zlib相对于snappy压缩算法，压缩比更低，压缩效果更好，但是花费了更多的压缩时间
                .compress(CompressionKind.ZLIB));

//        TypeDescription schema = TypeDescription.fromString("struct<x:int,y:string>");
//        Writer writer = OrcFile.createWriter(new Path(outputFileName),
//                OrcFile.writerOptions(conf)
//                        .setSchema(schema));

        File file = new File(fileName);
        BufferedReader reader = null;
        reader = new BufferedReader(new FileReader(file));
        VectorizedRowBatch batch = schema.createRowBatch();
        //获取每一列的引用
        LongColumnVector x = (LongColumnVector) batch.cols[0];
        BytesColumnVector y = (BytesColumnVector) batch.cols[1];
        String tempString = null;
        //测试转换时间
        long start = System.currentTimeMillis();

        //开始转换成二进制的orc文件
        while ((tempString = reader.readLine())!=null){
            int row = batch.size++;
            String[] contents = tempString.split(" ");
            //int,double,long等数据类型用  引用.vector
            x.vector[row] = Integer.parseInt(contents[0]);
            //String等数据类型用 引用.setVal
            y.setVal(row,contents[1].getBytes());
            writer.addRowBatch(batch);
            batch.reset();
        }
        long stop = System.currentTimeMillis();
        System.out.println("将text文件转换为orc文件花费的时间是 "+(stop-start)/1000+"秒");

        writer.close();

        return outputFileName;
    }
    @Override
    public String Name() {
        return "ORC";
    }
}




