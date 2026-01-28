import sys
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from pyspark.sql import functions as F

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Lecture des tables
df_sales = glueContext.create_dynamic_frame.from_catalog(
    database="sales",
    table_name="sales"
).toDF()

df_stream = glueContext.create_dynamic_frame.from_catalog(
    database="sales",
    table_name="stream_sales"
).toDF()

def normalize(df):
    for c in df.columns:
        df = df.withColumnRenamed(c, c.lower().replace(" ", "_"))
    return df

df_sales = normalize(df_sales)
df_stream = normalize(df_stream)

df_sales = df_sales.withColumn("event_time", F.col("order_date"))

cols = ["order_id", "event_time", "product_id", "product_name", "region", "quantity"]
df_sales = df_sales.select(cols)
df_stream = df_stream.select(cols)

df_all = df_sales.unionByName(df_stream)

df_all = df_all.withColumn(
    "order_timestamp",
    F.to_timestamp("event_time", "yyyy-MM-dd'T'HH:mm:ss")
).withColumn(
    "order_date",
    F.to_date("order_timestamp")
)

df_all = df_all.filter(F.col("quantity").isNotNull())

agg = df_all.groupBy("product_id", "region").agg(
    F.sum("quantity").alias("total_quantity_sold"),
    F.countDistinct("order_date").alias("nb_days")
)

agg = agg.withColumn(
    "avg_daily_sales",
    F.when(F.col("nb_days") > 0, F.col("total_quantity_sold") / F.col("nb_days"))
     .otherwise(0.1)
)

agg = agg.withColumn("estimated_stock", F.lit(1.5))

agg = agg.withColumn(
    "days_remaining",
    F.when(F.col("avg_daily_sales") > 0,
           F.col("estimated_stock") / F.col("avg_daily_sales"))
     .otherwise(999)
)

agg = agg.withColumn(
    "risk_level",
    F.when(F.col("days_remaining") < 3, "HIGH")
     .when(F.col("days_remaining") < 10, "MEDIUM")
     .otherwise("LOW")
)

agg.write.mode("overwrite").parquet("s3://jl-data-analytics/stock_risk/")

print("Stock risk calculé correctement")
