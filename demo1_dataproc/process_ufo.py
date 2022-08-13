from pyspark.sql import SparkSession
from pyspark.sql.functions import split

def read_data(spark):
    # อ่านไฟล์จาก GCS
    # TODO: เปลี่ยนเป็นชื่อ GCS ของคุณ
    ufo_df = spark.read.option('header', True).option("multiline", True).csv('gs://perth-test-storage/Workshop1_Data.csv')

    # แบ่งคอลัมน์ 'Date / Time' ออกเป็นคอลัมน์ Date และ Time
    # Reference: https://spark.apache.org/docs/3.1.1/api/python/reference/api/pyspark.sql.functions.split.html
    split_column = split(ufo_df['Date / Time'], ' ')

    # เพิ่มคอลัมน์ Date และ Time + ลบคอลัมน์ 'Date / Time'
    ufo_df_transformed = ufo_df.withColumn('Date', split_column.getItem(0)) \
        .withColumn('Time', split_column.getItem(1)) \
        .drop('Date / Time')

    # จัดเรียงคอลัมน์ให้สวยงาม
    ufo_df_output = ufo_df_transformed.select("Date", "Time", "Country", "City", "State", "Shape")

    # พิมพ์หน้าตาผลลัพธ์บนหน้าจอ
    ufo_df_output.show(5, False)

    # เซฟไฟล์ลง GCS
    # TODO: เปลี่ยนเป็นชื่อ GCS ของคุณ
    ufo_df_output.coalesce(1).write.csv('gs://perth-processed-storage/result.csv', header = True)

    print('UPDATE: Wrote to GCS laew')

if __name__ == "__main__":
  spark = SparkSession.builder.appName("DataTH GCP DE").getOrCreate()
  read_data(spark)
  
  spark.stop()